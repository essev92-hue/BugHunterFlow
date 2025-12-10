# BugHunterFlow - Go Tools Enhanced Edition

Automated bug hunting pipeline dengan integrasi penuh tools Go.

## Tools Go yang Digunakan:
- **subfinder, assetfinder** - Subdomain enumeration  
- **gau, waybackurls** - URL discovery  
- **httpx** - Live host checking  
- **nuclei** - Vulnerability scanning  
- **ffuf** - Fuzzing  
- **dalfox** - XSS scanning  
- **katana, hakrawler** - Spidering  
- **unfurl** - URL parsing  
- **gf** - Pattern matching  
- **anew, notify** - Output processing  
- **gowitness** - Screenshots  

## Setup Cepat:
```bash
# 1. Clone dan setup
git clone https://github.com/essev92-1/BugHunterFlow.git
cd BugHunterFlow
chmod +x *.sh *.py
pip3 install -r requirements.txt

# 2. Pastikan tools Go di PATH
echo 'export PATH="$PATH:$HOME/go/bin"' >> ~/.bashrc
source ~/.bashrc

# 3. Jalankan
./bughunter.sh example.com


## Example Output
[2023-12-10 16:30:28] [+] Starting BugHunterFlow for: example.com
[2023-12-10 16:30:35] [+] Found 124 subdomains
[2023-12-10 16:31:10] [+] Detected: Nginx, React, WordPress
[2023-12-10 16:32:45] [+] Found 45 potential vulnerabilities
...
