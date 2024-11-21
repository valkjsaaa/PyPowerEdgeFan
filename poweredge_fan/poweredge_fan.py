import argparse
import time
from subprocess import TimeoutExpired

from poweredge_fan.hardware import IPMIControl, get_all_sensors

arg_parser = argparse.ArgumentParser(description='PowerEdge Fan Controller')
arg_parser.add_argument('-H', '--host', type=str, help='IP address of the iDRAC', required=True)
arg_parser.add_argument('-U', '--username', type=str, help='Username for the iDRAC', required=True)
arg_parser.add_argument('-P', '--password', type=str, help='Password for the iDRAC', required=True)
arg_parser.add_argument('-I', '--high', type=float, help='Highest fan output', required=True)
arg_parser.add_argument('-L', '--low', type=float, help='Lowest fan output', required=True)
arg_parser.add_argument('-T', '--target', type=float, help='Target temperature for the fan controller', required=True)

ipmi: IPMIControl

class PIDController:
    def __init__(self, Kp, Ki, Kd, setpoint, high, low):
        self.Kp = Kp
        self.Ki = Ki
        self.Kd = Kd
        self.setpoint = setpoint
        self.high = high
        self.low = low

        self.integral = -46
        self.last_error = 0
        self.last_time = time.time()

    def update(self, current_temperature):
        # Calculate the error and time difference
        error = self.setpoint - current_temperature
        current_time = time.time()
        time_diff = current_time - self.last_time

        # Calculate proportional term
        proportional = self.Kp * error

        # Calculate integral term
        self.integral += self.Ki * error * time_diff
        if self.integral > 0:
            self.integral = 0

        # Calculate derivative term
        derivative = self.Kd * (error - self.last_error) / time_diff

        # Update the last error and last time
        self.last_error = error
        self.last_time = current_time

        # Compute the PID output
        pid_output = proportional + self.integral + derivative

        # Constrain PID output to fan speed range
        return max(min(pid_output, self.high), self.low)


def get_cpu_temperature():
    temp_dict = ipmi.get_temperatures()
    return max(temp_dict["cpu_temps"])


# Global variable for last fan speed
last_fan_speed = None

def set_fan_speed(speed):
    global last_fan_speed
    # keep speed within 0-100:
    speed = -speed
    speed = max(min(speed, 100), 5)
    
    # Smooth transition to the target speed
    if last_fan_speed is None:
        last_fan_speed = speed
    
    step = 5  # Max RPM increment per adjustment
    if abs(speed - last_fan_speed) > step:
        speed = last_fan_speed + step if speed > last_fan_speed else last_fan_speed - step

    # Update the fan speed and the last_fan_speed
    ipmi.set_fan_speed(int(speed))
    last_fan_speed = speed
    pass

last_sensor_values = []
last_sensor_values_count = 20
spike_tolerance = 20  
tolerance_increment = 5  
tolerance_reset_time = 30 
last_spike_time = None 

def loop(args):
    # PID parameters and target temperature
    Kp = 3
    Ki = 0.3
    Kd = 0.1
    target_temperature = args.target

    pid_controller = PIDController(Kp, Ki, Kd, target_temperature, args.high, args.low)

    # Main loop to update the fan speed based on PID output
    while True:
        try:
            global spike_tolerance, last_spike_time
            sensor_values = get_all_sensors()
            avg_sensor_value = sum(sensor_values) / len(sensor_values)
            current_time = time.time()

            # Check for inconsistencies
            if max(sensor_values) - avg_sensor_value > spike_tolerance:
                print("Sensor values are not consistent, skipping update")

                # Adjust the spike tolerance incrementally
                if last_spike_time and current_time - last_spike_time < 10:
                    spike_tolerance += tolerance_increment
                    print(f"Increasing spike tolerance to {spike_tolerance}")
                else:
                    spike_tolerance = 20  # Reset tolerance
                    print("Resetting spike tolerance to 20")

                last_spike_time = current_time

                ipmi.set_fan_automatic()
                time.sleep(1)
                continue

            # Reset spike_tolerance after the reset time
            if last_spike_time and current_time - last_spike_time > tolerance_reset_time:
                spike_tolerance = 20

            last_sensor_values.append(avg_sensor_value)
            if len(last_sensor_values) > last_sensor_values_count:
                last_sensor_values.pop(0)

            # Smooth current temperature using moving average
            current_temperature = sum(last_sensor_values) / len(last_sensor_values)
            pid_output = pid_controller.update(current_temperature)
            print(f"CPU temperature: {current_temperature:.2f} PID output: {pid_output:.2f}")
            print(f"Current parameters: Kp={pid_controller.Kp:.2f} Ki={pid_controller.Ki:.2f} Kd={pid_controller.Kd:.2f}")

            # Adjust the fan speed using the PID output
            set_fan_speed(pid_output)

            # Sleep for some time to avoid excessive adjustments
            time.sleep(0.1)
        except TimeoutExpired as e:
            print("Timeout expired, skipping update")
            print(e)
            ipmi.set_fan_automatic()
            time.sleep(1)

def main():
    global ipmi
    args = arg_parser.parse_args()
    ipmi = IPMIControl(args.host, args.username, args.password)
    try:
        loop(args)
    finally:
        ipmi.set_fan_automatic()

if __name__ == "__main__":
    main()