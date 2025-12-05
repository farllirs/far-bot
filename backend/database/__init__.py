import json
import os
from pathlib import Path
from typing import Any, Dict, List, Optional

class DatabaseManager:
    """Local JSON-based database manager for Far-Bot data"""
    
    def __init__(self, db_path: str = "data"):
        self.db_path = Path(db_path)
        self.db_path.mkdir(exist_ok=True)
        self.bots_file = self.db_path / "bots.json"
        self.commands_file = self.db_path / "commands.json"
        self.config_file = self.db_path / "config.json"
        self._initialize_files()
    
    def _initialize_files(self):
        """Initialize database files if they don't exist"""
        if not self.bots_file.exists():
            self._save_json(self.bots_file, {})
        if not self.commands_file.exists():
            self._save_json(self.commands_file, {})
        if not self.config_file.exists():
            self._save_json(self.config_file, {"version": "1.0.0"})
    
    def _load_json(self, file_path: Path) -> Dict[str, Any]:
        """Load JSON from file"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            return {}
    
    def _save_json(self, file_path: Path, data: Dict[str, Any]):
        """Save JSON to file"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=2)
    
    # BOT MANAGEMENT
    def add_bot(self, bot_id: str, bot_data: Dict[str, Any]) -> bool:
        """Add a new bot"""
        try:
            bots = self._load_json(self.bots_file)
            bots[bot_id] = {
                **bot_data,
                "created_at": str(Path.cwd()),
                "status": "stopped",
                "stats": {"commands_run": 0, "errors": 0}
            }
            self._save_json(self.bots_file, bots)
            return True
        except Exception as e:
            print(f"[DB] Error adding bot: {e}")
            return False
    
    def get_bot(self, bot_id: str) -> Optional[Dict[str, Any]]:
        """Get bot by ID"""
        bots = self._load_json(self.bots_file)
        return bots.get(bot_id)
    
    def get_all_bots(self) -> Dict[str, Any]:
        """Get all bots"""
        return self._load_json(self.bots_file)
    
    def update_bot(self, bot_id: str, updates: Dict[str, Any]) -> bool:
        """Update bot configuration"""
        try:
            bots = self._load_json(self.bots_file)
            if bot_id in bots:
                bots[bot_id].update(updates)
                self._save_json(self.bots_file, bots)
                return True
            return False
        except Exception as e:
            print(f"[DB] Error updating bot: {e}")
            return False
    
    def delete_bot(self, bot_id: str) -> bool:
        """Delete a bot"""
        try:
            bots = self._load_json(self.bots_file)
            if bot_id in bots:
                del bots[bot_id]
                self._save_json(self.bots_file, bots)
                return True
            return False
        except Exception as e:
            print(f"[DB] Error deleting bot: {e}")
            return False
    
    # COMMAND MANAGEMENT
    def add_command(self, bot_id: str, command_id: str, command_data: Dict[str, Any]) -> bool:
        """Add a command to a bot"""
        try:
            commands = self._load_json(self.commands_file)
            if bot_id not in commands:
                commands[bot_id] = {}
            commands[bot_id][command_id] = command_data
            self._save_json(self.commands_file, commands)
            return True
        except Exception as e:
            print(f"[DB] Error adding command: {e}")
            return False
    
    def get_commands(self, bot_id: str) -> Dict[str, Any]:
        """Get all commands for a bot"""
        commands = self._load_json(self.commands_file)
        return commands.get(bot_id, {})
    
    def update_command(self, bot_id: str, command_id: str, updates: Dict[str, Any]) -> bool:
        """Update a command"""
        try:
            commands = self._load_json(self.commands_file)
            if bot_id in commands and command_id in commands[bot_id]:
                commands[bot_id][command_id].update(updates)
                self._save_json(self.commands_file, commands)
                return True
            return False
        except Exception as e:
            print(f"[DB] Error updating command: {e}")
            return False
    
    def delete_command(self, bot_id: str, command_id: str) -> bool:
        """Delete a command"""
        try:
            commands = self._load_json(self.commands_file)
            if bot_id in commands and command_id in commands[bot_id]:
                del commands[bot_id][command_id]
                self._save_json(self.commands_file, commands)
                return True
            return False
        except Exception as e:
            print(f"[DB] Error deleting command: {e}")
            return False
    
    # CONFIG MANAGEMENT
    def get_config(self) -> Dict[str, Any]:
        """Get global config"""
        return self._load_json(self.config_file)
    
    def update_config(self, updates: Dict[str, Any]) -> bool:
        """Update global config"""
        try:
            config = self._load_json(self.config_file)
            config.update(updates)
            self._save_json(self.config_file, config)
            return True
        except Exception as e:
            print(f"[DB] Error updating config: {e}")
            return False
