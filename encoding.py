"""
Advanced encoding configuration and strategies
Provides intelligent encoding scheme selection and rotation
"""

import random
import json
from utils import EncodingSchemes


class AdvancedEncoding:
    """Advanced encoding with intelligent scheme selection"""
    
    # Encoding strategies
    SCHEMES = {
        "simple_base64": {
            "name": "Simple Base64",
            "encode": lambda data: EncodingSchemes.base64_encode(data),
            "decode": lambda data: EncodingSchemes.base64_decode(data),
            "strength": 1
        },
        "hex": {
            "name": "Hexadecimal",
            "encode": lambda data: EncodingSchemes.hex_encode(data),
            "decode": lambda data: EncodingSchemes.hex_decode(data),
            "strength": 2
        },
        "rot13": {
            "name": "ROT13",
            "encode": lambda data: EncodingSchemes.rot13_encode(data),
            "decode": lambda data: EncodingSchemes.rot13_encode(data),  # ROT13 reversible
            "strength": 2
        },
        "base64_hex": {
            "name": "Base64→Hex Chain",
            "encode": lambda data: EncodingSchemes.chain_encode(data, "base64_hex"),
            "decode": lambda data: EncodingSchemes.chain_decode(data, "base64_hex"),
            "strength": 3
        },
        "hex_rot13": {
            "name": "Hex→ROT13 Chain",
            "encode": lambda data: EncodingSchemes.chain_encode(data, "hex_rot13"),
            "decode": lambda data: EncodingSchemes.chain_decode(data, "hex_rot13"),
            "strength": 3
        },
        "base64_rot13": {
            "name": "Base64→ROT13 Chain",
            "encode": lambda data: EncodingSchemes.chain_encode(data, "base64_rot13"),
            "decode": lambda data: EncodingSchemes.chain_decode(data, "base64_rot13"),
            "strength": 3
        }
    }
    
    @staticmethod
    def select_scheme(strength="high", rotation=False):
        """
        Select encoding scheme based on required strength
        strength: "low" (1), "medium" (2), "high" (3)
        rotation: randomize scheme per session
        """
        strength_map = {
            "low": 1,
            "medium": 2,
            "high": 3
        }
        
        min_strength = strength_map.get(strength, 3)
        
        available = [
            name for name, config in AdvancedEncoding.SCHEMES.items()
            if config["strength"] >= min_strength
        ]
        
        if rotation:
            selected = random.choice(available)
        else:
            # Prefer highest strength
            selected = max(available, key=lambda x: AdvancedEncoding.SCHEMES[x]["strength"])
        
        return selected
    
    @staticmethod
    def get_scheme_info(scheme_name):
        """Get information about a specific scheme"""
        scheme = AdvancedEncoding.SCHEMES.get(scheme_name)
        if scheme:
            return {
                "name": scheme["name"],
                "strength": scheme["strength"],
                "type": "single" if "→" not in scheme["name"] else "chain"
            }
        return None
    
    @staticmethod
    def encode(data, scheme="base64_hex"):
        """Encode data using specified scheme"""
        if scheme not in AdvancedEncoding.SCHEMES:
            scheme = "base64_hex"  # Default to strongest
        
        try:
            return AdvancedEncoding.SCHEMES[scheme]["encode"](data)
        except Exception as e:
            print(f"[-] Encoding error with {scheme}: {e}")
            return EncodingSchemes.base64_encode(data)
    
    @staticmethod
    def decode(data, scheme="base64_hex"):
        """Decode data using specified scheme"""
        if scheme not in AdvancedEncoding.SCHEMES:
            scheme = "base64_hex"
        
        try:
            return AdvancedEncoding.SCHEMES[scheme]["decode"](data)
        except Exception as e:
            print(f"[-] Decoding error with {scheme}: {e}")
            try:
                return EncodingSchemes.base64_decode(data)
            except:
                return data


