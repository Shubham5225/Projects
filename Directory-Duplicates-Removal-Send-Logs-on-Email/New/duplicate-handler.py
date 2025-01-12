"""
Module for detecting and removing duplicate files based on their checksums.
"""
from typing import Dict, Set, List, Tuple
from pathlib import Path
import logging
from datetime import datetime

class DuplicateHandler:
    """
    Class to handle detection and removal of duplicate files.
    """
    
    def __init__(self, base_dir: str | Path):
        """
        Initialize DuplicateHandler.
        
        Args:
            base_dir (Union[str, Path]): Base directory for operations
        """
        self.base_dir = Path(base_dir)
        self._setup_logging()
        
    def _setup_logging(self) -> None:
        """Configure logging for the duplicate handler."""
        logging.basicConfig(
            filename=self.base_dir / "duplicate_operations.log",
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s'
        )
        
    def find_duplicates(self, checksums: Dict[str, str]) -> Dict[str, List[str]]:
        """
        Find duplicate files based on their checksums.
        
        Args:
            checksums (Dict[str, str]): Dictionary of filename to checksum mappings
            
        Returns:
            Dict[str, List[str]]: Dictionary mapping checksums to lists of duplicate filenames
        """
        checksum_groups: Dict[str, List[str]] = {}
        
        for filename, checksum in checksums.items():
            if checksum in checksum_groups:
                checksum_groups[checksum].append(filename)
            else:
                checksum_groups[checksum] = [filename]
                
        # Filter out unique files
        return {k: v for k, v in checksum_groups.items() if len(v) > 1}
        
    def remove_duplicates(self, duplicate_groups: Dict[str, List[str]]) -> Tuple[int, List[str]]:
        """
        Remove duplicate files, keeping only one copy of each.
        
        Args:
            duplicate_groups (Dict[str, List[str]]): Groups of duplicate files
            
        Returns:
            Tuple[int, List[str]]: Number of files removed and list of removed filenames
            
        Raises:
            PermissionError: If unable to remove files
        """
        removed_count = 0
        removed_files = []
        
        for checksum, filenames in duplicate_groups.items():
            # Keep the first file, remove the rest
            for filename in filenames[1:]:
                try:
                    filepath = self.base_dir / filename
                    filepath.unlink()
                    removed_count += 1
                    removed_files.append(filename)
                    logging.info(f"Removed duplicate file: {filename}")
                except PermissionError:
                    logging.error(f"Permission denied when trying to remove: {filename}")
                    raise
                except Exception as e:
                    logging.error(f"Error removing {filename}: {str(e)}")
                    raise
                    
        return removed_count, removed_files
