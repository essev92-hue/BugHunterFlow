#!/bin/bash
# install.sh - Installation script for BugHunterFlow

echo "[+] Installing BugHunterFlow..."

# Check for git
if ! command -v git &> /dev/null; then
    echo "[-] Git not found. Installing..."
    sudo apt update && sudo apt install -y git
fi

# Clone repository
if [ ! -d "BugHunterFlow" ]; then
    git clone https://github.com/essev92-1/BugHunterFlow.git
    cd BugHunterFlow
else
    cd BugHunterFlow
    git pull origin main
fi

# Make scripts executable
chmod +x *.sh
chmod +x *.py

# Install Python dependencies
echo "[+] Installing Python dependencies..."
pip3 install -r requirements.txt 2>/dev/null || {
    echo "[*] Installing pip packages manually..."
    pip3 install requests beautifulsoup4 urllib3
}

# Check for Go tools
echo "[+] Checking for Go tools..."
if ! command -v go &> /dev/null; then
    echo "[-] Go not found. Please install Go first."
    echo "[-] Visit: https://golang.org/dl/"
    exit 1
fi

# Add to PATH
echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc
source ~/.bashrc

echo "[+] Installation complete!"
echo "[+] Usage: ./bughunter.sh example.com"
echo "[+] GitHub: https://github.com/essev92-1/BugHunterFlow"
