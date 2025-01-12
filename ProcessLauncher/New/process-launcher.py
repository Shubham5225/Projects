"""
Windows Process Launcher Module

A utility for safely launching Windows system processes from a configuration file.
Only runs executables from the Windows System32 directory for security.
"""

import subprocess
import os
from pathlib import Path
from typing import List, Optional
import logging
import sys
from dataclasses import dataclass

@dataclass
class ProcessConfig:
    """Configuration for a process to be launched."""
    name: str
    executable_path: Path
    
    @classmethod
    def from_name(cls, process_name: str) -> 'ProcessConfig':
        """
        Create a ProcessConfig from a process name, validating it exists in System32.
        
        Args:
            process_name: Name of the process (without .exe extension)
            
        Returns:
            ProcessConfig: Validated process configuration
            
        Raises:
            ValueError: If the process executable doesn't exist in System32
        """
        # Ensure we only work with System32 for security
        system32_path = Path(os.environ.get('SystemRoot', 'C:\\Windows')) / 'System32'
        executable_path = system32_path / f"{process_name}.exe"
        
        if not executable_path.exists():
            raise ValueError(f"Process {process_name} not found in System32 directory")
            
        return cls(
            name=process_name,
            executable_path=executable_path
        )

class ProcessLauncher:
    """Handles the launching of Windows system processes."""
    
    def __init__(self):
        """Initialize the ProcessLauncher."""
        self.logger = logging.getLogger(__name__)
        
    def read_process_list(self, config_file: Path) -> List[str]:
        """
        Read process names from a configuration file.
        
        Args:
            config_file: Path to the configuration file
            
        Returns:
            List[str]: List of process names
            
        Raises:
            FileNotFoundError: If the config file doesn't exist
            IOError: If there's an error reading the file
        """
        try:
            with open(config_file, 'r') as f:
                # Filter out empty lines and strip whitespace
                return [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            self.logger.error(f"Configuration file not found: {config_file}")
            raise
        except IOError as e:
            self.logger.error(f"Error reading configuration file: {e}")
            raise
            
    def launch_process(self, config: ProcessConfig) -> Optional[subprocess.Popen]:
        """
        Launch a single process.
        
        Args:
            config: ProcessConfig object containing process information
            
        Returns:
            Optional[subprocess.Popen]: Process handle if successful, None otherwise
            
        Raises:
            subprocess.SubprocessError: If there's an error launching the process
        """
        try:
            process = subprocess.Popen(
                [str(config.executable_path)],
                shell=False,  # Safer execution
                creationflags=subprocess.CREATE_NO_WINDOW  # Prevent console window
            )
            self.logger.info(f"Successfully launched process: {config.name}")
            return process
        except subprocess.SubprocessError as e:
            self.logger.error(f"Failed to launch process {config.name}: {e}")
            raise
            
    def launch_processes(self, config_file: Path) -> List[subprocess.Popen]:
        """
        Launch all processes specified in the configuration file.
        
        Args:
            config_file: Path to the configuration file
            
        Returns:
            List[subprocess.Popen]: List of successfully launched process handles
        """
        process_list = self.read_process_list(config_file)
        launched_processes = []
        
        for process_name in process_list:
            try:
                config = ProcessConfig.from_name(process_name)
                if process := self.launch_process(config):
                    launched_processes.append(process)
            except ValueError as e:
                self.logger.error(str(e))
                continue
            except subprocess.SubprocessError as e:
                self.logger.error(f"Failed to launch {process_name}: {e}")
                continue
                
        return launched_processes
