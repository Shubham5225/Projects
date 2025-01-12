"""
Module for logging process information to files and sending email reports.
"""
import json
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import logging
import ProcessInfo

class ProcessLogger:
    """Class to handle logging of process information."""
    
    def __init__(self, base_dir: str | Path):
        """
        Initialize ProcessLogger.
        
        Args:
            base_dir: Base directory for log files
        """
        self.base_dir = Path(base_dir)
        self.logger = logging.getLogger(__name__)
        
    def create_log_directory(self, dir_name: str) -> Path:
        """
        Create a directory for log files if it doesn't exist.
        
        Args:
            dir_name: Name of the directory to create
            
        Returns:
            Path: Path to the created directory
        """
        log_dir = self.base_dir / dir_name
        log_dir.mkdir(parents=True, exist_ok=True)
        return log_dir
        
    def write_log(self, processes: List[ProcessInfo], log_dir: Path) -> Path:
        """
        Write process information to a log file.
        
        Args:
            processes: List of process information objects
            log_dir: Directory to write the log file
            
        Returns:
            Path: Path to the created log file
        """
        log_file = log_dir / "process_log.txt"
        
        try:
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write('=' * 80 + '\n')
                f.write(f'Process Log - {datetime.now().isoformat()}\n')
                f.write('=' * 80 + '\n\n')
                
                for proc in processes:
                    json.dump({
                        'pid': proc.pid,
                        'name': proc.name,
                        'username': proc.username,
                        'memory_mb': proc.memory_mb,
                        'create_time': proc.create_time,
                        'cpu_percent': proc.cpu_percent
                    }, f, indent=2)
                    f.write('\n')
                    
            return log_file
        except Exception as e:
            self.logger.error(f"Error writing log file: {str(e)}")
            raise

class EmailReporter:
    """Class to handle email reporting of process information."""
    
    def __init__(self, smtp_server: str = "smtp.gmail.com", smtp_port: int = 587):
        """
        Initialize EmailReporter.
        
        Args:
            smtp_server: SMTP server address
            smtp_port: SMTP server port
        """
        self.smtp_server = smtp_server
        self.smtp_port = smtp_port
        self.logger = logging.getLogger(__name__)
        
    def send_report(
        self,
        sender_email: str,
        sender_password: str,
        recipient_email: str,
        log_file: Path,
        subject: str = "Process Information Report"
    ) -> None:
        """
        Send process information report via email.
        
        Args:
            sender_email: Email address to send from
            sender_password: Password for sender email
            recipient_email: Email address to send to
            log_file: Path to the log file to attach
            subject: Email subject line
        """
        msg = MIMEMultipart()
        msg['From'] = sender_email
        msg['To'] = recipient_email
        msg['Subject'] = subject
        
        body = f"""
        Process Information Report
        Generated at: {datetime.now().isoformat()}
        
        Please find the detailed process information in the attached log file.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Attach log file
        try:
            with open(log_file, 'rb') as f:
                part = MIMEBase('application', 'octet-stream')
                part.set_payload(f.read())
                encoders.encode_base64(part)
                part.add_header(
                    'Content-Disposition',
                    f'attachment; filename="{log_file.name}"'
                )
                msg.attach(part)
        except Exception as e:
            self.logger.error(f"Error attaching log file: {str(e)}")
            raise
            
        # Send email
        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(sender_email, sender_password)
                server.send_message(msg)
        except Exception as e:
            self.logger.error(f"Error sending email: {str(e)}")
            raise
