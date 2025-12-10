#!/usr/bin/env python3
# bug_scanner.py - Enhanced Bug Scanner with Go Tools Integration

import requests
import sys
import os
import json
import subprocess
from urllib.parse import urljoin
from pathlib import Path

def scan_with_go_tools(domain):
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    
    tools_dir = str(Path.home() / "go" / "bin")
    url = f"https://{domain}"
    
    print(f"[*] Enhanced bug scanning for {domain} using Go tools")
    
    findings = {
        "xss": [],
        "sqli": [],
        "idor": [],
        "ssrf": [],
        "rce": [],
        "file_upload": [],
        "nuclei_findings": []
    }
    
    # 1. Scan dengan nuclei
    print("[*] Running nuclei scan...")
    nuclei_path = os.path.join(tools_dir, "nuclei")
    if os.path.exists(nuclei_path):
        try:
            cmd = [nuclei_path, "-u", url, "-silent", "-json"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            
            if result.stdout:
                for line in result.stdout.strip().split('\n'):
                    if line:
                        try:
                            finding = json.loads(line)
                            findings["nuclei_findings"].append({
                                "template": finding.get("template-id", ""),
                                "severity": finding.get("info", {}).get("severity", "unknown"),
                                "name": finding.get("info", {}).get("name", ""),
                                "matched": finding.get("matched-at", "")
                            })
                        except:
                            pass
                print(f"[+] Nuclei found {len(findings['nuclei_findings'])} issues")
        except Exception as e:
            print(f"[-] Nuclei scan error: {e}")
    
    # 2. XSS scan dengan dalfox
    print("[*] Running dalfox for XSS scanning...")
    dalfox_path = os.path.join(tools_dir, "dalfox")
    if os.path.exists(dalfox_path):
        try:
            # Gunakan URLs dari recon
            urls_file = f"{output_dir}/recon/all_urls.txt"
            if os.path.exists(urls_file):
                cmd = [dalfox_path, "file", urls_file, "--silence"]
                result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)
                
                if result.stdout:
                    for line in result.stdout.split('\n'):
                        if '[POC]' in line or '[VULN]' in line:
                            findings["xss"].append({
                                "tool": "dalfox",
                                "finding": line.strip()
                            })
                    print(f"[+] Dalfox found {len(findings['xss'])} XSS issues")
        except Exception as e:
            print(f"[-] Dalfox scan error: {e}")
    
    # 3. Fuzzing dengan ffuf
    print("[*] Running ffuf for directory fuzzing...")
    ffuf_path = os.path.join(tools_dir, "ffuf")
    if os.path.exists(ffuf_path):
        try:
            # Wordlist sederhana
            wordlist = "/usr/share/wordlists/dirb/common.txt"
            if not os.path.exists(wordlist):
                # Buat wordlist mini
                wordlist = f"{output_dir}/mini_wordlist.txt"
                with open(wordlist, 'w') as f:
                    f.write("\n".join(["admin", "api", "backup", "config", "test", "debug", "phpinfo"]))
            
            cmd = [ffuf_path, "-u", f"{url}/FUZZ", "-w", wordlist, "-mc", "200,301,302", "-t", "50", "-o", f"{output_dir}/ffuf_scan.json", "-of", "json"]
            subprocess.run(cmd, capture_output=True, timeout=120)
            print("[+] FFuf directory scan completed")
        except Exception as e:
            print(f"[-] FFuf scan error: {e}")
    
    # 4. IDOR pattern detection dari parameter
    print("[*] Checking for IDOR patterns...")
    params_file = f"{output_dir}/recon/param_keys.txt"
    if os.path.exists(params_file):
        with open(params_file, 'r') as f:
            params = [line.strip() for line in f]
        
        idor_patterns = ['id', 'user', 'uid', 'account', 'doc', 'file', 'invoice', 'order']
        for param in params:
            for pattern in idor_patterns:
                if pattern in param.lower():
                    findings["idor"].append({
                        "parameter": param,
                        "pattern": pattern,
                        "note": "Potential IDOR - manual testing required"
                    })
    
    # 5. Check file upload endpoints
    print("[*] Looking for file upload endpoints...")
    endpoints_file = f"{output_dir}/endpoints.txt"
    if os.path.exists(endpoints_file):
        with open(endpoints_file, 'r') as f:
            endpoints = [line.strip() for line in f]
        
        upload_keywords = ['upload', 'attachment', 'file', 'image', 'document', 'import', 'submit']
        for endpoint in endpoints:
            for keyword in upload_keywords:
                if keyword in endpoint.lower():
                    findings["file_upload"].append({
                        "endpoint": endpoint,
                        "keyword": keyword
                    })
    
    # Save semua findings
    with open(f"{output_dir}/bug_findings_enhanced.json", 'w') as f:
        json.dump(findings, f, indent=2)
    
    # Print summary
    print(f"\n{'='*50}")
    print("[+] Enhanced Bug Scan Summary:")
    print(f"{'='*50}")
    for bug_type, items in findings.items():
        if items:
            print(f"  [-] {bug_type.upper():15}: {len(items)} findings")
    print(f"{'='*50}")
    
    return findings

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 bug_scanner.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    scan_with_go_tools(domain)
