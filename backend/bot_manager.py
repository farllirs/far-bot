import asyncio
import os
import sys
from typing import Dict, Optional, Callable
import discord
from discord.ext import commands
from backend.database import DatabaseManager
from backend.command_executor import CommandExecutor, BotInstance
import threading
import time

VERSION = "2.0.0"

class BotManager:
    """Manages Discord bot instances - v2.0.0"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.active_bots: Dict[str, BotInstance] = {}
        self.bot_tasks: Dict[str, asyncio.Task] = {}
        self.bot_loops: Dict[str, asyncio.AbstractEventLoop] = {}
        self.bot_threads: Dict[str, threading.Thread] = {}
        self.callbacks: Dict[str, list] = {
            "bot_started": [],
            "bot_stopped": [],
            "command_executed": [],
            "error": []
        }
        self.executor = CommandExecutor()
    
    def register_callback(self, event: str, callback: Callable):
        """Register a callback for an event"""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
    
    async def _trigger_callbacks(self, event: str, data: Dict = None):
        """Trigger all callbacks for an event"""
        for callback in self.callbacks.get(event, []):
            try:
                if asyncio.iscoroutinefunction(callback):
                    await callback(data or {})
                else:
                    callback(data or {})
            except Exception as e:
                print(f"[BotManager] Callback error: {e}")
    
    def _run_bot_in_thread(self, bot_id: str, bot_instance: BotInstance):
        """Run bot in a separate thread with its own event loop"""
        try:
            loop = asyncio.new_event_loop()
            asyncio.set_event_loop(loop)
            self.bot_loops[bot_id] = loop
            
            print(f"[BotManager] Event loop created for {bot_id}")
            
            # Run the bot until it's stopped
            loop.run_until_complete(bot_instance.start())
        except asyncio.CancelledError:
            print(f"[BotManager] Bot {bot_id} cancelled")
        except Exception as e:
            print(f"[BotManager] Error in bot thread for {bot_id}: {e}")
            bot_instance.last_error = str(e)
        finally:
            # Clean up
            try:
                loop.close()
            except:
                pass
            if bot_id in self.bot_loops:
                del self.bot_loops[bot_id]
    
    def start_bot(self, bot_id: str, token: str, prefix: str = "!", status: str = "online") -> Dict:
        """Start a Discord bot (non-blocking)"""
        try:
            if bot_id in self.active_bots:
                return {"success": False, "error": "Bot already running"}
            
            if not token or len(token) < 10:
                return {"success": False, "error": "Invalid bot token"}
            
            print(f"[BotManager] Creating bot instance for {bot_id}")
            
            # Create bot instance
            bot_instance = BotInstance(bot_id, token, prefix)
            
            # Load commands from database
            commands_data = self.db.get_commands(bot_id)
            print(f"[BotManager] Loading {len(commands_data)} commands for {bot_id}")
            
            loaded = 0
            failed = 0
            for cmd_id, cmd_data in commands_data.items():
                if bot_instance.add_command(cmd_id, cmd_data):
                    loaded += 1
                else:
                    failed += 1
                    print(f"[BotManager] Failed to load command: {cmd_id}")
            
            print(f"[BotManager] Loaded {loaded} commands, {failed} failed")
            
            self.active_bots[bot_id] = bot_instance
            
            thread = threading.Thread(
                target=self._run_bot_in_thread,
                args=(bot_id, bot_instance),
                daemon=True
            )
            thread.start()
            self.bot_threads[bot_id] = thread
            
            # Update bot status and custom status in database
            self.db.update_bot(bot_id, {"status": "running", "custom_status": status})
            
            print(f"[BotManager] Bot {bot_id} started successfully")
            return {"success": True, "message": f"Bot {bot_id} started", "commands_loaded": loaded}
        except Exception as e:
            print(f"[BotManager] Error starting bot: {e}")
            if bot_id in self.active_bots:
                del self.active_bots[bot_id]
            return {"success": False, "error": str(e)}
    
    def stop_bot(self, bot_id: str) -> Dict:
        """Stop a Discord bot"""
        try:
            if bot_id not in self.active_bots:
                return {"success": False, "error": "Bot not running"}
            
            bot_instance = self.active_bots[bot_id]
            
            if bot_id in self.bot_loops:
                loop = self.bot_loops[bot_id]
                # Schedule the stop coroutine
                future = asyncio.run_coroutine_threadsafe(bot_instance.stop(), loop)
                try:
                    future.result(timeout=5)
                except Exception as e:
                    print(f"[BotManager] Error stopping bot gracefully: {e}")
            
            del self.active_bots[bot_id]
            
            # Update bot status
            self.db.update_bot(bot_id, {"status": "stopped"})
            
            print(f"[BotManager] Bot {bot_id} stopped")
            return {"success": True, "message": f"Bot {bot_id} stopped"}
        except Exception as e:
            print(f"[BotManager] Error stopping bot: {e}")
            # Force remove if graceful stop fails
            if bot_id in self.active_bots:
                del self.active_bots[bot_id]
            return {"success": True, "message": f"Bot {bot_id} stopped (forced)"}
    
    def reload_commands(self, bot_id: str) -> Dict:
        """Reload commands for a running bot"""
        try:
            if bot_id not in self.active_bots:
                return {"success": False, "error": "Bot not running"}
            
            bot_instance = self.active_bots[bot_id]
            commands_data = self.db.get_commands(bot_id)
            
            print(f"[BotManager] Reloading {len(commands_data)} commands for {bot_id}")
            
            # Reload commands
            bot_instance.reload_commands(commands_data)
            
            return {"success": True, "message": f"Commands reloaded for {bot_id}"}
        except Exception as e:
            print(f"[BotManager] Error reloading commands: {e}")
            return {"success": False, "error": str(e)}
    
    def is_bot_running(self, bot_id: str) -> bool:
        """Check if a bot is running"""
        return bot_id in self.active_bots
    
    def get_bot_info(self, bot_id: str) -> Optional[Dict]:
        """Get information about a running bot"""
        if bot_id not in self.active_bots:
            return None
        
        bot_instance = self.active_bots[bot_id]
        
        # Get avatar URL
        avatar_url = None
        if bot_instance.bot.user and bot_instance.bot.user.avatar:
            avatar_url = str(bot_instance.bot.user.avatar.url)
        
        return {
            "id": bot_id,
            "is_running": bot_instance.is_running,
            "is_ready": bot_instance.is_ready,
            "prefix": bot_instance.prefix,
            "user": str(bot_instance.bot.user) if bot_instance.bot.user else "Not ready",
            "avatar_url": avatar_url,
            "last_error": bot_instance.last_error,
            "commands_count": len(bot_instance.builder.registered_commands),
            "slash_commands_count": len(bot_instance.builder.registered_slash_commands),
            "guilds": bot_instance.guilds_info
        }
    
    def get_all_bots_info(self) -> Dict[str, Dict]:
        """Get information about all running bots"""
        result = {}
        for bot_id in self.active_bots:
            info = self.get_bot_info(bot_id)
            if info:
                result[bot_id] = info
        return result
