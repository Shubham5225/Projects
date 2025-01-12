"""
Main script for the Duplicate File Management System.
Handles duplicate file detection, removal, and notification.
"""
from pathlib import Path
import argparse
import sys
from typing import Optional

from duplicate_handler import DuplicateHandler
from file_operations import scan_directory
from utils import EmailNotifier, setup_logging

def parse_arguments():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Duplicate File Management System")
    parser.add_argument("directory", type=str, help="Directory to scan for duplicates")
    parser.add_argument("--email", type=str, help="Email address to send report to")
    parser.add_argument("--sender-email", type=str, help="Sender email address")
    parser.add_argument("--sender-password", type=str, help="Sender email password")
    parser.add_argument("--smtp-server", type=str, default="smtp.gmail.com", 
                       help="SMTP server address (default: smtp.gmail.com)")
    parser.add_argument("--smtp-port", type=int, default=587, 
                       help="SMTP server port (default: 587)")
    return parser.parse_args()

def main():
    """Main function to run the duplicate file management system."""
    # Parse command line arguments
    args = parse_arguments()
    base_dir = Path(args.directory)
    
    try:
        # Validate directory
        if not base_dir.exists() or not base_dir.is_dir():
            print(f"Error: {base_dir} is not a valid directory")
            sys.exit(1)
            
        # Initialize components
        handler = DuplicateHandler(base_dir)
        setup_logging(base_dir)
        
        # Set up email notifier if email parameters are provided
        email_notifier: Optional[EmailNotifier] = None
        if all([args.email, args.sender_email, args.sender_password]):
            email_notifier = EmailNotifier(
                sender_email=args.sender_email,
                sender_password=args.sender_password,
                smtp_server=args.smtp_server,
                smtp_port=args.smtp_port
            )
        
        # Scan directory and generate checksums
        print(f"Scanning directory: {base_dir}")
        checksums = scan_directory(base_dir)
        print(f"Found {len(checksums)} files")
        
        # Find duplicates
        duplicate_groups = handler.find_duplicates(checksums)
        total_duplicates = sum(len(files) - 1 for files in duplicate_groups.values())
        print(f"Found {total_duplicates} duplicate files")
        
        if total_duplicates == 0:
            print("No duplicates found. Exiting...")
            sys.exit(0)
            
        # Remove duplicates
        print("Removing duplicate files...")
        removed_count, removed_files = handler.remove_duplicates(duplicate_groups)
        print(f"Successfully removed {removed_count} duplicate files")
        
        # Send email report if configured
        if email_notifier and args.email:
            print("Sending email report...")
            try:
                email_notifier.send_report(
                    recipient_email=args.email,
                    removed_files=removed_files,
                    log_file=base_dir / "duplicate_operations.log"
                )
                print("Email report sent successfully")
            except Exception as e:
                print(f"Failed to send email report: {str(e)}")
                
    except PermissionError as e:
        print(f"Permission error: {str(e)}")
        sys.exit(1)
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main()
