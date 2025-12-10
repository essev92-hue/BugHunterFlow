#!/usr/bin/env python3
# js_analyzer.py - Enhanced JavaScript Analyzer with Katana

import requests
import re
import sys
import os
import subprocess
import json
from urllib.parse import urljoin
from pathlib import Path

def analyze_javascript_enhanced(domain):
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    
    tools_dir = str(Path.home() / "go" / "bin")
    url = f"https://{domain}"
    
    print(f"[*] Enhanced JavaScript analysis for {domain}")
    
    findings = {
        "api_keys": [],
        "endpoints": [],
        "tokens": [],
        "internal_urls": [],
        "developer_info": [],
        "js_files": [],
        "secrets": []
    }
    
    # 1. Gunakan katana untuk menemukan JS files
    print("[*] Using katana to discover JavaScript files...")
    katana_path = os.path.join(tools_dir, "katana")
    
    js_files = set()
    
    if os.path.exists(katana_path):
        try:
            cmd = [katana_path, "-u", url, "-silent", "-jc", "-d", "3"]
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
            
            # Extract JS files from katana output
            js_pattern = r'https?://[^"\'\s]+\.js'
            discovered_js = re.findall(js_pattern, result.stdout)
            js_files.update(discovered_js)
            
            print(f"[+] Katana found {len(discovered_js)} JS files")
        except Exception as e:
            print(f"[-] Katana error: {e}")
    
    # 2. Juga dapatkan dari halaman utama
    try:
        response = requests.get(url, timeout=10, verify=False)
        # Extract JS dari tag script
        script_pattern = r'<script[^>]+src=["\']([^"\']+\.js)["\'][^>]*>'
        inline_scripts = re.findall(r'<script[^>]*>(.*?)</script>', response.text, re.DOTALL)
        
        for js in re.findall(script_pattern, response.text):
            js_url = urljoin(url, js)
            js_files.add(js_url)
    except:
        pass
    
    # 3. Download dan analisis JS files (maks 20 file)
    print(f"[*] Analyzing {min(len(js_files), 20)} JS files...")
    all_js_content = []
    
    for i, js_url in enumerate(list(js_files)[:20]):
        try:
            print(f"  [{i+1}/{min(len(js_files), 20)}] Downloading: {js_url[:80]}...")
            js_response = requests.get(js_url, timeout=5)
            
            if js_response.status_code == 200:
                js_content = js_response.text
                all_js_content.append(js_content)
                findings["js_files"].append(js_url)
                
                # Analisis langsung
                analyze_js_content(js_content, js_url, findings)
        except Exception as e:
            continue
    
    # 4. Gunakan gf patterns untuk menemukan secrets
    print("[*] Using gf patterns for secrets...")
    gf_path = os.path.join(tools_dir, "gf")
    
    if os.path.exists(gf_path) and all_js_content:
        # Simpan semua JS ke file temporary
        temp_js = f"{output_dir}/all_js_combined.js"
        with open(temp_js, 'w') as f:
            f.write("\n".join(all_js_content))
        
        try:
            # Coba pattern tertentu
            patterns = ['api-keys', 'tokens', 'aws', 'generic']
            for pattern in patterns:
                cmd = [gf_path, pattern, temp_js]
                result = subprocess.run(cmd, capture_output=True, text=True)
                
                if result.stdout:
                    lines = result.stdout.strip().split('\n')
                    for line in lines:
                        if line and 'api' in pattern:
                            findings["api_keys"].append(line[:100])
                        elif line and 'token' in pattern:
                            findings["tokens"].append(line[:100])
        except:
            pass
        
        # Hapus file temporary
        os.remove(temp_js)
    
    # 5. Remove duplicates
    for key in findings:
        if isinstance(findings[key], list):
            findings[key] = list(set(findings[key]))
    
    # 6. Save detailed report
    save_js_report(domain, findings)
    
    return findings

