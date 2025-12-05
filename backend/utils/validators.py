import re
from typing import Tuple

class Validator:
    """Validation utilities for bot configuration"""
    
    @staticmethod
    def validate_token(token: str) -> Tuple[bool, str]:
        """Validate Discord bot token format"""
        if not token or len(token) < 10:
            return False, "Invalid token: Token must be at least 10 characters"
        # Discord tokens vary significantly in length, just check minimum
        return True, "Valid token"
    
    @staticmethod
    def validate_prefix(prefix: str) -> Tuple[bool, str]:
        """Validate command prefix"""
        if not prefix or len(prefix) > 5:
            return False, "Prefix must be 1-5 characters"
        if prefix.isalnum() and len(prefix) > 1:
            return False, "Multi-character prefix must contain non-alphanumeric"
        return True, "Valid prefix"
    
    @staticmethod
    def validate_command_name(name: str) -> Tuple[bool, str]:
        """Validate command name"""
        if not name or len(name) > 32:
            return False, "Command name must be 1-32 characters"
        if not re.match(r'^[a-zA-Z0-9_]+$', name):
            return False, "Command name can only contain letters, numbers, and underscores"
        return True, "Valid command name"
    
    @staticmethod
    def validate_python_code(code: str) -> Tuple[bool, str]:
        """Validate Python code syntax"""
        try:
            compile(code, '<string>', 'exec')
            return True, "Valid Python code"
        except SyntaxError as e:
            return False, f"Syntax error: {str(e)}"

class Variables:
    """Built-in variables for simple commands"""
    
    AVAILABLE = {
        "$username": "User's Discord username",
        "$userid": "User's Discord ID",
        "$servername": "Server name",
        "$botname": "Bot's name",
        "$time": "Current time",
        "$mention": "Mentions the user"
    }
    
    @staticmethod
    def replace_variables(text: str, ctx_data: dict = None) -> str:
        """Replace variables in command response"""
        ctx_data = ctx_data or {}
        result = text
        for var, _ in Variables.AVAILABLE.items():
            if var in result:
                value = ctx_data.get(var, f"[{var}]")
                result = result.replace(var, str(value))
        return result
