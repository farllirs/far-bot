from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import os
from pathlib import Path
from backend.database import DatabaseManager
from backend.bot_manager import BotManager
from backend.automod import AutoModManager
from backend.utils.validators import Validator

VERSION = "2.0.0"

class APIServer:
    """Flask API server for Far-Bot v2.0.0"""
    
    def __init__(self, db: DatabaseManager, bot_manager: BotManager, port: int = 5000):
        self.panel_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'panel'))
        self.app = Flask(__name__, 
                        static_folder=os.path.join(self.panel_path, 'assets'),
                        static_url_path='/assets')
        CORS(self.app)
        self.db = db
        self.bot_manager = bot_manager
        self.automod = AutoModManager()
        self.port = port
        self._setup_routes()
    
    def _setup_routes(self):
        """Setup Flask routes"""
        
        # ==================== STATIC FILES ====================
        @self.app.route('/')
        def serve_index():
            return send_from_directory(self.panel_path, 'index.html')
        
        @self.app.route('/assets/<path:path>')
        def serve_assets(path):
            assets_path = os.path.join(self.panel_path, 'assets')
            try:
                return send_from_directory(assets_path, path)
            except Exception as e:
                print(f"[API] Error serving asset {path}: {e}")
                return jsonify({"error": "File not found"}), 404
        
        @self.app.route('/command-editor.html')
        def serve_command_editor():
            return send_from_directory(self.panel_path, 'command-editor.html')
        
        @self.app.route('/automod.html')
        def serve_automod():
            return send_from_directory(self.panel_path, 'automod.html')
        
        @self.app.route('/<path:path>')
        def serve_static(path):
            try:
                return send_from_directory(self.panel_path, path)
            except Exception as e:
                print(f"[API] Error serving file {path}: {e}")
                return jsonify({"error": "File not found"}), 404
        
        @self.app.route('/docs/<path:path>')
        def serve_docs(path):
            docs_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'docs'))
            try:
                return send_from_directory(docs_path, path)
            except Exception as e:
                print(f"[API] Error serving doc {path}: {e}")
                return jsonify({"error": "File not found"}), 404
        
        # ==================== BOT ENDPOINTS ====================
        @self.app.route('/api/bots', methods=['GET'])
        def get_bots():
            bots = self.db.get_all_bots()
            for bot_id in bots:
                bots[bot_id]['is_running'] = self.bot_manager.is_bot_running(bot_id)
                commands = self.db.get_commands(bot_id)
                bots[bot_id]['command_count'] = len(commands) if commands else 0
                
                bot_info = self.bot_manager.get_bot_info(bot_id)
                if bot_info:
                    bots[bot_id]['guilds'] = bot_info.get('guilds', [])
                    bots[bot_id]['servers'] = len(bot_info.get('guilds', []))
                    bots[bot_id]['discord_user'] = bot_info.get('user', '')
                    bots[bot_id]['avatar_url'] = bot_info.get('avatar_url', '')
            
            return jsonify(bots)
        
        @self.app.route('/api/bots/<bot_id>', methods=['GET'])
        def get_bot(bot_id):
            bot = self.db.get_bot(bot_id)
            if bot:
                bot['is_running'] = self.bot_manager.is_bot_running(bot_id)
                commands = self.db.get_commands(bot_id)
                bot['command_count'] = len(commands) if commands else 0
                return jsonify(bot)
            return jsonify({"error": "Bot not found"}), 404
        
        @self.app.route('/api/bots', methods=['POST'])
        def create_bot():
            data = request.json
            
            valid, msg = Validator.validate_token(data.get('token', ''))
            if not valid:
                print(f"[API] Token validation failed: {msg}")
                return jsonify({"error": msg}), 400
            
            valid, msg = Validator.validate_prefix(data.get('prefix', '!'))
            if not valid:
                print(f"[API] Prefix validation failed: {msg}")
                return jsonify({"error": msg}), 400
            
            bot_id = data.get('name', '').lower().replace(' ', '_')
            if not bot_id:
                return jsonify({"error": "Bot name required"}), 400
            
            existing = self.db.get_bot(bot_id)
            if existing:
                return jsonify({"error": "Bot with this name already exists"}), 400
            
            bot_data = {
                "name": data.get('name'),
                "token": data.get('token'),
                "prefix": data.get('prefix', '!'),
                "client_id": data.get('client_id', ''),
                "description": data.get('description', ''),
                "custom_status": "online",
                "status": "stopped"
            }
            
            if self.db.add_bot(bot_id, bot_data):
                print(f"[API] Bot {bot_id} created successfully")
                return jsonify({"success": True, "bot_id": bot_id}), 201
            return jsonify({"error": "Failed to create bot"}), 500
        
        @self.app.route('/api/bots/<bot_id>', methods=['PUT'])
        def update_bot(bot_id):
            data = request.json
            if self.db.update_bot(bot_id, data):
                return jsonify({"success": True})
            return jsonify({"error": "Failed to update bot"}), 500
        
        @self.app.route('/api/bots/<bot_id>', methods=['DELETE'])
        def delete_bot(bot_id):
            if self.bot_manager.is_bot_running(bot_id):
                self.bot_manager.stop_bot(bot_id)
            
            if self.db.delete_bot(bot_id):
                return jsonify({"success": True})
            return jsonify({"error": "Failed to delete bot"}), 500
        
        @self.app.route('/api/bots/<bot_id>/start', methods=['POST'])
        def start_bot(bot_id):
            bot = self.db.get_bot(bot_id)
            if not bot:
                return jsonify({"error": "Bot not found"}), 404
            
            data = request.json or {}
            status = data.get('status', 'online')
            
            print(f"[API] Start request for bot {bot_id} with status {status}")
            
            result = self.bot_manager.start_bot(
                bot_id, 
                bot['token'], 
                bot.get('prefix', '!'),
                status
            )
            
            print(f"[API] Bot start result: {result}")
            
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
        
        @self.app.route('/api/bots/<bot_id>/stop', methods=['POST'])
        def stop_bot(bot_id):
            result = self.bot_manager.stop_bot(bot_id)
            if result.get('success'):
                return jsonify(result), 200
            else:
                return jsonify(result), 400
        
        @self.app.route('/api/bots/<bot_id>/restart', methods=['POST'])
        def restart_bot(bot_id):
            bot = self.db.get_bot(bot_id)
            if not bot:
                return jsonify({"error": "Bot not found"}), 404
            
            if self.bot_manager.is_bot_running(bot_id):
                self.bot_manager.stop_bot(bot_id)
                import time
                time.sleep(1)
            
            result = self.bot_manager.start_bot(
                bot_id,
                bot['token'],
                bot.get('prefix', '!'),
                bot.get('custom_status', 'online')
            )
            
            if result.get('success'):
                return jsonify({"success": True, "message": f"Bot {bot_id} restarted"}), 200
            return jsonify(result), 400
        
        @self.app.route('/api/bots/<bot_id>/sync', methods=['POST'])
        def sync_commands(bot_id):
            """Sync slash commands with Discord"""
            result = self.bot_manager.sync_slash_commands(bot_id)
            if result.get('success'):
                return jsonify(result), 200
            return jsonify(result), 400
        
        # ==================== COMMAND ENDPOINTS ====================
        @self.app.route('/api/bots/<bot_id>/commands', methods=['GET'])
        def get_commands(bot_id):
            return jsonify(self.db.get_commands(bot_id))
        
        @self.app.route('/api/bots/<bot_id>/commands', methods=['POST'])
        def add_command(bot_id):
            data = request.json
            
            cmd_id = data.get('id', data.get('trigger', '')).lower().replace(' ', '_')
            
            if not cmd_id:
                return jsonify({"error": "Command ID/trigger required"}), 400
            
            valid, msg = Validator.validate_command_name(cmd_id)
            if not valid:
                return jsonify({"error": msg}), 400
            
            cmd_type = data.get('type', 'simple')
            
            if cmd_type == 'advanced' or cmd_type == 'slash':
                code = data.get('code', '')
                if not code:
                    return jsonify({"error": "Code is required for advanced/slash commands"}), 400
                valid, msg = Validator.validate_python_code(code)
                if not valid:
                    return jsonify({"error": msg}), 400
            else:
                response = data.get('response', '')
                if not response:
                    return jsonify({"error": "Response is required for simple commands"}), 400
            
            command_data = {
                "id": cmd_id,
                "type": cmd_type,
                "trigger": data.get('trigger', cmd_id),
                "response": data.get('response', ''),
                "code": data.get('code', ''),
                "description": data.get('description', ''),
                "enabled": data.get('enabled', True)
            }
            
            if self.db.add_command(bot_id, cmd_id, command_data):
                if self.bot_manager.is_bot_running(bot_id):
                    print(f"[API] Bot is running, triggering command reload for {bot_id}")
                    self.bot_manager.reload_commands(bot_id)
                
                return jsonify({"success": True, "command_id": cmd_id}), 201
            return jsonify({"error": "Failed to add command"}), 500
        
        @self.app.route('/api/bots/<bot_id>/commands/<cmd_id>', methods=['PUT'])
        def update_command(bot_id, cmd_id):
            data = request.json
            
            if (data.get('type') == 'advanced' or data.get('type') == 'slash') and data.get('code'):
                valid, msg = Validator.validate_python_code(data.get('code', ''))
                if not valid:
                    return jsonify({"error": msg}), 400
            
            if self.db.update_command(bot_id, cmd_id, data):
                if self.bot_manager.is_bot_running(bot_id):
                    self.bot_manager.reload_commands(bot_id)
                return jsonify({"success": True})
            return jsonify({"error": "Failed to update command"}), 500
        
        @self.app.route('/api/bots/<bot_id>/commands/<cmd_id>', methods=['DELETE'])
        def delete_command(bot_id, cmd_id):
            if self.db.delete_command(bot_id, cmd_id):
                if self.bot_manager.is_bot_running(bot_id):
                    self.bot_manager.reload_commands(bot_id)
                return jsonify({"success": True})
            return jsonify({"error": "Failed to delete command"}), 500
        
        @self.app.route('/api/bots/<bot_id>/commands/bulk', methods=['POST'])
        def bulk_add_commands(bot_id):
            data = request.json
            commands = data.get('commands', [])
            
            added = 0
            errors = []
            
            for cmd in commands:
                cmd_id = cmd.get('id', cmd.get('trigger', '')).lower().replace(' ', '_')
                if cmd_id:
                    if self.db.add_command(bot_id, cmd_id, cmd):
                        added += 1
                    else:
                        errors.append(cmd_id)
            
            if self.bot_manager.is_bot_running(bot_id):
                self.bot_manager.reload_commands(bot_id)
            
            return jsonify({
                "success": True,
                "added": added,
                "errors": errors
            }), 201
        
        # ==================== AUTOMOD ENDPOINTS ====================
        @self.app.route('/api/bots/<bot_id>/automod/<guild_id>', methods=['GET'])
        def get_automod_config(bot_id, guild_id):
            config = self.automod.get_config(bot_id, guild_id)
            return jsonify(config)
        
        @self.app.route('/api/bots/<bot_id>/automod/<guild_id>', methods=['PUT'])
        def update_automod_config(bot_id, guild_id):
            data = request.json
            if self.automod.save_config(bot_id, guild_id, data):
                return jsonify({"success": True})
            return jsonify({"error": "Failed to save config"}), 500
        
        @self.app.route('/api/bots/<bot_id>/automod/<guild_id>/<section>', methods=['PUT'])
        def update_automod_section(bot_id, guild_id, section):
            data = request.json
            if self.automod.update_config(bot_id, guild_id, section, data):
                return jsonify({"success": True})
            return jsonify({"error": "Failed to save config"}), 500
        
        @self.app.route('/api/bots/<bot_id>/automod', methods=['GET'])
        def get_all_automod_configs(bot_id):
            configs = self.automod.get_all_configs(bot_id)
            return jsonify(configs)
        
        @self.app.route('/api/automod/templates', methods=['GET'])
        def get_automod_templates():
            return jsonify(self.automod.get_templates())
        
        @self.app.route('/api/automod/variables', methods=['GET'])
        def get_automod_variables():
            return jsonify(self.automod.get_variables())
        
        # ==================== HEALTH CHECK ====================
        @self.app.route('/api/health', methods=['GET'])
        def health():
            return jsonify({
                "status": "healthy",
                "bots_running": len([b for b in self.bot_manager.active_bots if self.bot_manager.is_bot_running(b)])
            })
        
        @self.app.route('/api/version', methods=['GET'])
        def get_version():
            return jsonify({"version": VERSION, "name": "Far-Bot"})
    
    def run(self, debug: bool = False):
        """Run the Flask server"""
        self.app.run(host='0.0.0.0', port=self.port, debug=debug)