def analyze_js_content(content, source_url, findings):
    """Analisis konten JavaScript untuk berbagai pattern"""
    
    # API Keys patterns
    api_patterns = [
        r'["\'](?:api[_-]?key|secret|token|password)["\']\s*[:=]\s*["\']([A-Za-z0-9_\-=]{20,})["\']',
        r'(?:aws|azure|google)[^"\']*["\']([A-Za-z0-9_\-=]{20,})["\']',
        r'["\'](?:access[_-]?key|secret[_-]?key)["\']\s*[:=]\s*["\']([A-Za-z0-9_\-=]{20,})["\']'
    ]
    
    for pattern in api_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        findings["api_keys"].extend(matches)
    
    # Endpoints
    endpoint_patterns = [
        r'["\'](/api/v[0-9]/[^"\']+)["\']',
        r'["\'](/[a-z]{3,}/[a-z]{3,}/[^"\']+)["\']',
        r'fetch\(["\']([^"\']+)["\']',
        r'\.(?:get|post|put|delete)\(["\']([^"\']+)["\']',
        r'url:\s*["\']([^"\']+)["\']'
    ]
    
    for pattern in endpoint_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        findings["endpoints"].extend(matches)
    
    # Internal URLs
    internal_patterns = [
        r'["\'](https?://(?:localhost|127\.0\.0\.1|192\.168|10\.|172\.(?:1[6-9]|2[0-9]|3[0-1]))[^"\']*)["\']',
        r'["\'](https?://(?:dev|stage|test|staging|internal)[^"\']*)["\']'
    ]
    
    for pattern in internal_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        findings["internal_urls"].extend(matches)
    
    # Developer info
    dev_patterns = [
        r'@(?:author|license|copyright)\s+([^\n]+)',
        r'username["\']?\s*[:=]\s*["\']([^"\']+)["\']',
        r'email["\']?\s*[:=]\s*["\']([^@]+@[^"\']+)["\']',
        r'created by[:\s]+([^\n]+)',
        r'Maintained by[:\s]+([^\n]+)'
    ]
    
    for pattern in dev_patterns:
        matches = re.findall(pattern, content, re.IGNORECASE)
        findings["developer_info"].extend(matches)
    
    # Hardcoded secrets
    secret_patterns = [
        r'["\'](eyJ[A-Za-z0-9\-_=]+\.[A-Za-z0-9\-_=]+\.?[A-Za-z0-9\-_=]*)["\']',  # JWT
        r'["\'](gh[ps]_[A-Za-z0-9_]{36,})["\']',  # GitHub tokens
        r'["\'](xox[abp]-[A-Za-z0-9\-]+)["\']',  # Slack tokens
        r'["\'](sk_[a-z0-9]{32})["\']'  # Stripe keys
    ]
    
    for pattern in secret_patterns:
        matches = re.findall(pattern, content)
        findings["secrets"].extend(matches)

def save_js_report(domain, findings):
    output_dir = f"output/{domain}"
    report_file = f"{output_dir}/js_analysis_enhanced.md"
    
    with open(report_file, 'w') as f:
        f.write(f"# Enhanced JavaScript Analysis Report for {domain}\n")
        f.write(f"Generated: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 60 + "\n\n")
        
        # Summary
        f.write("## 📊 Summary\n")
        f.write("| Metric | Count |\n")
        f.write("|--------|-------|\n")
        f.write(f"| JS Files Analyzed | {len(findings['js_files'])} |\n")
        f.write(f"| API Keys Found | {len(findings['api_keys'])} |\n")
        f.write(f"| Secrets Found | {len(findings['secrets'])} |\n")
        f.write(f"| Endpoints Found | {len(findings['endpoints'])} |\n")
        f.write(f"| Internal URLs | {len(findings['internal_urls'])} |\n")
        f.write(f"| Developer Info | {len(findings['developer_info'])} |\n\n")
        
        # JS Files
        if findings['js_files']:
            f.write("## 📁 JavaScript Files\n")
            for js_file in findings['js_files'][:30]:  # Limit display
                f.write(f"- `{js_file}`\n")
            if len(findings['js_files']) > 30:
                f.write(f"- ... and {len(findings['js_files']) - 30} more\n")
            f.write("\n")
        
        # API Keys & Secrets (dengan caution)
        if findings['api_keys'] or findings['secrets']:
            f.write("## 🔐 Potential Secrets & API Keys\n")
            f.write("> ⚠️ **WARNING**: Handle these findings with care!\n\n")
            
            if findings['secrets']:
                f.write("### High-Confidence Secrets\n")
                for secret in findings['secrets'][:10]:
                    f.write(f"- `{secret[:50]}...`\n")
            
            if findings['api_keys']:
                f.write("### Potential API Keys\n")
                for key in findings['api_keys'][:15]:
                    f.write(f"- `{key[:60]}...`\n")
            f.write("\n")
        
        # Endpoints
        if findings['endpoints']:
            f.write("## 🔗 Discovered Endpoints\n")
            unique_endpoints = sorted(set(findings['endpoints']))
            for endpoint in unique_endpoints[:40]:
                f.write(f"- `{endpoint}`\n")
            f.write("\n")
        
        # Internal URLs
        if findings['internal_urls']:
            f.write("## 🏢 Internal URLs\n")
            for url in findings['internal_urls'][:20]:
                f.write(f"- `{url}`\n")
            f.write("\n")
        
        # Developer Info
        if findings['developer_info']:
            f.write("## 👨‍💻 Developer Information\n")
            for info in findings['developer_info'][:10]:
                f.write(f"- {info}\n")
        
        # Recommendations
        f.write("\n## 🛡️ Recommendations\n")
        f.write("1. Rotate any exposed API keys immediately\n")
        f.write("2. Remove hardcoded secrets from JavaScript files\n")
        f.write("3. Move sensitive configuration to server-side\n")
        f.write("4. Implement proper access controls for internal endpoints\n")
    
    print(f"[+] Enhanced JS analysis saved to {report_file}")
    print(f"[+] Found {len(findings['secrets'])} potential secrets")
    print(f"[+] Found {len(findings['api_keys'])} API keys")
    print(f"[+] Found {len(findings['endpoints'])} endpoints")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 js_analyzer.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    analyze_javascript_enhanced(domain)
