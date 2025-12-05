#!/usr/bin/env python3
"""
Far-Bot Launcher - Start the bot manager and web panel
Run on Windows, Linux, macOS, or Android (Termux)
"""

import os
import sys
import platform
import asyncio
import threading
import webbrowser
from pathlib import Path
from datetime import datetime

VERSION = "2.0.1"

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print Far-Bot header"""
    header = f"""
    ███████╗ █████╗ ██████╗        ██████╗  ██████╗ ████████╗
    ██╔════╝██╔══██╗██╔══██╗       ██╔══██╗██╔═══██╗╚══██╔══╝
    █████╗  ███████║██████╔╝       ██████╔╝██║   ██║   ██║
    ██╔══╝  ██╔══██║██╔══██╗       ██╔══██╗██║   ██║   ██║
    ██║     ██║  ██║██║  ██║       ██████╔╝╚██████╔╝   ██║
    ╚═╝     ╚═╝  ╚═╝╚═╝  ╚═╝       ╚═════╝  ╚═════╝    ╚═╝

    Discord Bot Manager v{VERSION}
    """
    print(header)

def check_dependencies():
    """Check if all dependencies are installed"""
    required = {
        'discord': 'discord.py',
        'flask': 'flask',
        'flask_cors': 'flask-cors'
    }
    
    missing = []
    for module, package in required.items():
        try:
            __import__(module)
        except ImportError:
            missing.append(package)
    
    return missing

def print_system_info():
    """Print system information"""
    system = platform.system()
    is_termux = os.path.exists('/data/data/com.termux')
    
    print(f"\n[*] System: {system}")
    if is_termux:
        print("[*] Environment: Termux (Android)")
    print(f"[*] Python: {sys.version.split()[0]}")
    print(f"[*] Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")

def check_database():
    """Check if database exists"""
    db_path = Path("data")
    if not db_path.exists():
        print("\n[!] Database directory not found")
        print("[*] Creating data directory...")
        db_path.mkdir(exist_ok=True)
    
    # Check files
    bots_file = db_path / "bots.json"
    commands_file = db_path / "commands.json"
    
    if not bots_file.exists():
        bots_file.write_text('{}')
        print("[✓] Created: data/bots.json")
    
    if not commands_file.exists():
        commands_file.write_text('{}')
        print("[✓] Created: data/commands.json")

def load_modules():
    """Load Far-Bot modules"""
    try:
        print("\n[*] Loading Far-Bot modules...")
        from backend.database import DatabaseManager
        from backend.bot_manager import BotManager
        from backend.api_server import APIServer
        from backend.logger import FarBotLogger
        
        print("[✓] All modules loaded successfully")
        return DatabaseManager, BotManager, APIServer, FarBotLogger
    except ImportError as e:
        print(f"[✗] Failed to load modules: {e}")
        print("[!] Make sure all dependencies are installed")
        print("    Run: pip install discord.py flask flask-cors")
        return None

def open_browser(url, delay=2):
    """Open browser with delay"""
    threading.Timer(delay, webbrowser.open, args=[url]).start()

def main():
    """Main launcher function"""
    clear_screen()
    print_header()
    
    # Check dependencies
    print("[*] Checking dependencies...")
    missing = check_dependencies()
    if missing:
        print(f"[✗] Missing packages: {', '.join(missing)}")
        print("[!] Install them with: pip install " + " ".join(missing))
        sys.exit(1)
    print("[✓] All dependencies found")
    
    # Print system info
    print_system_info()
    
    # Check database
    check_database()
    
    # Load modules
    modules = load_modules()
    if not modules:
        sys.exit(1)
    
    DatabaseManager, BotManager, APIServer, FarBotLogger = modules
    
    # Initialize components
    print("\n[*] Initializing Far-Bot...")
    db = DatabaseManager(db_path="data")
    bot_manager = BotManager(db)
    logger = FarBotLogger(log_dir="logs")
    api_server = APIServer(db, bot_manager, port=5000)
    
    print("[✓] Initialization complete")
    
    # Print startup info
    print("\n" + "="*50)
    print("FAR-BOT IS STARTING")
    print("="*50)
    url = "http://localhost:5000"
    print(f"\n[*] Web Panel: {url}")
    print("[*] Opening browser...")
    print("[*] Press Ctrl+C to stop\n")
    
    # Open browser
    open_browser(url, delay=1)
    
    # Start server
    logger.info("Far-Bot launched successfully")
    try:
        api_server.run(debug=False)
    except KeyboardInterrupt:
        print("\n\n[*] Shutting down Far-Bot...")
        logger.info("Far-Bot shutdown")
        print("[✓] Goodbye!")
        sys.exit(0)
    except Exception as e:
        print(f"\n[✗] Error: {e}")
        logger.error(f"Fatal error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
