#!/bin/bash
# bughunter.sh - Automated Bug Hunting Pipeline dengan Tools Go

DOMAIN=$1
OUTPUT_DIR="output/$DOMAIN"
TOOLS_DIR="$HOME/go/bin"
LOG_FILE="$OUTPUT_DIR/scan.log"

# Tambahkan PATH untuk tools Go
export PATH="$PATH:$TOOLS_DIR"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Banner
echo -e "${GREEN}"
cat << "EOF"
╔══════════════════════════════════════════════════════╗
║      BugHunterFlow - Enhanced Go Tools Edition       ║
║         Integrated with: ffuf, nuclei, gau, etc.     ║
╚══════════════════════════════════════════════════════╝
EOF
echo -e "${NC}"

if [ -z "$DOMAIN" ]; then
    echo "Usage: ./bughunter.sh example.com"
    exit 1
fi

# Buat direktori output
mkdir -p "$OUTPUT_DIR"

# Fungsi log
log() {
    echo -e "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# Fungsi cek tool Go
check_go_tool() {
    if [ -f "$TOOLS_DIR/$1" ]; then
        log "${GREEN}[✓] Tool $1 ditemukan di $TOOLS_DIR/${NC}"
        return 0
    elif command -v $1 &> /dev/null; then
        log "${GREEN}[✓] Tool $1 ditemukan di PATH${NC}"
        return 0
    else
        log "${RED}[!] Tool $1 tidak ditemukan${NC}"
        return 1
    fi
}

# Cek tools yang penting
log "${BLUE}[*] Memeriksa tools Go yang tersedia...${NC}"
check_go_tool "subfinder"
check_go_tool "assetfinder"
check_go_tool "httpx"
check_go_tool "gau"
check_go_tool "waybackurls"
check_go_tool "nuclei"
check_go_tool "ffuf"
check_go_tool "dalfox"
check_go_tool "hakrawler"
check_go_tool "katana"
check_go_tool "anew"
check_go_tool "notify"

# Mulai scanning
log "${GREEN}[+] Memulai scan untuk $DOMAIN${NC}"

# Fase 1: Reconnaissance dengan tools Go
log "${YELLOW}[*] Fase 1: Reconnaissance (Enhanced)${NC}"
./reconnaissance.sh "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"

# Fase 2: Analisis Aplikasi Web
log "${YELLOW}[*] Fase 2: Analisis Teknologi Web${NC}"
python3 web_tech.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"

# Fase 3: Cari Parameter & Endpoint dengan tools Go
log "${YELLOW}[*] Fase 3: Mencari Parameter & Endpoint (Enhanced)${NC}"
python3 param_finder.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"

# Fase 4: Uji Bug Umum dengan nuclei dan dalfox
log "${YELLOW}[*] Fase 4: Scanning Bug dengan Nuclei & Dalfox${NC}"
python3 bug_scanner.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"

# Fase 5: Cek Security Headers
log "${YELLOW}[*] Fase 5: Checking Security Headers${NC}"
python3 header_checker.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"

# Fase 6: Analisis JavaScript dengan katana
log "${YELLOW}[*] Fase 6: Analisis File JavaScript (Enhanced)${NC}"
python3 js_analyzer.py "$DOMAIN" 2>&1 | tee -a "$LOG_FILE"

# Ekstra: Fase nuclei scanning
log "${YELLOW}[*] Fase Ekstra: Nuclei Template Scanning${NC}"
if check_go_tool "nuclei"; then
    nuclei -u "https://$DOMAIN" -o "$OUTPUT_DIR/nuclei_scan.txt" -silent 2>/dev/null &
    log "${BLUE}[*] Nuclei scan berjalan di background${NC}"
fi

# Ringkasan
log "${GREEN}[+] Scan selesai!${NC}"
echo -e "\n${GREEN}════════════ HASIL SCAN ════════════${NC}"
echo -e "Output disimpan di: ${BLUE}$OUTPUT_DIR${NC}"
echo -e "File log: ${BLUE}$LOG_FILE${NC}"
echo -e "\n${YELLOW}Tools Go yang digunakan:${NC}"
ls $TOOLS_DIR | grep -E "(subfinder|assetfinder|httpx|gau|nuclei|ffuf|dalfox)" | xargs echo "  - "
echo -e "\n${GREEN}Struktur hasil:${NC}"
tree "$OUTPUT_DIR" 2>/dev/null || ls -la "$OUTPUT_DIR"
