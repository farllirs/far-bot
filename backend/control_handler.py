from typing import Dict, Any, Optional
from backend.database import DatabaseManager
from backend.bot_manager import BotManager
from backend.logger import FarBotLogger
from backend.commands.command_manager import CommandManager

class BotControlHandler:
    """Handle bot control operations"""
    
    def __init__(self, db: DatabaseManager, bot_manager: BotManager, logger: FarBotLogger):
        self.db = db
        self.bot_manager = bot_manager
        self.logger = logger
        self.command_manager = CommandManager(db)
    
    async def execute_action(self, action: str, bot_id: str, **kwargs) -> Dict[str, Any]:
        """Execute bot control action"""
        try:
            if action == "start":
                result = await self.bot_manager.start_bot(
                    bot_id, 
                    kwargs.get('token'),
                    kwargs.get('prefix', '!')
                )
            elif action == "stop":
                result = await self.bot_manager.stop_bot(bot_id)
            elif action == "add_command":
                cmd_type = kwargs.get('type', 'simple')
                if cmd_type == 'simple':
                    success, msg = self.command_manager.create_simple_command(
                        bot_id,
                        kwargs.get('trigger'),
                        kwargs.get('response'),
                        kwargs.get('description', '')
                    )
                else:
                    success, msg = self.command_manager.create_advanced_command(
                        bot_id,
                        kwargs.get('name'),
                        kwargs.get('code'),
                        kwargs.get('description', '')
                    )
                result = {"success": success, "message": msg}
            elif action == "remove_command":
                success, msg = self.command_manager.delete_command(
                    bot_id,
                    kwargs.get('command_id')
                )
                result = {"success": success, "message": msg}
            elif action == "get_status":
                bot_info = self.db.get_bot(bot_id)
                is_running = self.bot_manager.is_bot_running(bot_id)
                result = {
                    "success": True,
                    "bot": bot_info,
                    "is_running": is_running,
                    "commands": len(self.db.get_commands(bot_id))
                }
            else:
                result = {"success": False, "error": f"Unknown action: {action}"}
            
            # Log action
            if result.get('success'):
                self.logger.success(f"Action '{action}' completed", bot_id)
            else:
                self.logger.error(f"Action '{action}' failed: {result.get('error', 'Unknown error')}", bot_id)
            
            return result
        except Exception as e:
            self.logger.error(f"Error executing action '{action}': {str(e)}", bot_id)
            return {"success": False, "error": str(e)}
