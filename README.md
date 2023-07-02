# PyPowerEdgeFan

PyPowerEdgeFan is a Python-based PID fan controller for Dell PowerEdge servers.

## Installation

Install the package using pip:

```bash
pip install poweredge_fan
```

Replace `poweredge_fan` with the name of your package.

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

## Contributing

Contributions to PyPowerEdgeFan are welcome! To contribute, please open an issue or submit a pull request through the [GitHub repository](https://github.com/valkjsaaa/PyPowerEdgeFan).