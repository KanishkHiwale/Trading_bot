"""
Logging configuration for the trading bot
"""
import logging
import os
from datetime import datetime


def setup_logging(log_dir: str = 'logs', log_level: int = logging.INFO) -> None:
    """
    Configure logging for the application
    
    Args:
        log_dir: Directory to store log files
        log_level: Logging level (default: INFO)
    """
    # Create logs directory if it doesn't exist
    if not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Generate log filename with timestamp
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    log_file = os.path.join(log_dir, f'trading_bot_{timestamp}.log')
    
    # Configure logging format
    log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    date_format = '%Y-%m-%d %H:%M:%S'
    
    # Create formatters
    formatter = logging.Formatter(log_format, date_format)
    
    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(log_level)
    file_handler.setFormatter(formatter)
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_formatter = logging.Formatter('%(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)
    
    # Configure root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Log startup message
    logging.info("="*60)
    logging.info("Trading Bot Started")
    logging.info(f"Log file: {log_file}")
    logging.info("="*60)
    
    return log_file
