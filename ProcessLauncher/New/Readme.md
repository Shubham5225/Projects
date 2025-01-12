# Windows Process Launcher

A Python-based utility for safely launching Windows system processes specified in a configuration file. The tool ensures security by restricting process execution to the Windows System32 directory.

---

## Features

- **Secure Process Execution**: Only launches executables located in the Windows System32 directory.
- **Configuration File Support**: Reads process names from a user-specified file.
- **Error Handling**: Logs errors if executables are missing or processes fail to launch.
- **Cross-Process Management**: Supports launching multiple processes simultaneously.

---

## Project Structure

### 1. `cli.py`
- Command-line interface for launching processes.
- Key Features:
  - Arguments:
    - `--config`: Path to the configuration file (default: `inp.txt`).
    - `--log-level`: Set logging level (`DEBUG`, `INFO`, etc.).
  - Ensures compatibility with Windows systems only.
  - Entry point for the application.

### 2. `process-launcher.py`
- Core module for reading process configurations and launching executables.
- Key Features:
  - `ProcessConfig`: Data class for process configuration.
  - `read_process_list(config_file)`: Reads process names from a configuration file.
  - `launch_process(config)`: Launches an individual process securely.
  - `launch_processes(config_file)`: Launches all processes from the configuration file.

---

## Setup & Usage

### Prerequisites
- **Platform**: Windows only.
- **Python Version**: Python 3.9+
- **Required Modules**: `argparse`, `subprocess`, `dataclasses`, `logging`
- Install dependencies:
  ```bash
  pip install -r requirements.txt
