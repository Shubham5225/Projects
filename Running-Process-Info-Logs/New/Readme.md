# Process Monitoring and Logging Tool

A Python-based CLI tool for real-time monitoring and logging of system processes. It supports detailed logging, filtering processes by name, and email notifications for process reports.

---

## Features

- **Monitor Processes**: Retrieve and log details of all running processes.
- **Filter by Name**: Option to filter and log processes based on a specific name.
- **Email Reports**: Send detailed process reports via email with log files attached.
- **System Info**: Gather general system information (CPU usage, memory usage, etc.).

---

## Project Structure

### 1. `cli.py`
- Command-line interface for managing process monitoring and logging.
- Key Features:
  - CLI Arguments:
    - `--output-dir`: Specify output directory for log files (required).
    - `--process-name`: Filter processes by name (optional).
    - `--email`: Enable email reporting.
    - `--sender-email`, `--sender-password`, `--recipient-email`: Email credentials and recipient address (required if `--email` is used).
    - `--log-level`: Set logging level (`DEBUG`, `INFO`, etc.).
  - Main entry point: Executes process monitoring and logging workflow.

### 2. `process-monitor.py`
- Core module for gathering process information.
- Key Features:
  - `get_all_processes()`: Retrieve details of all running processes.
  - `find_processes_by_name(name)`: Filter processes by name.
  - `get_system_info()`: Collect system-level metrics (CPU, memory, etc.).

### 3. `process-logger.py`
- Handles logging of process information and sending email reports.
- Key Features:
  - `create_log_directory(dir_name)`: Create a directory for storing logs.
  - `write_log(processes, log_dir)`: Save process details to a log file.
  - `EmailReporter`: Send process reports via email.

---

## Setup & Usage

### Prerequisites
- Python 3.9+
- Required modules: `psutil`, `argparse`, `smtplib`, `email`
- Install dependencies:
  ```bash
  pip install psutil
