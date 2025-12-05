from datetime import datetime, timedelta
from typing import Dict, Any
from backend.database import DatabaseManager

class StatsTracker:
    """Track bot and command statistics"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.stats_file = db.db_path / "stats.json"
        if not self.stats_file.exists():
            db._save_json(self.stats_file, {})
    
    def increment_command_count(self, bot_id: str):
        """Increment command execution count"""
        stats = self.db._load_json(self.stats_file)
        if bot_id not in stats:
            stats[bot_id] = {"commands_run": 0, "errors": 0, "last_active": None}
        stats[bot_id]["commands_run"] += 1
        stats[bot_id]["last_active"] = datetime.now().isoformat()
        self.db._save_json(self.stats_file, stats)
    
    def increment_error_count(self, bot_id: str):
        """Increment error count"""
        stats = self.db._load_json(self.stats_file)
        if bot_id not in stats:
            stats[bot_id] = {"commands_run": 0, "errors": 0}
        stats[bot_id]["errors"] += 1
        self.db._save_json(self.stats_file, stats)
    
    def get_stats(self, bot_id: str) -> Dict[str, Any]:
        """Get bot statistics"""
        stats = self.db._load_json(self.stats_file)
        return stats.get(bot_id, {"commands_run": 0, "errors": 0})
    
    def get_all_stats(self) -> Dict[str, Any]:
        """Get all statistics"""
        return self.db._load_json(self.stats_file)
