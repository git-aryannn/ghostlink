#!/usr/bin/env python3
"""
Verify Multi-Layer Encoding in GhostLink
"""
import json
import base64
from cryptography.fernet import Fernet
from utils import EncodingSchemes

ENCRYPTION_KEY = b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ="

def test_single_layer():
    """Test single-layer encoding (Fernet → Base64)"""
    print("\n" + "="*60)
    print("SINGLE-LAYER ENCODING (Fernet + Base64)")
    print("="*60)
    
    f = Fernet(ENCRYPTION_KEY)
    original = {"command": "whoami", "session": "test123"}
    
    # Encode
    json_data = json.dumps(original)
    encrypted = f.encrypt(json_data.encode())
    encoded = base64.b64encode(encrypted).decode()
    
    print(f"\n[Original]  {json_data}")
    print(f"[Encrypted] {str(encrypted[:50])}... ({len(encrypted)} bytes)")
    print(f"[Encoded]   {encoded[:80]}... ({len(encoded)} chars)")
    
    # Decode
    decoded_encrypted = base64.b64decode(encoded.encode())
    decrypted = f.decrypt(decoded_encrypted)
    result = json.loads(decrypted.decode())
    
    print(f"\n[Decoded]   {result}")
    print(f"✓ Match: {result == original}")
    
    return encoded


def test_multi_layer():
    """Test multi-layer encoding (Fernet → Base64 → Hex)"""
    print("\n" + "="*60)
    print("MULTI-LAYER ENCODING (Fernet → Base64 → Hex)")
    print("="*60)
    
    f = Fernet(ENCRYPTION_KEY)
    original = {"command": "whoami", "session": "test123"}
    
    # Encode with 3 layers
    json_data = json.dumps(original)
    print(f"\n[Layer 0 - Original]      {json_data}")
    
    encrypted = f.encrypt(json_data.encode())
    print(f"[Layer 1 - Fernet]        {str(encrypted[:40])}... ({len(encrypted)} bytes)")
    
    b64_encoded = base64.b64encode(encrypted).decode()
    print(f"[Layer 2 - Base64]        {b64_encoded[:60]}... ({len(b64_encoded)} chars)")
    
    hex_encoded = EncodingSchemes.hex_encode(b64_encoded)
    print(f"[Layer 3 - Hex Encoded]   {hex_encoded[:80]}... ({len(hex_encoded)} chars)")
    
    # Decode all layers
    print("\n[Decoding Process]")
    
    b64_decoded = EncodingSchemes.hex_decode(hex_encoded)
    print(f"  ✓ Hex decoded to Base64: {b64_decoded[:60]}...")
    
    encrypted_decoded = base64.b64decode(b64_decoded.encode())
    print(f"  ✓ Base64 decoded: {len(encrypted_decoded)} bytes")
    
    decrypted = f.decrypt(encrypted_decoded)
    result = json.loads(decrypted.decode())
    print(f"  ✓ Fernet decrypted: {result}")
    
    print(f"\n✓ Match: {result == original}")
    
    return hex_encoded


def compare_obfuscation():
    """Compare appearance of encodings"""
    print("\n" + "="*60)
    print("ENCODING OBFUSCATION COMPARISON")
    print("="*60)
    
    payload = "GhostLink_SecurePayload_12345"
    
    # Raw plaintext
    print(f"\n[Plaintext]  {payload}")
    print("  Risk: HIGH - Immediately visible to IDS/monitoring")
    
    # Base64 only
    b64 = base64.b64encode(payload.encode()).decode()
    print(f"\n[Base64 Only]  {b64}")
    print("  Risk: MEDIUM - Recognizable as base64 (common obfuscation)")
    print("  Signature: = padding, only [A-Za-z0-9+/=]")
    
    # Hex encoding
    hex_enc = EncodingSchemes.hex_encode(b64)
    print(f"\n[Hex Encoded]  {hex_enc[:60]}...")
    print("  Risk: LOW - Appears as random hex data")
    print("  Signature: Only [0-9a-f]")
    
    # ROT13
    rot13 = EncodingSchemes.rot13_encode(b64)
    print(f"\n[ROT13 Layer]  {rot13}")
    print("  Risk: LOW - Rotation cipher obfuscation")
    
    # Multi-layer
    multi = hex_enc + "..." # truncated
    print(f"\n[Multi-Layer]  {multi}")
    print("  Risk: VERY LOW - Triple obfuscation + encryption")
    print("  Detection: Extremely difficult without key")


def show_encoding_stats():
    """Show encoding statistics"""
    print("\n" + "="*60)
    print("ENCODING STATISTICS")
    print("="*60)
    
    test_data = {"command": "whoami", "agent": "Agent_01", "session": "abc123def456"}
    json_str = json.dumps(test_data)
    f = Fernet(ENCRYPTION_KEY)
    
    # Calculate sizes
    original_size = len(json_str)
    encrypted_size = len(f.encrypt(json_str.encode()))
    b64_size = len(base64.b64encode(f.encrypt(json_str.encode())).decode())
    hex_size = len(EncodingSchemes.hex_encode(base64.b64encode(f.encrypt(json_str.encode())).decode()))
    
    print(f"\n[Original JSON]        {original_size:>5} bytes")
    print(f"[+ Fernet Encryption]  {encrypted_size:>5} bytes  (+{encrypted_size-original_size} bytes, {(encrypted_size/original_size-1)*100:.1f}% overhead)")
    print(f"[+ Base64 Encoding]    {b64_size:>5} bytes  (+{b64_size-encrypted_size} bytes, {(b64_size/encrypted_size-1)*100:.1f}% overhead)")
    print(f"[+ Hex Encoding]       {hex_size:>5} bytes  (+{hex_size-b64_size} bytes, {(hex_size/b64_size-1)*100:.1f}% overhead)")
    print(f"\nTotal Overhead: {hex_size-original_size} bytes ({(hex_size/original_size-1)*100:.1f}%)")


if __name__ == "__main__":
    print("\n" + "█"*60)
    print("█  GhostLink v2.0 - Multi-Layer Encoding Verification")
    print("█"*60)
    
    test_single_layer()
    test_multi_layer()
    compare_obfuscation()
    show_encoding_stats()
    
    print("\n" + "█"*60)
    print("█  ENCODING VERIFICATION COMPLETE")
    print("█"*60 + "\n")
