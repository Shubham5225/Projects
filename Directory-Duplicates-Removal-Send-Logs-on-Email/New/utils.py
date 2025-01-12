"""
Utility functions for file operations, logging, and email notifications.
"""
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import logging

class EmailNotifier:
    """
    Class to handle email notifications about duplicate file operations.
    """
    
    def __init__(self, sender_email: str, sender_password: str, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize EmailNotifier.
        
        Args:
            sender_email (str): Email address to send from
            sender_password (str): Password or app-specific password for the email account
            smtp_server (str): SMTP server address (default: smtp.gmail.com)
            smtp_port (int): SMTP server port (default: 587)
        """
        self.sender_email = sender_email
        self.sender_password = sender_password
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        
    def send_report(self, recipient_email: str, removed_files: List[str], log_file: Path) -> None:
        """
        Send email report about removed duplicate files.
        
        Args:
            recipient_email (str): Email address to send report to
            removed_files (List[str]): List of removed duplicate files
            log_file (Path): Path to the log file to attach
            
        Raises:
            smtplib.SMTPException: If there's an error sending the email
        """
        msg = MIMEMultipart()
        msg['From'] = self.sender_email
        msg['To'] = recipient_email
        msg['Subject'] = f"Duplicate Files Removal Report - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        body = f"""
        Duplicate Files Removal Report
        
        Total files removed: {len(removed_files)}
        
        Removed files:
        {chr(10).join(f'- {file}' for file in removed_files)}
        
        Please see the attached log file for details.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach log file
        with open(log_file, "rb") as f:
            part = MIMEBase('application', 'octet-stream')
            part.set_payload(f.read())
            encoders.encode_base64(part)
            part.add_header('Content-Disposition', f'attachment; filename="{log_file.name}"')
            msg.attach(part)
            
        # Send email
        with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
            server.starttls()
            server.login(self.sender_email, self.sender_password)
            server.send_message(msg)

def setup_logging(log_dir: Path) -> None:
    """
    Set up logging configuration.
    
    Args:
        log_dir (Path): Directory to store log files
    """
    log_file = log_dir / f"duplicate_removal_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
    
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(log_file),
            logging.StreamHandler()
        ]
    )
