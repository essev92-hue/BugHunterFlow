#!/usr/bin/env python3
# header_checker.py - Fase 5: Security Headers Checker

import requests
import sys
import os
from datetime import datetime

def check_security_headers(domain):
    output_dir = f"output/{domain}"
    os.makedirs(output_dir, exist_ok=True)
    
    url = f"https://{domain}"
    
    print(f"[*] Checking security headers for {domain}")
    
    security_headers = {
        'Content-Security-Policy': {
            'required': True,
            'description': 'Prevents XSS and other code injection attacks',
            'status': 'MISSING',
            'score': 0
        },
        'X-Frame-Options': {
            'required': True,
            'description': 'Prevents clickjacking attacks',
            'status': 'MISSING',
            'score': 0
        },
        'Strict-Transport-Security': {
            'required': True,
            'description': 'Enforces HTTPS connections',
            'status': 'MISSING',
            'score': 0
        },
        'X-Content-Type-Options': {
            'required': True,
            'description': 'Prevents MIME type sniffing',
            'status': 'MISSING',
            'score': 0
        },
        'Referrer-Policy': {
            'required': False,
            'description': 'Controls referrer information',
            'status': 'MISSING',
            'score': 0
        },
        'Permissions-Policy': {
            'required': False,
            'description': 'Controls browser features',
            'status': 'MISSING',
            'score': 0
        }
    }
    
    try:
        response = requests.get(url, timeout=10, verify=False)
        headers = response.headers
        
        # Check each security header
        total_score = 0
        max_score = 0
        
        for header, info in security_headers.items():
            max_score += 2 if info['required'] else 1
            
            if header in headers:
                info['status'] = 'PRESENT'
                info['value'] = headers[header]
                info['score'] = 2 if info['required'] else 1
                total_score += info['score']
            else:
                info['status'] = 'MISSING'
                info['score'] = 0
        
        # Calculate percentage
        security_percentage = (total_score / max_score) * 100 if max_score > 0 else 0
        
        # Generate report
        report = f"""# Security Headers Report for {domain}
Scan Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
Security Score: {security_percentage:.1f}%

## Headers Analysis:
"""
        
        for header, info in security_headers.items():
            report += f"\n### {header}\n"
            report += f"- Status: **{info['status']}**\n"
            report += f"- Importance: {'Required' if info['required'] else 'Recommended'}\n"
            report += f"- Description: {info['description']}\n"
            if info['status'] == 'PRESENT':
                report += f"- Value: `{info['value']}`\n"
            report += f"- Score: {info['score']}/{'2' if info['required'] else '1'}\n"
        
        report += f"\n## Recommendations:\n"
        if security_percentage < 50:
            report += "❌ **POOR** - Implement missing security headers immediately\n"
        elif security_percentage < 80:
            report += "⚠️ **FAIR** - Consider implementing missing headers\n"
        else:
            report += "✅ **GOOD** - Security headers are well configured\n"
        
        # Save report
        report_file = f"{output_dir}/security_headers_report.md"
        with open(report_file, 'w') as f:
            f.write(report)
        
        print(f"[+] Security headers report saved to {report_file}")
        print(f"[+] Security score: {security_percentage:.1f}%")
        
    except Exception as e:
        print(f"[-] Error checking headers: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 header_checker.py example.com")
        sys.exit(1)
    
    domain = sys.argv[1]
    check_security_headers(domain)
