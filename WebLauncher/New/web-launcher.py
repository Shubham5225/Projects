"""
WebLauncher - Automated website launcher with scheduling capabilities
Launches specified websites from a configuration file at scheduled times
"""

import argparse
import logging
import pathlib
import schedule
import time
import urllib3
import webbrowser
from typing import List, Optional
from urllib3.exceptions import URLError

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class WebLauncher:
    def __init__(self, config_path: pathlib.Path):
        self.config_path = config_path
        self.http = urllib3.PoolManager(timeout=urllib3.Timeout(connect=2.0, read=2.0))

    def check_internet_connection(self) -> bool:
        """Check if internet connection is available."""
        try:
            self.http.request('GET', 'http://www.google.com')
            return True
        except URLError as err:
            logger.error(f"Internet connection error: {err}")
            return False

    def extract_urls(self, text: str) -> List[str]:
        """Extract valid URLs from text using proper URL parsing."""
        try:
            url = urllib3.util.parse_url(text.strip())
            if url.scheme in ('http', 'https') and url.host:
                return [text.strip()]
        except Exception as e:
            logger.warning(f"Invalid URL found: {text.strip()}")
        return []

    def read_urls_from_config(self) -> List[str]:
        """Read and validate URLs from configuration file."""
        try:
            with open(self.config_path, 'r') as f:
                urls = []
                for line in f:
                    urls.extend(self.extract_urls(line))
                return urls
        except FileNotFoundError:
            logger.error(f"Configuration file not found: {self.config_path}")
            return []

    def launch_websites(self) -> None:
        """Launch all configured websites in new browser tabs."""
        if not self.check_internet_connection():
            logger.error("No internet connection available")
            return

        urls = self.read_urls_from_config()
        if not urls:
            logger.warning("No valid URLs found in configuration")
            return

        for url in urls:
            try:
                webbrowser.open(url, new=2)
                logger.info(f"Launched: {url}")
            except Exception as e:
                logger.error(f"Failed to launch {url}: {e}")

def main():
    parser = argparse.ArgumentParser(
        description="WebLauncher - Automated website launcher with scheduling",
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-t', '--time',
        help='Schedule time in HH:MM format (24-hour)',
        default='18:42'
    )
    parser.add_argument(
        '-c', '--config',
        help='Path to configuration file containing URLs',
        default='inp.txt',
        type=pathlib.Path
    )

    args = parser.parse_args()
    launcher = WebLauncher(args.config)

    logger.info("=== WebLauncher Started ===")
    logger.info(f"Scheduled launch time: {args.time}")

    # Schedule the task
    schedule.every().day.at(args.time).do(launcher.launch_websites)

    try:
        while True:
            schedule.run_pending()
            time.sleep(1)
    except KeyboardInterrupt:
        logger.info("WebLauncher stopped by user")
    except Exception as e:
        logger.error(f"Unexpected error: {e}")

if __name__ == '__main__':
    main()
