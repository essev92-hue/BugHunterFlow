#!/bin/bash
# bughunter.sh - Final Version with Error Handling

set -e  # Exit on error

DOMAIN=$1
OUTPUT_DIR="output/$DOMAIN"
TOOLS_DIR="$HOME/go/bin"
LOG_FILE="$OUTPUT_DIR/scan_$(date +%Y%m%d_%H%M%S).log"

# Add Go tools to PATH
export PATH="$PATH:$TOOLS_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
print_banner() {
    echo -e "${GREEN}"
    cat << "EOF"
╔══════════════════════════════════════════════════════╗
║      BugHunterFlow - Automated Bug Hunting           ║
║           GitHub: @essev92-1                         ║
╚══════════════════════════════════════════════════════╝
EOF
    echo -e "${NC}"
}

# Functions
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

check_dependencies() {
    log "${BLUE}[*] Checking dependencies...${NC}"
    
    # Check Python
    if ! command -v python3 &> /dev/null; then
        log "${RED}[!] Python3 not found. Please install python3${NC}"
        exit 1
    fi
    
    # Check Go tools
    local missing_tools=()
    local required_tools=("subfinder" "httpx" "nuclei" "ffuf")
    
    for tool in "${required_tools[@]}"; do
        if ! command -v "$tool" &> /dev/null; then
            missing_tools+=("$tool")
        fi
    done
    
    if [ ${#missing_tools[@]} -gt 0 ]; then
        log "${YELLOW}[!] Missing tools: ${missing_tools[*]}${NC}"
        log "${YELLOW}[!] Install with: go install github.com/projectdiscovery/[tool]@latest${NC}"
    fi
}

print_summary() {
    echo -e "\n${GREEN}════════════ SCAN SUMMARY ════════════${NC}"
    echo -e "Target: ${BLUE}$DOMAIN${NC}"
    echo -e "Output: ${BLUE}$OUTPUT_DIR${NC}"
    echo -e "Log: ${BLUE}$LOG_FILE${NC}"
    
    if [ -d "$OUTPUT_DIR" ]; then
        echo -e "\n${YELLOW}Generated Files:${NC}"
        find "$OUTPUT_DIR" -type f -name "*.txt" -o -name "*.json" -o -name "*.md" | head -10
    fi
}

# Main execution
main() {
    print_banner
    
    if [ -z "$DOMAIN" ]; then
        echo "Usage: ./bughunter.sh example.com"
        echo "Example: ./bughunter.sh hackerone.com"
        exit 1
    fi
    
    log "${GREEN}[+] Starting BugHunterFlow for: $DOMAIN${NC}"
    
    # Create output directory
    mkdir -p "$OUTPUT_DIR"
    
    # Check dependencies
    check_dependencies
    
    # Phase 1: Reconnaissance
    log "${YELLOW}[*] Phase 1/6: Reconnaissance${NC}"
    ./reconnaissance.sh "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"
    
    # Phase 2: Web Technology Analysis
    log "${YELLOW}[*] Phase 2/6: Technology Analysis${NC}"
    python3 web_tech.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"
    
    # Phase 3: Parameter Discovery
    log "${YELLOW}[*] Phase 3/6: Parameter Discovery${NC}"
    python3 param_finder.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"
    
    # Phase 4: Bug Scanning
    log "${YELLOW}[*] Phase 4/6: Bug Scanning${NC}"
    python3 bug_scanner.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"
    
    # Phase 5: Security Headers
    log "${YELLOW}[*] Phase 5/6: Security Headers${NC}"
    python3 header_checker.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"
    
    # Phase 6: JavaScript Analysis
    log "${YELLOW}[*] Phase 6/6: JavaScript Analysis${NC}"
    python3 js_analyzer.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"
    
    # Optional: Nuclei deep scan
    if command -v nuclei &> /dev/null; then
        log "${BLUE}[*] Running Nuclei deep scan (background)...${NC}"
        nuclei -u "https://$DOMAIN" -severity medium,high,critical -o "$OUTPUT_DIR/nuclei_deep_scan.txt" -silent &
    fi
    
    log "${GREEN}[+] Scan completed successfully!${NC}"
    print_summary
}

# Run main function
main "$@"
