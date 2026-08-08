# FSW_ASSM

Housekeeping Telemetry Monitoring and Event Generation Software.

This project implements a configurable housekeeping monitor that reads telemetry data, checks parameters against predefined thresholds, generates events with different severity levels, and writes the resulting event log to an output file.

## Instructions to Run the Code

This project uses **[uv](https://astral.sh/uv/)** as the Python package and environment manager.

### 1. Install `uv`

If `uv` is not already installed, install it using:

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

Restart your terminal or reload your shell configuration if required.

Verify the installation:

```bash
uv --version
```

### 2. Install Dependencies

From the project root directory, run:

```bash
uv sync
```

This creates the virtual environment and installs the dependencies specified in `pyproject.toml`.

### 3. Activate the Virtual Environment

Activate the environment using:

```bash
source .venv/bin/activate
```

### 4. Run the Application

Run the application from the project root:

```bash
python app.py
```

The generated event log will be written to:

```text
outputs/events.json
```

## Project Structure

```text
.
├── app.py
├── inputs
│   ├── define_threshold.json
│   └── housekeeping_nominal.json
├── outputs
│   └── events.json
├── LICENSE
├── pyproject.toml
├── README.md
├── src
│   └── fsw_assm
│       ├── main.py
│       ├── threshold_check.py
│       ├── utils.py
│       └── write_log.py
└── uv.lock
```

## Directory Description

| Path                               | Description                                        |
| ---------------------------------- | -------------------------------------------------- |
| `app.py`                           | Application entry point                            |
| `inputs/define_threshold.json`     | Configuration file containing parameter thresholds |
| `inputs/housekeeping_nominal.json` | Input housekeeping telemetry data                  |
| `outputs/events.json`              | Generated event log                                |
| `src/fsw_assm/main.py`             | Main application logic                             |
| `src/fsw_assm/threshold_check.py`  | Threshold checking and severity determination      |
| `src/fsw_assm/utils.py`            | Common utility functions                           |
| `src/fsw_assm/write_log.py`        | Event log generation and output handling           |
| `pyproject.toml`                   | Project metadata and dependency configuration      |
| `uv.lock`                          | Locked dependency versions                         |

## Output

After running:

```bash
python app.py
```

the application generates an event log at:

```text
outputs/events.json
```

The output contains the detected housekeeping events, including information such as:

* Timestamp
* Subsystem
* Violated parameter
* Severity
* Recommended software action

## Sample output
``` text
|Timestamp|               |Subsystem|           |Parameter|           |Severity|                 |Action|
========================================================================================================================
2026-08-04T12:00:00Z      payload              temperature_C             WARNING    Record the high temperature and continue monitoring.
2026-08-04T12:00:00Z      payload              cpu_usage_percent         INFO       No action required.
2026-08-04T12:00:00Z      payload              memory_usage_percent      INFO       No action required.
2026-08-04T12:00:00Z      fpga                 temperature_C             INFO       No action required.
2026-08-04T12:00:00Z      fpga                 utilization_percent       INFO       No action required.
2026-08-04T12:00:10Z      payload              temperature_C             WARNING    Record the high temperature and continue monitoring.
```
## Notes

* Thresholds can be modified in `inputs/define_threshold.json`.
* Housekeeping telemetry can be provided through `inputs/housekeeping_nominal.json`.
* The `outputs` directory is created automatically if it does not already exist.
* Run the application from the **project root directory** so that the configured input and output paths resolve correctly.
