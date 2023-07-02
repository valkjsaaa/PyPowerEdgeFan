import subprocess


class IPMIControl:
    def __init__(self, ipmihost, ipmiuser, ipmipw,
                 ipmiek="0000000000000000000000000000000000000000",
                 cpuid0="0Eh", cpuid1="0Fh", ambient_id="04h", exhaust_id="01h"):
        self.IPMIHOST = ipmihost
        self.IPMIUSER = ipmiuser
        self.IPMIPW = ipmipw
        self.IPMIEK = ipmiek
        self.CPUID0 = cpuid0
        self.CPUID1 = cpuid1
        self.AMBIENT_ID = ambient_id
        self.EXHAUST_ID = exhaust_id

    def run_ipmi_command(self, command_args):
        ipmi_base_command = ["ipmitool", "-I", "lanplus", "-H", self.IPMIHOST, "-U", self.IPMIUSER, "-P", self.IPMIPW,
                             "-y", self.IPMIEK]
        return subprocess.check_output(ipmi_base_command + command_args, timeout=10).decode("utf-8")

    def get_temperatures(self):
        ipmi_output = self.run_ipmi_command(["sdr", "type", "temperature"])
        cpu_temps = []
        ambient_temp = None
        exhaust_temp = None
        for line in ipmi_output.splitlines():
            if "Temp" in line:
                line_parts = line.split("|")
                temp_id = line_parts[1].strip()
                temp = line_parts[4].strip().split(" ")[0]
                if temp_id == self.CPUID0 or temp_id == self.CPUID1:
                    cpu_temps.append(float(temp))
                elif temp_id == self.AMBIENT_ID:
                    ambient_temp = float(temp)
                elif temp_id == self.EXHAUST_ID:
                    exhaust_temp = float(temp)

        return {"cpu_temps": cpu_temps, "ambient_temp": ambient_temp, "exhaust_temp": exhaust_temp}

    def set_fan_speed(self, speed):
        hex_value = hex(speed)
        self.run_ipmi_command(["raw", "0x30", "0x30", "0x01", "0x00"])
        self.run_ipmi_command(["raw", "0x30", "0x30", "0x02", "0xff", hex_value])

    def set_fan_automatic(self):
        self.run_ipmi_command(["raw", "0x30", "0x30", "0x01", "0x01"])


if __name__ == "__main__":
    ipmi = IPMIControl()
    print(ipmi.get_temperatures())
    ipmi.set_fan_speed(50)
    ipmi.set_fan_automatic()