#!/usr/bin/env python3
# param_finder.py - Enhanced Parameter Finder with Go Tools

import requests
import re
import sys
import os
import subprocess
import json
from urllib.parse import urlparse, parse_qs
from pathlib import Path

def find_parameters_enhanced(domain):
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    
    tools_dir = str(Path.home() / "go" / "bin")
    url = f"https://{domain}"
    
    print(f"[*] Enhanced parameter discovery for {domain}")
    
    endpoints = set()
    parameters = set()
    all_urls = set()
    
    # 1. Gunakan gau untuk mendapatkan URLs
    print("[*] Using gau to discover URLs...")
    gau_path = os.path.join(tools_dir, "gau")
    
    if os.path.exists(gau_path):
        try:
            cmd = [gau_path, domain, "--subs"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            if result.stdout:
                urls = result.stdout.strip().split('\n')
                all_urls.update(urls)
                print(f"[+] GAU found {len(urls)} URLs")
        except Exception as e:
            print(f"[-] GAU error: {e}")
    
    # 2. Gunakan waybackurls
    print("[*] Using waybackurls...")
    wayback_path = os.path.join(tools_dir, "waybackurls")
    
    if os.path.exists(wayback_path):
        try:
            cmd = [wayback_path, domain]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
            
            if result.stdout:
                urls = result.stdout.strip().split('\n')
                all_urls.update(urls)
                print(f"[+] Waybackurls found {len(urls)} URLs")
        except:
            pass
    
    # 3. Tambahkan dari hasil recon
    recon_urls = f"{output_dir}/recon/all_urls.txt"
    if os.path.exists(recon_urls):
        with open(recon_urls, 'r') as f:
            urls = [line.strip() for line in f]
            all_urls.update(urls)
    
    # 4. Gunakan unfurl untuk extract parameter keys
    print("[*] Extracting parameters with unfurl...")
    unfurl_path = os.path.join(tools_dir, "unfurl")
    
    if os.path.exists(unfurl_path) and all_urls:
        # Simpan URLs ke file
        urls_file = f"{output_dir}/all_urls_temp.txt"
        with open(urls_file, 'w') as f:
            f.write("\n".join(all_urls))
        
        try:
            # Ekstrak parameter keys
            cmd = [unfurl_path, "keys", urls_file]
            result = subprocess.run(cmd, capture_output=True, text=True)
            
            if result.stdout:
                params = result.stdout.strip().split('\n')
                parameters.update(params)
                print(f"[+] Unfurl found {len(params)} unique parameters")
        except:
            pass
        
        # Hapus file temporary
        os.remove(urls_file)
    
    # 5. Juga parse manual
    for url in list(all_urls)[:1000]:  # Batasi untuk performa
        try:
            parsed = urlparse(url)
            
            # Tambah endpoint
            if parsed.path and parsed.path != '/':
                endpoints.add(parsed.path)
            
            # Tambah parameter dari query string
            query_params = parse_qs(parsed.query)
            for param in query_params.keys():
                parameters.add(param)
        except:
            continue
    
    # 6. Gunakan gf patterns untuk parameter menarik
    print("[*] Checking for interesting parameters with gf...")
    gf_path = os.path.join(tools_dir, "gf")
    
    if os.path.exists(gf_path) and parameters:
        param_file = f"{output_dir}/parameters_temp.txt"
        with open(param_file, 'w') as f:
            f.write("\n".join(parameters))
        
        interesting_patterns = ['idor', 'ssrf', 'xss', 'rce', 'sqli', 'lfi']
        
        interesting_params = {}
        for pattern in interesting_patterns:
            try:
                cmd = [gf_path, pattern, param_file]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.stdout:
                    interesting_params[pattern] = result.stdout.strip().split('\n')
            except:
                pass
        
        # Simpan parameter menarik
        if interesting_params:
            with open(f"{output_dir}/interesting_parameters.json", 'w') as f:
                json.dump(interesting_params, f, indent=2)
        
        os.remove(param_file)
    
    # Convert to lists
    endpoints = sorted(list(endpoints))
    parameters = sorted(list(parameters))
    
    # Save results
    with open(f"{output_dir}/endpoints_enhanced.txt", 'w') as f:
        for endpoint in endpoints:
            f.write(f"{endpoint}\n")
    
    with open(f"{output_dir}/parameters_enhanced.txt", 'w') as f:
        for param in parameters:
            f.write(f"{param}\n")
    
    # Save untuk ffuf
    with open(f"{output_dir}/urls_for_ffuf.txt", 'w') as f:
        for url in list(all_urls)[:5000]:  # Batasi untuk ffuf
            f.write(f"{url}\n")
    
    print(f"\n[+] Parameter Discovery Complete:")
    print(f"  - Endpoints: {len(endpoints)}")
    print(f"  - Parameters: {len(parameters)}")
    print(f"  - Sample endpoints: {endpoints[:5]}")
    print(f"  - Sample parameters: {parameters[:5]}")
    
    # Rekomendasi
    if len(parameters) > 100:
        print(f"\n[!] Banyak parameter ditemukan ({len(parameters)})")
        print("[!] Pertimbangkan untuk fokus testing pada parameter yang menarik")
    
    return endpoints, parameters

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 param_finder.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    find_parameters_enhanced(domain)
