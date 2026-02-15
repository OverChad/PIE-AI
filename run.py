#!/usr/bin/env python3

import sys
import subprocess
import os
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from web.server import create_app
import uvicorn


CHROME_PATHS = [
    r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    os.path.expandvars(r"%LOCALAPPDATA%\Google\Chrome\Application\chrome.exe"),
]


def launch_chrome_with_cdp():
    """
    Launch Chrome with remote debugging enabled on port 9222.
    This allows PIE AI to close individual tabs instead of the whole browser.
    If Chrome is already running, this opens a new window alongside it.
    """
    chrome_exe = None
    for path in CHROME_PATHS:
        if os.path.exists(path):
            chrome_exe = path
            break

    if not chrome_exe:
        print("Chrome not found - tab-close feature will use fallback mode.")
        print("(Tab-close works best when Chrome is launched by PIE AI)")
        return

    # Check if Chrome is already running with CDP
    import urllib.request
    try:
        urllib.request.urlopen("http://127.0.0.1:9222/json", timeout=1)
        print("Chrome CDP already active on port 9222 - tab-close ready.")
        return
    except Exception:
        pass

    # Launch Chrome with remote debugging
    subprocess.Popen([
        chrome_exe,
        "--remote-debugging-port=9222",
        "--remote-allow-origins=http://127.0.0.1:8000",
        "http://127.0.0.1:8000"
    ], creationflags=subprocess.DETACHED_PROCESS if sys.platform == "win32" else 0)

    print("Chrome launched with tab-close support (CDP port 9222).")


def main():
    print("\n" + "=" * 50)
    print("PIE AI - Productivity Monitoring System")
    print("=" * 50)

    app = create_app()

    host = "127.0.0.1"
    port = 8000

    # Launch Chrome with CDP so we can close individual tabs
    launch_chrome_with_cdp()

    print(f"\nDashboard: http://localhost:{port}")
    print("Press Ctrl+C to stop")
    print("=" * 50 + "\n")

    try:
        uvicorn.run(
            app,
            host=host,
            port=port,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n\nPIE AI STOPPED")
    except Exception as e:
        print(f"\nError: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
