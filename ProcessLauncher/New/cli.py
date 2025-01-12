"""
Command-line interface for the Windows Process Launcher.
"""

import argparse
import sys
from pathlib import Path
import logging
import ProcessLauncher

def setup_logging(level: str = "INFO") -> None:
    """Configure logging with the specified level."""
    logging.basicConfig(
        level=getattr(logging, level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def create_parser() -> argparse.ArgumentParser:
    """Create and configure the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Launch Windows system processes from a configuration file"
    )
    
    parser.add_argument(
        '--config',
        type=Path,
        default=Path('inp.txt'),
        help="Path to the process configuration file (default: inp.txt)"
    )
    
    parser.add_argument(
        '--log-level',
        choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'],
        default='INFO',
        help="Set the logging level"
    )
    
    return parser

def main() -> None:
    """Main entry point for the CLI."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Set up logging
    setup_logging(args.log_level)
    logger = logging.getLogger(__name__)
    
    try:
        # Ensure we're running on Windows
        if sys.platform != 'win32':
            logger.error("This script only runs on Windows systems")
            sys.exit(1)
            
        launcher = ProcessLauncher()
        launched_processes = launcher.launch_processes(args.config)
        
        logger.info(f"Successfully launched {len(launched_processes)} processes")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
