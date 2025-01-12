# Duplicate File Management System

A Python-based utility for detecting, managing, and removing duplicate files from directories. It includes support for checksum-based file identification, logging, and email notifications for operation reports.

---

## Features

- **Detect Duplicates**: Identify duplicate files using their checksums (MD5).
- **Remove Duplicates**: Automatically remove duplicate files while keeping a single instance.
- **Logging**: Maintain logs for operations in the specified directory.
- **Email Notifications**: Send detailed reports about removed files via email.

---

## Project Structure

### 1. `duplicate-handler.py`
- Manages detection and removal of duplicate files.
- Maintains a log of all duplicate-related operations.
- Key Functions:
  - `find_duplicates(checksums)`: Groups files by checksum to identify duplicates.
  - `remove_duplicates(duplicate_groups)`: Deletes duplicate files, logging all removals.

### 2. `file-operations.py`
- Handles file scanning and checksum generation.
- Key Functions:
  - `generate_file_checksum(filepath)`: Computes MD5 checksum of a file.
  - `scan_directory(directory_path)`: Generates a dictionary of filenames mapped to their checksums.

### 3. `utils.py`
- Contains utility classes and functions for logging and notifications.
- Key Features:
  - Email Notifications: `EmailNotifier` class to send reports with logs attached.
  - Logging Setup: `setup_logging(log_dir)` to configure logging for operations.

---

## Setup & Usage

### Prerequisites
- Python 3.9+
- Required modules:
  - `os`, `hashlib`, `smtplib`, `email`
  - Install additional dependencies: `pip install -r requirements.txt` (if applicable)

### Steps
1. **Initialize DuplicateHandler**:
   ```python
   from duplicate_handler import DuplicateHandler
   handler = DuplicateHandler(base_dir="/path/to/directory")
