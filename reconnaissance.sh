#!/bin/bash
# reconnaissance.sh - Enhanced Reconnaissance with Go Tools

DOMAIN=$1
OUTPUT_DIR="output/$DOMAIN"
RECON_DIR="$OUTPUT_DIR/recon"
TOOLS_DIR="$HOME/go/bin"

export PATH="$PATH:$TOOLS_DIR"

mkdir -p "$RECON_DIR"

echo "[+] Enhanced reconnaissance for $DOMAIN using Go tools"

# 1. Subdomain enumeration dengan multiple tools
echo "[*] Enumerating subdomains (subfinder + assetfinder + gau)..."
{
    # Gunakan subfinder
    if command -v subfinder &> /dev/null; then
        echo "[+] Running subfinder..."
        subfinder -d "$DOMAIN" -silent -o "$RECON_DIR/subfinder.txt"
        cat "$RECON_DIR/subfinder.txt"
    fi
    
    # Gunakan assetfinder
    if command -v assetfinder &> /dev/null; then
        echo "[+] Running assetfinder..."
        assetfinder --subs-only "$DOMAIN" | tee "$RECON_DIR/assetfinder.txt"
    fi
    
    # Gunakan gau untuk URLs
    if command -v gau &> /dev/null; then
        echo "[+] Running gau for URLs..."
        gau "$DOMAIN" | cut -d'/' -f3 | cut -d':' -f1 | sort -u | tee "$RECON_DIR/gau_subs.txt"
    fi
    
    # CRT.SH
    echo "[+] Checking crt.sh..."
    curl -s "https://crt.sh/?q=%25.$DOMAIN&output=json" | jq -r '.[].name_value' 2>/dev/null | sed 's/\*\.//g' | sort -u
    
} | sort -u | anew "$RECON_DIR/subdomains_all.txt" 2>/dev/null || sort -u > "$RECON_DIR/subdomains_all.txt"

echo "[+] Found $(wc -l < "$RECON_DIR/subdomains_all.txt") total subdomains"

# 2. Filter subdomains yang hidup dengan httpx
echo "[*] Checking live subdomains with httpx..."
if command -v httpx &> /dev/null; then
    cat "$RECON_DIR/subdomains_all.txt" | httpx -silent -threads 50 -o "$RECON_DIR/live_subdomains.txt"
    echo "[+] Found $(wc -l < "$RECON_DIR/live_subdomains.txt") live subdomains"
else
    cp "$RECON_DIR/subdomains_all.txt" "$RECON_DIR/live_subdomains.txt"
fi

# 3. Wayback Machine dengan waybackurls
echo "[*] Getting URLs from Wayback Machine..."
if command -v waybackurls &> /dev/null; then
    cat "$RECON_DIR/live_subdomains.txt" | waybackurls | sort -u > "$RECON_DIR/wayback_urls.txt"
    echo "[+] Found $(wc -l < "$RECON_DIR/wayback_urls.txt") URLs from Wayback"
fi

# 4. Spidering dengan hakrawler/katana
echo "[*] Spidering main domain with hakrawler/katana..."
if command -v katana &> /dev/null; then
    echo "[+] Using katana for spidering..."
    katana -u "https://$DOMAIN" -silent -o "$RECON_DIR/katana_urls.txt"
elif command -v hakrawler &> /dev/null; then
    echo "[+] Using hakrawler for spidering..."
    hakrawler -url "https://$DOMAIN" -plain | tee "$RECON_DIR/hakrawler_urls.txt"
fi

# 5. Gabungkan semua URLs
cat "$RECON_DIR/wayback_urls.txt" "$RECON_DIR/katana_urls.txt" "$RECON_DIR/hakrawler_urls.txt" 2>/dev/null | sort -u > "$RECON_DIR/all_urls.txt"

# 6. Ekstrak parameter dengan unfurl
echo "[*] Extracting parameters..."
if command -v unfurl &> /dev/null; then
    cat "$RECON_DIR/all_urls.txt" | unfurl keys | sort -u > "$RECON_DIR/param_keys.txt"
    echo "[+] Found $(wc -l < "$RECON_DIR/param_keys.txt") unique parameter keys"
fi

# 7. DNS records dengan dnsx (jika ada) atau dig
echo "[*] Gathering DNS records..."
{
    for sub in $(head -20 "$RECON_DIR/live_subdomains.txt"); do
        echo "=== $sub ==="
        dig "$sub" A +short 2>/dev/null || echo "No A records"
        echo ""
    done
} > "$RECON_DIR/dns_records.txt"

# 8. Screenshot dengan gowitness (jika ada)
echo "[*] Taking screenshots with gowitness..."
if command -v gowitness &> /dev/null; then
    mkdir -p "$RECON_DIR/screenshots"
    gowitness file -f "$RECON_DIR/live_subdomains.txt" -P "$RECON_DIR/screenshots" --delay 5 2>/dev/null &
    echo "[+] Screenshots running in background"
fi

# 9. Port scanning untuk domain utama
echo "[*] Quick port scan..."
nmap -sV --top-ports 100 "$DOMAIN" -oN "$RECON_DIR/nmap_scan.txt" 2>/dev/null || echo "Nmap scan skipped"

echo "[+] Enhanced reconnaissance completed!"