class AdaptiveEncoding:
    """
    Adaptive encoding that changes scheme based on:
    - Network conditions
    - Detection risk
    - Performance requirements
    """
    
    def __init__(self, session_id):
        self.session_id = session_id
        self.current_scheme = "base64_hex"  # Start with strongest
        self.scheme_history = []
        self.detection_risk = 0  # 0-100 scale
    
    def adapt_scheme(self, network_latency=None, suspected_detection=False):
        """
        Adapt encoding scheme based on current conditions
        """
        if suspected_detection:
            # High detection risk - switch to obfuscated scheme
            self.current_scheme = random.choice(["hex_rot13", "base64_rot13"])
            self.detection_risk = 80
        elif network_latency and network_latency > 5000:
            # High latency - use simpler scheme for faster encoding
            self.current_scheme = "hex"
            self.detection_risk = 40
        else:
            # Normal conditions - use strongest scheme
            self.current_scheme = "base64_hex"
            self.detection_risk = 20
        
        self.scheme_history.append({
            "timestamp": __import__('time').time(),
            "scheme": self.current_scheme,
            "risk_level": self.detection_risk
        })
        
        return self.current_scheme
    
    def rotate_scheme(self):
        """Rotate to different scheme (evasion)"""
        available = list(AdvancedEncoding.SCHEMES.keys())
        available.remove(self.current_scheme) if self.current_scheme in available else None
        
        self.current_scheme = random.choice(available)
        return self.current_scheme
    
    def get_status(self):
        """Get adaptive encoding status"""
        return {
            "current_scheme": self.current_scheme,
            "scheme_info": AdvancedEncoding.get_scheme_info(self.current_scheme),
            "detection_risk": self.detection_risk,
            "history_length": len(self.scheme_history)
        }


class PayloadObfuscator:
    """Obfuscate payloads with multiple encoding and encryption layers"""
    
    @staticmethod
    def obfuscate(payload, layers=3):
        """
        Apply multiple encoding layers
        layers: 1-3 (more layers = stronger obfuscation)
        """
        import base64
        from cryptography.fernet import Fernet
        
        data = payload
        
        for i in range(min(layers, 3)):
            if i == 0:
                # Layer 1: Fernet encryption
                key = b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ="
                f = Fernet(key)
                data = f.encrypt(data.encode() if isinstance(data, str) else data)
            elif i == 1:
                # Layer 2: Base64 encoding
                data = base64.b64encode(data).decode()
            elif i == 2:
                # Layer 3: Hex encoding
                data = EncodingSchemes.hex_encode(data)
        
        return data
    
    @staticmethod
    def deobfuscate(payload, layers=3):
        """Reverse obfuscation layers"""
        import base64
        from cryptography.fernet import Fernet
        
        data = payload
        
        for i in range(min(layers, 3) - 1, -1, -1):
            try:
                if i == 2:
                    # Reverse Layer 3: Hex decoding
                    data = EncodingSchemes.hex_decode(data)
                elif i == 1:
                    # Reverse Layer 2: Base64 decoding
                    data = base64.b64decode(data).decode()
                elif i == 0:
                    # Reverse Layer 1: Fernet decryption
                    key = b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ="
                    f = Fernet(key)
                    data = f.decrypt(data.encode()).decode()
            except Exception as e:
                print(f"[-] Deobfuscation layer {i} error: {e}")
                continue
        
        return data


def demonstrate_encoding():
    """Demonstrate all encoding schemes"""
    print("\n" + "="*70)
    print("ADVANCED ENCODING SCHEMES DEMONSTRATION")
    print("="*70 + "\n")
    
    test_data = "GhostLink_SecurePayload_12345"
    
    print(f"Original: {test_data}\n")
    
    for scheme_name, config in AdvancedEncoding.SCHEMES.items():
        print(f"[{config['name']}]")
        try:
            encoded = config["encode"](test_data)
            decoded = config["decode"](encoded)
            
            print(f"  Encoded: {encoded[:50]}..." if len(encoded) > 50 else f"  Encoded: {encoded}")
            print(f"  Decoded: {decoded}")
            print(f"  Strength: {'★' * config['strength']}")
            print()
        except Exception as e:
            print(f"  Error: {e}\n")
    
    # Demonstrate adaptive encoding
    print("\n[ADAPTIVE ENCODING EXAMPLE]")
    adapter = AdaptiveEncoding("session_12345")
    print(f"Initial scheme: {adapter.current_scheme}")
    
    adapter.adapt_scheme(suspected_detection=True)
    print(f"After detection risk: {adapter.current_scheme}")
    print(f"Status: {json.dumps(adapter.get_status(), indent=2)}")


if __name__ == "__main__":
    demonstrate_encoding()
