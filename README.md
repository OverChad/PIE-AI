

## Requirements

- **Python 3.10+** — https://www.python.org/downloads/
- **Windows 10/11** — window tracking uses Win32 APIs
- **Free Groq API key** — https://console.groq.com/keys
## Setup

### 1. Install dependencies

```bash
python setup.py
```

This installs all required packages and creates a default `config.json`.

### 2. Add your API key

Open `config.json` and replace the placeholder with your Groq key:

```json
{
    "api_key": "gsk_your_key_here"
}
```

Get a free key at: https://console.groq.com/keys  
No credit card required. Limits: 30 req/min, 14,400 req/day.

### 3. Run

```bash
python run.py
```

Open your browser at **http://localhost:8000**

---

## Manual dependency install

If `setup.py` fails for any reason, install manually:

```bash
pip install fastapi uvicorn[standard] pydantic requests psutil aiosqlite python-multipart websockets pywin32 python-dotenv
```

---

---

## How it works

1. You set a task (e.g. "Build a Python game")
2. PIE monitors your active windows every few seconds
3. If it detects a distraction (YouTube, social media, etc.) it sends a warning to the dashboard
4. You decide to close the distraction or mark it as allowed

The AI uses your task description to judge what counts as a distraction, a Python tutorial on YouTube would be allowed, an unrelated video would not.

---

## Troubleshooting

**`Monitor error: win32 not available`** — Install pywin32: `pip install pywin32`  
**`API key invalid`** — Check your key at https://console.groq.com/keys  
**Dashboard not loading** — Make sure port 8000 is free, or change it in `config.json`
