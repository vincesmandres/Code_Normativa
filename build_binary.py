import subprocess
import sys

print("Starting PyInstaller build for main.py...")

try:
    result = subprocess.run([sys.executable, "-m", "pyinstaller", "--onefile", "--windowed", "main.py"], check=True)
    print("Build completed successfully.")
except subprocess.CalledProcessError as e:
    print(f"Build failed with error: {e}")
    sys.exit(1)