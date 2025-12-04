#!/bin/bash
# Far-Bot Launcher for Linux/macOS/Termux

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}"
echo "╔════════════════════════════════╗"
echo "║       Far-Bot Launcher          │"
echo "║  Discord Bot Manager v1.0.0     │"
echo "╚════════════════════════════════╝${NC}"

# Check Python
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 not found${NC}"
    echo "Install Python 3 and try again"
    exit 1
fi

PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
echo -e "${GREEN}✓${NC} Python $PYTHON_VERSION found"

# Run installer if needed
if [ ! -d "data" ]; then
    echo -e "${YELLOW}First run detected, running installer...${NC}"
    python3 installer.py
fi

# Run launcher
echo -e "\n${GREEN}Starting Far-Bot...${NC}\n"
python3 launcher.py
