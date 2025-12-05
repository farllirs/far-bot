from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from backend.database import DatabaseManager
from backend.commands.simple_builder import SimpleCommandBuilder
from backend.commands.advanced_builder import AdvancedCommandBuilder, CommandTemplate

class CommandManager:
    """Manage all bot commands with improved error handling and validation"""
    
    def __init__(self, db: DatabaseManager):
        self.db = db
        self.simple_builder = SimpleCommandBuilder()
        self.advanced_builder = AdvancedCommandBuilder()
    
    def create_command(self, bot_id: str, command_data: Dict[str, Any]) -> Tuple[bool, str]:
        """Create a command (simple or advanced) with unified interface"""
        cmd_type = command_data.get('type', 'simple')
        trigger = command_data.get('trigger', command_data.get('id', ''))
        description = command_data.get('description', '')
        
        if cmd_type == 'simple':
            response = command_data.get('response', '')
            return self.create_simple_command(bot_id, trigger, response, description)
        else:
            code = command_data.get('code', '')
            return self.create_advanced_command(bot_id, trigger, code, description)
    
    def create_simple_command(self, bot_id: str, trigger: str, response: str, 
                            description: str = "") -> Tuple[bool, str]:
        """Create a simple response command"""
        # Validate trigger
        valid, msg = SimpleCommandBuilder.validate_trigger(trigger)
        if not valid:
            return False, msg
        
        # Validate response
        valid, msg = SimpleCommandBuilder.validate_response(response)
        if not valid:
            return False, msg
        
        # Create command data
        cmd_data = SimpleCommandBuilder.create_command(trigger, response, description)
        
        # Check if command already exists
        existing = self.db.get_commands(bot_id)
        if trigger in existing:
            return False, f"El comando '{trigger}' ya existe. Usa actualizar en su lugar."
        
        # Save to database
        if self.db.add_command(bot_id, trigger, cmd_data):
            return True, f"Comando '{trigger}' creado exitosamente"
        return False, "Error al guardar el comando en la base de datos"
    
    def create_advanced_command(self, bot_id: str, name: str, code: str, 
                               description: str = "") -> Tuple[bool, str]:
        """Create an advanced Python command"""
        # Validate code
        valid, msg = AdvancedCommandBuilder.validate_command(code)
        if not valid:
            return False, msg
        
        # Create command data
        cmd_data = AdvancedCommandBuilder.create_command(code, description, name)
        
        # Check if command already exists
        existing = self.db.get_commands(bot_id)
        if name in existing:
            return False, f"El comando '{name}' ya existe. Usa actualizar en su lugar."
        
        # Save to database
        if self.db.add_command(bot_id, name, cmd_data):
            return True, f"Comando avanzado '{name}' creado exitosamente"
        return False, "Error al guardar el comando en la base de datos"
    
    def get_command(self, bot_id: str, command_id: str) -> Optional[Dict[str, Any]]:
        """Get a specific command by ID"""
        commands = self.db.get_commands(bot_id)
        return commands.get(command_id)
    
    def list_commands(self, bot_id: str) -> Dict[str, Any]:
        """List all commands for a bot"""
        return self.db.get_commands(bot_id)
    
    def update_command(self, bot_id: str, command_id: str, updates: Dict[str, Any]) -> Tuple[bool, str]:
        """Update an existing command"""
        # Get existing command
        existing = self.get_command(bot_id, command_id)
        if not existing:
            return False, f"Comando '{command_id}' no encontrado"
        
        cmd_type = updates.get('type', existing.get('type', 'simple'))
        
        # Validate based on type
        if cmd_type == 'simple':
            response = updates.get('response', existing.get('response', ''))
            valid, msg = SimpleCommandBuilder.validate_response(response)
            if not valid:
                return False, msg
        else:
            code = updates.get('code', existing.get('code', ''))
            valid, msg = AdvancedCommandBuilder.validate_command(code)
            if not valid:
                return False, msg
        
        # Add updated timestamp
        updates['updated_at'] = datetime.now().isoformat()
        
        # Update in database
        if self.db.update_command(bot_id, command_id, updates):
            return True, f"Comando '{command_id}' actualizado exitosamente"
        return False, "Error al actualizar el comando"
    
    def delete_command(self, bot_id: str, command_id: str) -> Tuple[bool, str]:
        """Delete a command"""
        # Check if exists
        if not self.get_command(bot_id, command_id):
            return False, f"Comando '{command_id}' no encontrado"
        
        if self.db.delete_command(bot_id, command_id):
            return True, f"Comando '{command_id}' eliminado exitosamente"
        return False, "Error al eliminar el comando"
    
    def toggle_command(self, bot_id: str, command_id: str) -> Tuple[bool, str]:
        """Toggle command enabled/disabled state"""
        cmd = self.get_command(bot_id, command_id)
        if not cmd:
            return False, f"Comando '{command_id}' no encontrado"
        
        new_state = not cmd.get('enabled', True)
        return self.update_command(bot_id, command_id, {'enabled': new_state})
    
    def preview_simple_command(self, response: str, context: Dict[str, str] = None) -> str:
        """Preview a simple command output with sample data"""
        return SimpleCommandBuilder.preview_command(response, context)
    
    def get_templates(self) -> Dict[str, Any]:
        """Get all command templates"""
        return CommandTemplate.list_all_templates()
    
    def get_template_categories(self) -> Dict[str, List[str]]:
        """Get templates organized by category"""
        return CommandTemplate.get_template_categories()
    
    def get_command_stats(self, bot_id: str) -> Dict[str, Any]:
        """Get statistics about commands for a bot"""
        commands = self.list_commands(bot_id)
        
        simple_count = sum(1 for c in commands.values() if c.get('type') == 'simple')
        advanced_count = sum(1 for c in commands.values() if c.get('type') == 'advanced')
        enabled_count = sum(1 for c in commands.values() if c.get('enabled', True))
        total_usage = sum(c.get('usage_count', 0) for c in commands.values())
        
        return {
            'total': len(commands),
            'simple': simple_count,
            'advanced': advanced_count,
            'enabled': enabled_count,
            'disabled': len(commands) - enabled_count,
            'total_usage': total_usage
        }
    
    def increment_usage(self, bot_id: str, command_id: str) -> bool:
        """Increment usage counter for a command"""
        cmd = self.get_command(bot_id, command_id)
        if cmd:
            usage = cmd.get('usage_count', 0) + 1
            self.db.update_command(bot_id, command_id, {'usage_count': usage})
            return True
        return False
    
    def export_commands(self, bot_id: str) -> Dict[str, Any]:
        """Export all commands for backup"""
        commands = self.list_commands(bot_id)
        return {
            'bot_id': bot_id,
            'exported_at': datetime.now().isoformat(),
            'commands': commands
        }
    
    def import_commands(self, bot_id: str, data: Dict[str, Any], overwrite: bool = False) -> Tuple[bool, str]:
        """Import commands from backup"""
        commands = data.get('commands', {})
        imported = 0
        skipped = 0
        
        for cmd_id, cmd_data in commands.items():
            existing = self.get_command(bot_id, cmd_id)
            
            if existing and not overwrite:
                skipped += 1
                continue
            
            if existing:
                self.db.update_command(bot_id, cmd_id, cmd_data)
            else:
                self.db.add_command(bot_id, cmd_id, cmd_data)
            imported += 1
        
        return True, f"Importados: {imported}, Omitidos: {skipped}"
