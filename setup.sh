#!/bin/bash
# GhostLink v2.0 - Setup and Run Script
# This script automates the setup and running of GhostLink

set -e

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Banner
echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║         GhostLink v2.0 - Setup & Run Script           ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version | awk '{print $2}')
echo -e "${GREEN}✓ Python $PYTHON_VERSION found${NC}"

# Change to script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd "$SCRIPT_DIR"

# Function to show menu
show_menu() {
    echo -e "\n${BLUE}Choose an option:${NC}"
    echo "1) Install dependencies"
    echo "2) Start C2 Server"
    echo "3) Start Agent"
    echo "4) Run full setup (install deps + start both)"
    echo "5) Clean database and logs"
    echo "6) Test encoding"
    echo "7) Exit"
    echo -e "\nEnter your choice [1-7]: "
}

# Function to install dependencies
install_deps() {
    echo -e "\n${YELLOW}[*] Installing dependencies...${NC}"
    pip install -r requirements.txt -q
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ Dependencies installed successfully${NC}"
    else
        echo -e "${RED}✗ Failed to install dependencies${NC}"
        exit 1
    fi
}

# Function to verify installation
verify_install() {
    echo -e "\n${YELLOW}[*] Verifying installation...${NC}"
    python3 << 'EOF'
try:
    from flask import Flask
    from cryptography.fernet import Fernet
    import requests
    print("✓ All dependencies verified")
except ImportError as e:
    print(f"✗ Missing dependency: {e}")
    exit(1)
EOF
}

# Function to check port availability
check_port() {
    port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 1  # Port in use
    else
        return 0  # Port available
    fi
}

# Function to start server
start_server() {
    echo -e "\n${YELLOW}[*] Starting C2 Server...${NC}"
    
    if ! check_port 8888; then
        echo -e "${RED}✗ Port 8888 is already in use${NC}"
        echo "Killing existing process..."
        lsof -ti:8888 | xargs kill -9 2>/dev/null || true
        sleep 1
    fi
    
    echo -e "${GREEN}✓ Starting Listener.py on port 8888${NC}"
    echo "Press Ctrl+C to stop the server"
    python3 Listener.py
}

# Function to start agent
start_agent() {
    echo -e "\n${YELLOW}[*] Starting Agent...${NC}"
    echo -e "${GREEN}✓ Starting Implant.py${NC}"
    echo "Press Ctrl+C to stop the agent"
    python3 Implant.py
}

# Function to clean database and logs
clean_data() {
    echo -e "\n${YELLOW}[*] Cleaning database and logs...${NC}"
    
    if [ -f "ghostlink.db" ]; then
        rm ghostlink.db
        echo -e "${GREEN}✓ Database removed${NC}"
    fi
    
    if [ -f "server.log" ]; then
        rm server.log
        echo -e "${GREEN}✓ Server log removed${NC}"
    fi
    
    if [ -f "agent.log" ]; then
        rm agent.log
        echo -e "${GREEN}✓ Agent log removed${NC}"
    fi
    
    echo -e "${GREEN}✓ Cleanup complete${NC}"
}

# Function to test encoding
test_encoding() {
    echo -e "\n${YELLOW}[*] Testing encoding...${NC}"
    if [ -f "verify_encoding.py" ]; then
        python3 verify_encoding.py
    else
        echo -e "${RED}✗ verify_encoding.py not found${NC}"
    fi
}

# Function for full setup
full_setup() {
    echo -e "\n${YELLOW}[*] Running full setup...${NC}"
    install_deps
    verify_install
    echo -e "\n${GREEN}✓ Setup complete!${NC}"
    echo -e "${BLUE}To start the framework:${NC}"
    echo "  Terminal 1: python3 Listener.py"
    echo "  Terminal 2: python3 Implant.py"
    echo "  Terminal 3: python3 Controller.py"
}

# Main loop
while true; do
    show_menu
    read -r choice
    
    case $choice in
        1)
            install_deps
            verify_install
            ;;
        2)
            start_server
            ;;
        3)
            start_agent
            ;;
        4)
            full_setup
            ;;
        5)
            clean_data
            ;;
        6)
            test_encoding
            ;;
        7)
            echo -e "${GREEN}Goodbye!${NC}"
            exit 0
            ;;
        *)
            echo -e "${RED}Invalid option. Please try again.${NC}"
            ;;
    esac
done
