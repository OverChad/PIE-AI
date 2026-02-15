#!/usr/bin/env python3

import subprocess
import sys
import os
import json
from pathlib import Path


REQUIRED_PACKAGES = [
    "fastapi>=0.104.0",
    "uvicorn[standard]>=0.24.0",
    "pydantic>=2.0.0",
    "requests>=2.31.0",
    "psutil>=5.9.0",
    "aiosqlite>=0.19.0",
    "python-multipart>=0.0.6",
    "websockets>=12.0",
    "pywin32>=306",      # Windows only - for window tracking
    "python-dotenv>=1.0.0",
]

PYTHON_MIN = (3, 10)


def check_python_version():
    version = sys.version_info[:2]
    if version < PYTHON_MIN:
        print(f"ERROR: Python {PYTHON_MIN[0]}.{PYTHON_MIN[1]}+ is required.")
        print(f"       You have Python {version[0]}.{version[1]}.")
        print("       Download: https://www.python.org/downloads/")
        sys.exit(1)
    print(f"  Python {version[0]}.{version[1]} - OK")


def install_packages():
    print("\nInstalling dependencies...")
    failed = []

    for package in REQUIRED_PACKAGES:
        # pywin32 is Windows-only
        if "pywin32" in package and sys.platform != "win32":
            print(f"  Skipping {package} (not on Windows)")
            continue

        print(f"  Installing {package}...", end=" ", flush=True)
        result = subprocess.run(
            [sys.executable, "-m", "pip", "install", package, "--quiet"],
            capture_output=True,
            text=True
        )
        if result.returncode == 0:
            print("OK")
        else:
            print("FAILED")
            failed.append(package)

    if failed:
        print(f"\nWARNING: The following packages failed to install:")
        for pkg in failed:
            print(f"  - {pkg}")
        print("\nTry installing them manually:")
        print(f"  pip install {' '.join(failed)}")
    else:
        print("\nAll packages installed successfully.")


def check_config():
    config_path = Path(__file__).parent / "config.json"
    example_path = Path(__file__).parent / "config.example.json"

    if not config_path.exists():
        if example_path.exists():
            import shutil
            shutil.copy(example_path, config_path)
            print("\n  Created config.json from config.example.json")
        else:
            default_config = {
                "api_key": "YOUR_GROQ_API_KEY_HERE",
                "server": {"host": "127.0.0.1", "port": 8000},
                "monitoring": {"check_interval": 5}
            }
            with open(config_path, 'w') as f:
                json.dump(default_config, f, indent=4)
            print("\n  Created default config.json")

    with open(config_path, 'r') as f:
        config = json.load(f)

    api_key = config.get("api_key", "")
    if not api_key or api_key == "YOUR_GROQ_API_KEY_HERE":
        print("\n  ACTION REQUIRED: Add your Groq API key to config.json")
        print("    1. Get a free key at: https://console.groq.com/keys")
        print('    2. Open config.json and replace "YOUR_GROQ_API_KEY_HERE" with your key')
    else:
        print(f"\n  API key found in config.json: {api_key[:12]}...")


def main():
    print("=" * 55)
    print("  P.I.E AI - Setup")
    print("=" * 55)

    print("\nChecking Python version...")
    check_python_version()

    install_packages()
    check_config()

    print("\n" + "=" * 55)
    print("  Setup complete. Run the app with: python run.py")
    print("=" * 55 + "\n")


if __name__ == "__main__":
    main()
