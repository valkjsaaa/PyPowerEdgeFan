# PyPowerEdgeFan

PyPowerEdgeFan is a Python-based PID fan controller for Dell PowerEdge servers.

With PyPowerEdgeFan, the fan speed with be adjusted dynamically based on the CPU temperature.
This allows the fan to run at a lower speed when the CPU is cool, reducing noise and power consumption.
Another added bonus comparing to a static fan curve is that the fan speed is that it needs less tuning and will reduce the annoying oscillation between two fan speeds.

## Disclaimer

This project is not affiliated with Dell in any way.

I have only tested this on a Dell PowerEdge R730xd. It may or may not work on other models.

Adjusting fan speed is potentially dangerous. If the fan speed is too low, the server may overheat and cause damage to the hardware or even objects around the server.
**Use at your own risk.**
I **highly recommend test the cli tool in shell mode first** to make sure the script is working for your scenario before running it in daemon mode.

## Installation

### Install the package using pip:

```bash
pip install poweredge_fan
```

### Set up sensors on Ubuntu

To make sure the required `sensors` package is installed on Ubuntu, run the following command:

```bash
sudo apt-get install lm-sensors
```

After installing lm-sensors, you can run `sensors-detect` to configure sensors on your system. It will ask you a series of questions to identify the correct sensors for your hardware:

```bash
sudo sensors-detect
```

Follow the prompts and answer the questions accordingly. You may need to reboot your system after the process is complete to ensure proper functionality.

To make sure your sensors are working properly, run the following command:

```bash
sensors
```

You should see output similar to the following:

```
coretemp-isa-0000
Adapter: ISA adapter
Package id 0:  +58.0°C  (high = +77.0°C, crit = +87.0°C)
Core 0:        +49.0°C  (high = +77.0°C, crit = +87.0°C)
Core 1:        +47.0°C  (high = +77.0°C, crit = +87.0°C)
Core 2:        +48.0°C  (high = +77.0°C, crit = +87.0°C)
Core 3:        +48.0°C  (high = +77.0°C, crit = +87.0°C)
Core 4:        +49.0°C  (high = +77.0°C, crit = +87.0°C)
Core 5:        +49.0°C  (high = +77.0°C, crit = +87.0°C)
Core 6:        +48.0°C  (high = +77.0°C, crit = +87.0°C)
Core 7:        +47.0°C  (high = +77.0°C, crit = +87.0°C)

coretemp-isa-0001
Adapter: ISA adapter
Package id 1:  +66.0°C  (high = +77.0°C, crit = +87.0°C)
Core 0:        +59.0°C  (high = +77.0°C, crit = +87.0°C)
Core 1:        +57.0°C  (high = +77.0°C, crit = +87.0°C)
Core 2:        +57.0°C  (high = +77.0°C, crit = +87.0°C)
Core 3:        +57.0°C  (high = +77.0°C, crit = +87.0°C)
Core 4:        +54.0°C  (high = +77.0°C, crit = +87.0°C)
Core 5:        +56.0°C  (high = +77.0°C, crit = +87.0°C)
Core 6:        +54.0°C  (high = +77.0°C, crit = +87.0°C)
Core 7:        +55.0°C  (high = +77.0°C, crit = +87.0°C)
```
PyPowerEdgeFan uses the average of all the core temperatures to determine the fan speed.

## Usage

To use PyPowerEdgeFan, run the following command:

```bash
poweredge_fan -H <host> -U <username> -P <password>
```

Replace `<host>`, `<username>`, and `<password>` with the appropriate values for your iDRAC.

### Arguments

- `-H`, `--host`: IP address of the iDRAC (required)
- `-U`, `--username`: Username for the iDRAC (required)
- `-P`, `--password`: Password for the iDRAC (required)

## Running as a systemd service

To run PyPowerEdgeFan as a systemd service, follow these steps:

1. Create a file called `poweredge_fan.service` with the Systemd unit template provided in this repository.

2. Replace `<host>`, `<username>`, and `<password>` in the `poweredge_fan.service` file with the appropriate values for your iDRAC.

3. Copy the `poweredge_fan.service` file to `/etc/systemd/system/`:

   ```
   sudo cp poweredge_fan.service /etc/systemd/system/
   ```

4. Reload the systemd configuration:

   ```
   sudo systemctl daemon-reload
   ```

5. Enable the service to start at boot:

   ```
   sudo systemctl enable poweredge_fan
   ```

6. Start the service:

   ```
   sudo systemctl start poweredge_fan
   ```

7. Check the status of the service:

   ```
   sudo systemctl status poweredge_fan
   ```

## Contributing

Contributions to PyPowerEdgeFan are welcome! To contribute, please open an issue or submit a pull request through the [GitHub repository](https://github.com/valkjsaaa/PyPowerEdgeFan).