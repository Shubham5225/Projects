"""
File system operations module for handling file scanning and checksum generation.
"""
import os
import hashlib
from typing import Dict, Optional
from pathlib import Path

def generate_file_checksum(filepath: str | Path, chunk_size: int = 4096) -> str:
    """
    Generate MD5 checksum for a given file.
    
    Args:
        filepath (Union[str, Path]): Path to the file
        chunk_size (int): Size of chunks to read at once (default: 4096 bytes)
    
    Returns:
        str: Hexadecimal representation of the MD5 hash
        
    Raises:
        FileNotFoundError: If the specified file doesn't exist
        PermissionError: If the program lacks permission to read the file
    """
    hash_md5 = hashlib.md5()
    
    filepath = Path(filepath)
    if not filepath.exists():
        raise FileNotFoundError(f"File not found: {filepath}")
        
    try:
        with open(filepath, "rb") as f:
            for chunk in iter(lambda: f.read(chunk_size), b""):
                hash_md5.update(chunk)
        return hash_md5.hexdigest()
    except PermissionError:
        raise PermissionError(f"Permission denied to read file: {filepath}")

def scan_directory(directory_path: str | Path) -> Dict[str, str]:
    """
    Scan a directory and generate checksums for all files.
    
    Args:
        directory_path (Union[str, Path]): Path to the directory to scan
        
    Returns:
        Dict[str, str]: Dictionary mapping filenames to their checksums
        
    Raises:
        NotADirectoryError: If the specified path is not a directory
        PermissionError: If the program lacks permission to access the directory
    """
    directory_path = Path(directory_path)
    if not directory_path.is_dir():
        raise NotADirectoryError(f"Not a directory: {directory_path}")
        
    checksums: Dict[str, str] = {}
    
    try:
        for filepath in directory_path.rglob("*"):
            if filepath.is_file():
                checksums[filepath.name] = generate_file_checksum(filepath)
        return checksums
    except PermissionError:
        raise PermissionError(f"Permission denied to access directory: {directory_path}")
