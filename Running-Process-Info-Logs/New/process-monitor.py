"""
Core module for process monitoring and information gathering.
Provides functionality to collect and filter process information using psutil.
"""
import psutil
from typing import List, Dict, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import logging

@dataclass
class ProcessInfo:
    """Data class to store process information in a structured way."""
    pid: int
    name: str
    username: str
    memory_mb: float
    create_time: float
    cpu_percent: float

class ProcessMonitor:
    """Class to handle process monitoring and information gathering."""
    
    def __init__(self):
        """Initialize the ProcessMonitor."""
        self.logger = logging.getLogger(__name__)
    
    def get_process_info(self, process: psutil.Process) -> Optional[ProcessInfo]:
        """
        Get information about a single process.
        
        Args:
            process: psutil.Process object
            
        Returns:
            Optional[ProcessInfo]: Process information if available, None if process cannot be accessed
        """
        try:
            with process.oneshot():  # Efficient system calls
                return ProcessInfo(
                    pid=process.pid,
                    name=process.name(),
                    username=process.username(),
                    memory_mb=process.memory_info().vms / (1024 * 1024),
                    create_time=process.create_time(),
                    cpu_percent=process.cpu_percent()
                )
        except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess) as e:
            self.logger.debug(f"Could not access process {process.pid}: {str(e)}")
            return None
    
    def get_all_processes(self) -> List[ProcessInfo]:
        """
        Get information about all running processes.
        
        Returns:
            List[ProcessInfo]: List of process information objects
        """
        processes = []
        for proc in psutil.process_iter(['pid']):
            if info := self.get_process_info(proc):
                processes.append(info)
        return processes
    
    def find_processes_by_name(self, name: str) -> List[ProcessInfo]:
        """
        Find all processes matching a given name.
        
        Args:
            name: Name of the process to find (case-insensitive)
            
        Returns:
            List[ProcessInfo]: List of matching process information objects
        """
        return [
            proc for proc in self.get_all_processes()
            if name.lower() in proc.name.lower()
        ]
    
    def get_system_info(self) -> Dict[str, Any]:
        """
        Get general system information.
        
        Returns:
            Dict[str, Any]: Dictionary containing system information
        """
        return {
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'total_processes': len(psutil.pids()),
            'boot_time': datetime.fromtimestamp(psutil.boot_time()).isoformat()
        }
