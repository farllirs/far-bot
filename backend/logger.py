import logging
import os
from datetime import datetime
from pathlib import Path
from typing import Optional

class FarBotLogger:
    """Logging system for Far-Bot"""
    
    LOG_LEVELS = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'critical': logging.CRITICAL
    }
    
    def __init__(self, log_dir: str = "logs"):
        self.log_dir = Path(log_dir)
        self.log_dir.mkdir(exist_ok=True)
        self.logs = []
        self._setup_logging()
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_file = self.log_dir / f"far-bot-{datetime.now().strftime('%Y-%m-%d')}.log"
        
        logging.basicConfig(
            level=logging.DEBUG,
            format='[%(asctime)s] [%(levelname)s] %(message)s',
            handlers=[
                logging.FileHandler(log_file),
                logging.StreamHandler()
            ]
        )
        
        self.logger = logging.getLogger('far-bot')
    
    def log(self, level: str, message: str, bot_id: Optional[str] = None):
        """Log a message"""
        timestamp = datetime.now().isoformat()
        log_entry = {
            'timestamp': timestamp,
            'level': level.upper(),
            'message': message,
            'bot_id': bot_id
        }
        
        self.logs.append(log_entry)
        
        # Keep last 1000 logs in memory
        if len(self.logs) > 1000:
            self.logs.pop(0)
        
        log_method = getattr(self.logger, level.lower(), self.logger.info)
        log_method(f"[{bot_id}]" if bot_id else "" + f" {message}")
    
    def debug(self, message: str, bot_id: Optional[str] = None):
        self.log('debug', message, bot_id)
    
    def info(self, message: str, bot_id: Optional[str] = None):
        self.log('info', message, bot_id)
    
    def warning(self, message: str, bot_id: Optional[str] = None):
        self.log('warning', message, bot_id)
    
    def error(self, message: str, bot_id: Optional[str] = None):
        self.log('error', message, bot_id)
    
    def critical(self, message: str, bot_id: Optional[str] = None):
        self.log('critical', message, bot_id)
    
    def success(self, message: str, bot_id: Optional[str] = None):
        """Log a success message"""
        self.log('success', message, bot_id)
    
    def get_logs(self, limit: int = 100, level: Optional[str] = None, 
                 bot_id: Optional[str] = None) -> list:
        """Get logs with optional filtering"""
        filtered = self.logs
        
        if level:
            filtered = [log for log in filtered if log['level'].lower() == level.lower()]
        
        if bot_id:
            filtered = [log for log in filtered if log['bot_id'] == bot_id]
        
        return filtered[-limit:]
    
    def clear_logs(self):
        """Clear in-memory logs"""
        self.logs = []
    
    def export_logs(self, filename: str = "logs_export.json") -> bool:
        """Export logs to JSON file"""
        try:
            import json
            export_file = self.log_dir / filename
            with open(export_file, 'w') as f:
                json.dump(self.logs, f, indent=2)
            return True
        except Exception as e:
            self.error(f"Failed to export logs: {e}")
            return False

class BotLogger:
    """Logger for individual bots"""
    
    def __init__(self, bot_id: str, main_logger: FarBotLogger):
        self.bot_id = bot_id
        self.main_logger = main_logger
    
    def log(self, level: str, message: str):
        """Log bot-specific message"""
        self.main_logger.log(level, message, self.bot_id)
    
    def debug(self, message: str):
        self.main_logger.debug(message, self.bot_id)
    
    def info(self, message: str):
        self.main_logger.info(message, self.bot_id)
    
    def warning(self, message: str):
        self.main_logger.warning(message, self.bot_id)
    
    def error(self, message: str):
        self.main_logger.error(message, self.bot_id)
    
    def success(self, message: str):
        self.main_logger.success(message, self.bot_id)
