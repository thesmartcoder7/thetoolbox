#!/usr/bin/env python3
import os
import platform
import subprocess
import sys
import venv

# Path to your virtual environment
VENV_PATH = ".venv"

def create_venv():
    print(f"Creating virtual environment at {VENV_PATH}...")
    builder = venv.EnvBuilder(with_pip=True)
    builder.create(VENV_PATH)
    print("Virtual environment created successfully.")

def activate_venv():
    system = platform.system()
    
    if system == "Windows":
        activate_script = os.path.join(VENV_PATH, "Scripts", "activate.bat")
        if not os.path.exists(activate_script):
            create_venv()
        print(f"Activating virtual environment for Windows: {activate_script}")
        subprocess.call(["cmd.exe", "/K", activate_script])
    
    elif system in ("Linux", "Darwin"):  # macOS
        activate_script = os.path.join(VENV_PATH, "bin", "activate")
        if not os.path.exists(activate_script):
            create_venv()
        print(f"Activating virtual environment for {system}: {activate_script}")
        subprocess.call(["/bin/bash", "--rcfile", activate_script])
    
    else:
        print(f"Unsupported platform: {system}")
        sys.exit(1)

if __name__ == "__main__":
    if not os.path.exists(VENV_PATH):
        create_venv()
    activate_venv()