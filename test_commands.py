#!/usr/bin/env python3
"""
Test GhostLink C2 Framework
"""
import requests
import sqlite3
import time

C2_SERVER = "http://127.0.0.1:8888"

def send_command(agent_id, command):
    """Send command to agent"""
    response = requests.post(f"{C2_SERVER}/send_command", 
                            json={"agent_id": agent_id, "command": command})
    return response.status_code == 200

def get_results():
    """Get command results from database"""
    conn = sqlite3.connect('ghostlink.db')
    conn.row_factory = sqlite3.Row
    c = conn.cursor()
    
    c.execute("SELECT * FROM commands ORDER BY timestamp DESC LIMIT 10")
    commands = c.fetchall()
    conn.close()
    return commands

def main():
    print("\n" + "="*60)
    print("GhostLink C2 Framework - Test Suite")
    print("="*60)
    
    # Test commands
    test_commands = [
        "whoami",
        "pwd",
        "uname -a",
        "id"
    ]
    
    print("\n[*] Sending test commands...")
    for cmd in test_commands:
        if send_command("Agent_01", cmd):
            print(f"    ✓ Queued: {cmd}")
        else:
            print(f"    ✗ Failed to queue: {cmd}")
    
    print("\n[*] Waiting for execution (5 seconds)...")
    time.sleep(5)
    
    print("\n=== EXECUTION RESULTS ===\n")
    results = get_results()
    
    for cmd in results:
        status_emoji = "✓" if cmd['status'] == 'completed' else "⏳"
        print(f"{status_emoji} [{cmd['status'].upper():9}] {cmd['command']:<20}")
        if cmd['result']:
            result_lines = cmd['result'].strip().split('\n')
            for line in result_lines[:2]:  # Show first 2 lines
                print(f"           {line[:55]}")
            if len(result_lines) > 2:
                print(f"           ... ({len(result_lines)} lines total)")
        print()
    
    print("="*60)
    print("Test Complete!")
    print("="*60)

if __name__ == "__main__":
    main()
