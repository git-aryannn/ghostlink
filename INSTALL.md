# GhostLink v1.0 - Installation & Deployment Guide

## Quick Start (3 Steps)

### Step 1: Clone Repository
```bash
git clone https://github.com/YOUR_USERNAME/ghostlink.git
cd ghostlink
```

### Step 2: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 3: Run Setup Script
```bash
chmod +x setup.sh
./setup.sh
```

The setup script will guide you through:
- Starting the C2 Server (Listener.py)
- Deploying the Agent (Implant.py)
- Running tests
- Interactive menu for all operations

---

## Manual Setup (Alternative)

### Terminal 1 - Start C2 Server:
```bash
python Listener.py
```
Server runs on: `http://127.0.0.1:8888`

### Terminal 2 - Deploy Agent:
```bash
python Implant.py
```

### Terminal 3 - Interact with Agents:
```bash
python Controller.py
```

---

## Commands in Controller

```
agents          - List all connected agents
send <id> <cmd> - Send command to agent
interact <id>   - Interactive shell with agent
exit            - Exit controller
```

---

## Project Structure

```
ghostlink/
├── Listener.py          # C2 Server (Flask API)
├── Implant.py           # Agent/Beacon
├── Controller.py        # CLI Controller
├── utils.py             # Encoding & evasion utilities
├── encoding.py          # Multi-layer encoding schemes
├── persistence.py       # Cross-platform persistence
├── advanced.py          # Privilege escalation, lateral movement
├── loader.py            # Multi-stage loading
├── requirements.txt     # Python dependencies
├── config.template.py   # Configuration template
├── setup.sh             # Automated setup script
└── README.md            # Project documentation
```

---

## Configuration

Edit `config.template.py` to customize:
- C2 Server address
- Beacon interval
- Encoding scheme
- Persistence methods
- Evasion techniques

---

## Features

✅ Encrypted C2 Communication (Fernet AES-128-CBC)
✅ Multi-Layer Encoding (Fernet → Base64 → Hex)
✅ Cross-Platform Persistence (Windows/Linux/macOS)
✅ Advanced Evasion Techniques
✅ Privilege Escalation Detection
✅ Lateral Movement Capabilities
✅ Data Exfiltration Tools
✅ Multi-Stage Loading
✅ Interactive Command Execution

---

## Troubleshooting

**Port already in use:**
```bash
# Kill process using port 8888
lsof -i :8888 | grep -v COMMAND | awk '{print $2}' | xargs kill -9
```

**Dependencies not installing:**
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Agent not connecting:**
- Check `C2_SERVER` address in Implant.py
- Verify Listener.py is running
- Check firewall settings

---

## Security Notes

⚠️ **This tool is for authorized security testing only**
- Only use in controlled environments
- Obtain proper authorization before deployment
- Respect all applicable laws and regulations

---

## Support

For issues or questions, refer to QUICKSTART.md for detailed configuration options.
