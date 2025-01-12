"""
Startup Configuration Script
Adds programs to Windows startup for automatic launch on system boot
"""

import os
import pathlib
import logging
from typing import Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class StartupManager:
    def __init__(self):
        self.username = os.getenv('USERNAME') or os.getenv('USER')
        self.startup_path = pathlib.Path(
            f'C:/Users/{self.username}/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup'
        )

    def add_to_startup(self, file_path: Optional[str] = None) -> bool:
        """
        Add a program to Windows startup.
        
        Args:
            file_path: Path to the program to add to startup.
                      If None, uses the directory of the current script.
        
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            if not file_path:
                file_path = str(pathlib.Path(__file__).parent.resolve())

            if not self.startup_path.exists():
                logger.error(f"Startup directory not found: {self.startup_path}")
                return False

            bat_file = self.startup_path / "launcher.bat"
            
            with open(bat_file, "w") as f:
                f.write(f'@echo off\nstart "" "{file_path}"\n')
            
            logger.info(f"Successfully added to startup: {file_path}")
            return True

        except Exception as e:
            logger.error(f"Failed to add to startup: {e}")
            return False

def main():
    manager = StartupManager()
    success = manager.add_to_startup()
    
    if success:
        print("Successfully configured startup launcher")
    else:
        print("Failed to configure startup launcher")

if __name__ == "__main__":
    main()
