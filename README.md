# FSW\_ASSM

Housekeeping Telemetry Monitoring and Event Generation Software.

This project implements a configurable housekeeping monitor that reads telemetry data, checks parameters against predefined thresholds, generates events with different severity levels, and writes the resulting event log to an output file.

## Table of Contents

- [Instructions to Run the Code](#instructions-to-run-the-code)
  - [1. Install `uv`](#1-install-uv)
  - [2. Install Dependencies](#2-install-dependencies)
  - [3. Activate the Virtual Environment](#3-activate-the-virtual-environment)
  - [4. Run the Application](#4-run-the-application)
- [Project Structure](#project-structure)
- [Directory Description](#directory-description)
- [Output](#output)
- [Sample output](#sample-output)
- [Notes](#notes)
- [Additional notes](#additional-notes)
- [Post review modification](#post-review-modification)
- [Run test_cases](#pytest)

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
outputs/event_log.json
```

## Project Structure

```text
.
├── app.py
├── inputs
│   ├── define_threshold.json
│   └── housekeeping_nominal.json
├── LICENSE
├── notes
│   ├── Coding task.pdf
│   ├── FS architecture [Task 1].pdf
│   ├── FSE PSR.pdf
│   ├── TASK_2.pdf
│   ├── Task_3.pdf
│   └── VyomIC general.pdf
├── outputs
│   └── event_log.json
├── pyproject.toml
├── README.md
├── sample_results.json
├── src
│   ├── fsw_assm
│   │   ├── main.py
│   │   ├── threshold_check.py
│   │   ├── utils.py
│   │   └── write_log.py
│   └── test
│       ├── __init__.py
│       ├── test_main.py
│       ├── test_threshold_check.py
│       ├── test_utils.py
│       └── test_write_log.py
└── uv.lock
```

## Directory Description

| Path                               | Description                                        |
| ---------------------------------- | -------------------------------------------------- |
| `app.py`                           | Application entry point                            |
| `inputs/define_threshold.json`     | Configuration file containing parameter thresholds |
| `inputs/housekeeping_nominal.json` | Input housekeeping telemetry data                  |
| `outputs/event_log.json`           | Generated event log                                |
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

OR

```bash
python app.py --hk_telemetry <telemetry filename> --config <threshold filename> --output <event log filename>
```

the application generates an event log at:

```text
outputs/event_log.json
```

The output contains the detected housekeeping events, including information such as:

- Timestamp
- Subsystem
- Violated parameter
- Severity
- Recommended software action

## Sample output

```text
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

- Thresholds can be modified in `inputs/define_threshold.json`.
- Housekeeping telemetry can be provided through `inputs/housekeeping_nominal.json`.
- The `outputs` directory is created automatically if it does not already exist.
- Run the application from the **project root directory** so that the configured input and output paths resolve correctly.

## Additional notes

- `https://digitalcommons.usu.edu/cgi/viewcontent.cgi?article=6066&context=smallsat`

## Post review modification

- bug fixed: write_event_log by passing the CLI passed filename bug fixed.
- sample test cases and error handling is completed.

## pytest

- Implemented test cases using pytest. Change the CWD to `src/` folder and run the following:

```bash
pytest
```