#!/usr/bin/env python3
"""
Far-Bot Installer - Install dependencies and setup environment
Works on Windows, Linux, macOS, and Android (Termux)
"""

import os
import sys
import platform
import subprocess
from pathlib import Path

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def print_header():
    """Print installation header"""
    print("""
    ╔════════════════════════════════════════════╗
    ║     Far-Bot Installer v1.0.0              ║
    ║  Discord Bot Manager Setup Wizard          ║
    ║  Ready for Windows, Linux, macOS, Termux   ║
    ╚════════════════════════════════════════════╝
    """)

def detect_environment():
    """Detect the running environment"""
    system = platform.system()
    env_info = {
        'system': system,
        'python_version': sys.version.split()[0],
        'is_termux': os.path.exists('/data/data/com.termux')
    }
    
    if env_info['is_termux']:
        env_info['environment'] = 'Termux (Android)'
    elif system == 'Windows':
        env_info['environment'] = 'Windows'
    elif system == 'Darwin':
        env_info['environment'] = 'macOS'
    else:
        env_info['environment'] = 'Linux'
    
    return env_info

def run_command(cmd, description="", ignore_error=False):
    """Run a shell command and return success status"""
    try:
        print(f"  ➜ {description}...", end=" ", flush=True)
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✓")
            return True
        else:
            print("✗")
            if not ignore_error:
                print(f"    Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"✗\n    Exception: {e}")
        return False

def create_directories():
    """Create required project directories"""
    print("\n[1/4] Creating project structure...")
    directories = [
        "data",
        "logs",
        "backend/commands",
        "backend/utils",
        "panel/assets/css",
        "panel/assets/js"
    ]
    
    for directory in directories:
        Path(directory).mkdir(parents=True, exist_ok=True)
        print(f"  ✓ Created: {directory}")
    
    return True

def install_dependencies(env_info):
    """Install Python dependencies"""
    print("\n[2/4] Installing Python dependencies...")
    
    dependencies = [
        ("discord.py", "discord.py>=2.0.0"),
        ("flask", "flask>=2.0.0"),
        ("flask-cors", "flask-cors>=3.0.0")
    ]
    
    success_count = 0
    for pkg_name, pkg_spec in dependencies:
        if run_command(f"{sys.executable} -m pip install {pkg_spec}", f"Installing {pkg_name}", ignore_error=True):
            success_count += 1
    
    if success_count == len(dependencies):
        print(f"\n  All {len(dependencies)} dependencies installed successfully!")
        return True
    else:
        print(f"\n  Warning: Only {success_count}/{len(dependencies)} dependencies installed")
        print("  Some features may not work properly")
        return success_count > 0

def create_config():
    """Create default configuration file"""
    print("\n[3/4] Creating configuration...")
    
    config_content = """{
  "version": "1.0.0",
  "app_name": "Far-Bot",
  "port": 5000,
  "debug": false,
  "database": {
    "type": "json",
    "path": "data"
  },
  "discord": {
    "default_prefix": "!"
  },
  "logging": {
    "level": "info",
    "max_logs": 1000
  }
}
"""
    
    try:
        with open("config.json", "w") as f:
            f.write(config_content)
        print("  ✓ Configuration file created: config.json")
        return True
    except Exception as e:
        print(f"  ✗ Failed to create config: {e}")
        return False

def verify_installation():
    """Verify all dependencies are installed"""
    print("\n[4/4] Verifying installation...")
    
    required_packages = ['discord', 'flask', 'flask_cors']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {package} verified")
        except ImportError:
            print(f"  ✗ {package} not found")
            missing.append(package)
    
    return len(missing) == 0

def print_summary(env_info, success):
    """Print installation summary"""
    print("\n" + "="*50)
    print("INSTALLATION SUMMARY")
    print("="*50)
    print(f"\nEnvironment: {env_info['environment']}")
    print(f"Python: {env_info['python_version']}")
    print(f"System: {env_info['system']}")
    
    if success:
        print("\n✓ Installation completed successfully!")
        print("\nNEXT STEPS:")
        print("  1. Run: python launcher.py")
        print("  2. Open: http://localhost:5000")
        print("  3. Add your Discord bot token")
        print("  4. Start creating commands!")
    else:
        print("\n⚠ Installation completed with warnings")
        print("  Some dependencies may be missing")
        print("  Try running: python launcher.py")
        print("  If errors occur, manually install:")
        print("    pip install discord.py flask flask-cors")

def main():
    """Main installer function"""
    clear_screen()
    print_header()
    
    # Detect environment
    env_info = detect_environment()
    print(f"\nDetected: {env_info['environment']}")
    print(f"Python Version: {env_info['python_version']}")
    
    # Create directories
    if not create_directories():
        print("Failed to create directories")
        sys.exit(1)
    
    # Install dependencies
    deps_ok = install_dependencies(env_info)
    
    # Create config
    config_ok = create_config()
    
    # Verify installation
    verify_ok = verify_installation()
    
    # Print summary
    success = deps_ok and config_ok and verify_ok
    print_summary(env_info, success)
    
    print("\n" + "="*50)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\nInstallation cancelled by user")
        sys.exit(0)
    except Exception as e:
        print(f"\nFatal error: {e}")
        sys.exit(1)
