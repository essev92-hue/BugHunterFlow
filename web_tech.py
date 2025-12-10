#!/usr/bin/env python3
# web_tech.py - Fase 2: Web Technology Analysis

import requests
import json
import sys
import os
from datetime import datetime

def analyze_web_tech(domain):
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    
    results = {
        "domain": domain,
        "scan_date": datetime.now().isoformat(),
        "technologies": [],
        "headers": {},
        "security_indicators": {}
    }
    
    url = f"https://{domain}"
    
    try:
        print(f"[*] Analyzing {url}")
        response = requests.get(url, timeout=10, verify=False)
        
        # Headers analysis
        results["headers"] = dict(response.headers)
        
        # Server technology detection
        server = response.headers.get('Server', 'Unknown')
        results["technologies"].append({"type": "Server", "name": server})
        
        # X-Powered-By
        powered_by = response.headers.get('X-Powered-By')
        if powered_by:
            results["technologies"].append({"type": "Backend", "name": powered_by})
        
        # Framework detection from headers
        if 'X-Generator' in response.headers:
            results["technologies"].append({"type": "CMS/Generator", "name": response.headers['X-Generator']})
        
        # WAF detection
        waf_indicators = ['cloudflare', 'akamai', 'sucuri', 'imperva', 'aws', 'fastly']
        for waf in waf_indicators:
            if waf in server.lower():
                results["security_indicators"]["waf"] = waf.capitalize()
                break
        
        # CDN detection
        cdn_headers = ['CF-RAY', 'Akamai-Origin-Hop', 'X-CDN']
        for header in cdn_headers:
            if header in response.headers:
                results["security_indicators"]["cdn"] = "Detected"
                break
        
        # Content analysis for framework clues
        content = response.text
        framework_patterns = {
            'wordpress': ['wp-content', 'wp-includes'],
            'laravel': ['/vendor/laravel/', 'csrf-token'],
            'django': ['csrfmiddlewaretoken', 'Django'],
            'react': ['react.', 'react-dom'],
            'vue': ['vue.', '__vue__'],
            'jquery': ['jquery.min.js']
        }
        
        for framework, patterns in framework_patterns.items():
            for pattern in patterns:
                if pattern.lower() in content.lower():
                    results["technologies"].append({"type": "Framework", "name": framework.capitalize()})
                    break
        
        # Save results
        with open(f"{output_dir}/web_tech.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"[+] Analysis saved to {output_dir}/web_tech.json")
        print(f"[+] Detected technologies: {[t['name'] for t in results['technologies']]}")
        
    except Exception as e:
        print(f"[-] Error analyzing {domain}: {e}")
        # Try HTTP if HTTPS fails
        try:
            url = f"http://{domain}"
            response = requests.get(url, timeout=10)
            print(f"[*] Using HTTP instead of HTTPS")
        except:
            pass

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 web_tech.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    analyze_web_tech(domain)
