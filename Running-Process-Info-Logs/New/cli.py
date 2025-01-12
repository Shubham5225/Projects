"""
Command-line interface module for process monitoring tools.
"""
import argparse
import sys
import logging
from pathlib import Path
from typing import Optional
from process_monitor import ProcessMonitor
from process_logger import ProcessLogger, EmailReporter

def setup_logging(log_level: str = "INFO") -> None:
    """Set up logging configuration."""
    logging.basicConfig(
        level=getattr(logging, log_level),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def create_parser() -> argparse.ArgumentParser:
    """Create command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Process monitoring and reporting tool"
    )
    
    parser.add_argument(
        '--output-dir',
        type=str,
        required=True,
        help="Directory to store output files"
    )
    
    parser.add_argument(
        '--process-name',
        type=str,
        help="Filter processes by name (optional)"
    )
    
    parser.add_argument(
        '--email',
        action='store_true',
        help="Send report via email"
    )
    
    parser.add_argument(
        '--sender-email',
        type=str,
        help="Sender email address (required if --email is used)"
    )
    
    parser.add_argument(
        '--sender-password',
        type=str,
        help="Sender email password (required if --email is used)"
    )
    
    parser.add_argument(
        '--recipient-email',
        type=str,
        help="Recipient email address (required if --email is used)"
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
        # Initialize components
        monitor = ProcessMonitor()
        process_logger = ProcessLogger(args.output_dir)
        
        # Get process information
        if args.process_name:
            processes = monitor.find_processes_by_name(args.process_name)
        else:
            processes = monitor.get_all_processes()
        
        # Create output directory and write log
        log_dir = process_logger.create_log_directory("process_logs")
        log_file = process_logger.write_log(processes, log_dir)
        
        # Send email if requested
        if args.email:
            if not all([args.sender_email, args.sender_password, args.recipient_email]):
                parser.error("Email sending requires --sender-email, --sender-password, and --recipient-email")
            
            reporter = EmailReporter()
            reporter.send_report(
                args.sender_email,
                args.sender_password,
                args.recipient_email,
                log_file
            )
            logger.info("Email report sent successfully")
            
        logger.info(f"Process information logged to {log_file}")
        
    except Exception as e:
        logger.error(f"Error: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
