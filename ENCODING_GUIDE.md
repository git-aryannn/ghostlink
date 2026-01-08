# Advanced Encoding Configuration Guide

## Overview

GhostLink v1.0 features **multi-layer encoding** with intelligent scheme selection for maximum stealth and detection evasion.

---

## Encoding Architecture

### Single-Layer Encoding
```
Plaintext → Encryption (Fernet) → Encoding (Base64/Hex/ROT13) → Transmission
```

### Multi-Layer Encoding (RECOMMENDED)
```
Plaintext → Fernet Encryption → Base64 → Hex → Transmission
Reversal: Transmission → Hex Decode → Base64 Decode → Fernet Decrypt → Plaintext
```

---

## Configuration Options

### 1. In Implant.py

```python
# Encoding scheme selection
ENCODING_SCHEME = "chain"  # Options: base64, hex, rot13, chain

# Enable multi-layer encoding (Fernet + Base64 + Hex)
USE_MULTILAYER_ENCODING = True
```

### 2. Available Schemes

| Scheme | Strength | Use Case |
|--------|----------|----------|
| `base64` | ⭐ | Basic, compatible |
| `hex` | ⭐⭐ | Good obfuscation |
| `rot13` | ⭐⭐ | Light obfuscation |
| `base64_hex` | ⭐⭐⭐ | Chained, strong |
| `hex_rot13` | ⭐⭐⭐ | Double obfuscation |
| `base64_rot13` | ⭐⭐⭐ | Double obfuscation |

---

## Quick Start Examples

### Example 1: Maximum Stealth (Recommended)

```python
ENCODING_SCHEME = "chain"
USE_MULTILAYER_ENCODING = True
ENABLE_EVASION = True
```

**What happens:**
1. Agent encrypts data with Fernet (AES-128)
2. Encodes with Base64
3. Encodes with Hex
4. Transmits (appears as hex string)
5. Server reverses: Hex → Base64 → Decrypt

---

### Example 2: High Performance

```python
ENCODING_SCHEME = "base64"
USE_MULTILAYER_ENCODING = False
```

**What happens:**
- Single-layer: Fernet → Base64
- Faster encoding/decoding
- Still encrypted and obfuscated

---

### Example 3: Maximum Obfuscation

```python
ENCODING_SCHEME = "hex"
USE_MULTILAYER_ENCODING = True
USE_ADAPTIVE_ENCODING = True  # Optional
```

**What happens:**
- Triple layer: Fernet → Base64 → Hex
- Highest obfuscation
- Scheme can rotate based on detection risk

---

## Advanced: Adaptive Encoding

Use the new `encoding.py` module for intelligent scheme rotation:

```python
from encoding import AdaptiveEncoding

# Initialize adaptive encoding
adapter = AdaptiveEncoding("session_id_123")

# Adapt scheme based on network conditions
if network_latency > 5000:
    adapter.adapt_scheme(network_latency=network_latency)
    current_scheme = adapter.current_scheme

# Rotate scheme when suspected detection
if suspected_detection:
    adapter.rotate_scheme()

# Get status
status = adapter.get_status()
print(f"Current: {status['current_scheme']}")
print(f"Risk: {status['detection_risk']}")
```

---

## Payload Obfuscation

Obfuscate payloads with multiple layers:

```python
from encoding import PayloadObfuscator

# Apply 3-layer obfuscation
obfuscated = PayloadObfuscator.obfuscate("secret_command", layers=3)
# Fernet → Base64 → Hex

# Reverse obfuscation
original = PayloadObfuscator.deobfuscate(obfuscated, layers=3)
```

---

## Real-World Example

### Configuration for Maximum Stealth

**In Implant.py:**
```python
ENABLE_EVASION = True
ENABLE_PERSISTENCE = False
ENCODING_SCHEME = "chain"           # Use chained encoding
USE_MULTILAYER_ENCODING = True      # Enable multi-layer (Fernet→B64→Hex)
BEACON_INTERVAL = 10                # Every 10 seconds
```

**Result:**
- Every beacon: New User-Agent, randomized interval ±3 sec
- Data transmission: Fernet encrypted → Base64 encoded → Hex encoded
- Network traffic: Appears as random hex strings
- File operations: Encrypted in memory

---

## Testing Your Encoding

### Test Encoding Module

```bash
cd GhostLink
python3 encoding.py

# Output:
# ADVANCED ENCODING SCHEMES DEMONSTRATION
# Original: GhostLink_SecurePayload_12345
# 
# [Simple Base64]
#   Encoded: R2hvc3RMaW5rX1NlY3VyZVBheWxvYWRfMTIzNDU=
#   Decoded: GhostLink_SecurePayload_12345
#   Strength: ★
# 
# [Base64→Hex Chain]
#   Encoded: 5237687...(long hex)
#   Decoded: GhostLink_SecurePayload_12345
#   Strength: ★★★
```

### Test with Server/Agent

```bash
# Terminal 1: Start server
python3 Listener.py

# Terminal 2: Start agent with advanced encoding
python3 Implant.py

# Terminal 3: Send command
python3 Controller.py
GhostLink> send Agent_01 "whoami"

# Check transmission (with verbose logging)
# You'll see multi-layer encoded data in transit
```

---

## Encoding Strength Comparison

### Single-Layer (Fernet only)
```
Pros: Lightweight, fast
Cons: Appears as base64 string (recognizable)
```

### Multi-Layer (Fernet→Base64→Hex)
```
Pros: 
  - Encrypted (Fernet/AES)
  - Obfuscated twice (Base64 + Hex)
  - Appears as random hex data
  - No string patterns visible
Cons: Slight performance overhead
```

### Adaptive (Dynamic scheme rotation)
```
Pros:
  - Changes scheme on detection risk
  - Maximum evasion
  - Intelligent adaptation
Cons:
  - Requires server support
  - More complex
```

---

## Performance Impact

| Encoding | CPU | Memory | Transmission |
|----------|-----|--------|--------------|
| Base64 only | <1% | 2-3MB | +25% |
| Base64→Hex | 1-2% | 4-5MB | +50% |
| Fernet+Base64→Hex | 2-3% | 5-7MB | +50% |
| Adaptive | 2-4% | 6-8MB | +60% |

**Note:** Overhead is minimal (milliseconds per encoding)

---

## Detection Evasion

### What the encoding hides:
✅ Plaintext command content
✅ String patterns (command names, file paths)
✅ Payload structure
✅ Encryption key (AES-128)
✅ Session tokens

### What it doesn't hide:
⚠️ Beacon timing patterns (use randomization)
⚠️ Destination IP/domain (use proxy)
⚠️ Packet sizes (use padding)
⚠️ Communication frequency (use jitter)

### Complete stealth (recommended settings):
```python
ENABLE_EVASION = True           # Random UA, jitter, sandbox detect
ENCODING_SCHEME = "chain"       # Multi-layer encoding
USE_MULTILAYER_ENCODING = True  # Fernet→B64→Hex
PROXY_SUPPORT = {               # Route through proxy
    "http": "socks5://proxy:port",
    "https": "socks5://proxy:port"
}
BEACON_INTERVAL = 10            # Will be randomized ±3 sec
```

---

## Troubleshooting

### Server can't decode agent data
**Problem:** Encoding scheme mismatch
**Solution:** Ensure server and agent use same encoding
```python
# Both should have:
ENCODING_SCHEME = "chain"
USE_MULTILAYER_ENCODING = True
```

### High latency/performance issues
**Problem:** Multi-layer encoding overhead
**Solution:** Reduce encoding complexity
```python
ENCODING_SCHEME = "base64"
USE_MULTILAYER_ENCODING = False
```

### Data appears corrupted
**Problem:** Decoder failing due to encoding errors
**Solution:** Server has fallback to simple base64
```python
# Listener.py automatically tries:
# 1. Multi-layer decode (Hex→B64→Decrypt)
# 2. Simple base64 decode
# 3. Direct decryption
```

---

## Best Practices

1. **Start with recommended settings** - use multi-layer encoding
2. **Test in lab environment** first before deployment
3. **Monitor performance** - adjust if overhead is too high
4. **Rotate schemes periodically** - use adaptive encoding
5. **Keep encryption key secure** - never hardcode in production
6. **Use proxies** - add network layer obfuscation
7. **Enable evasion** - combine with other techniques
8. **Monitor for detection** - watch for blocked connections

---

## Advanced Customization

Create custom encoding schemes:

```python
# In utils.py, add to EncodingSchemes class:
@staticmethod
def custom_encode(data):
    """Your custom encoding logic"""
    # Implement your algorithm
    return encoded_data

@staticmethod
def custom_decode(data):
    """Your custom decoding logic"""
    return decoded_data

# Then use:
custom = EncodingSchemes.custom_encode("data")
original = EncodingSchemes.custom_decode(custom)
```

---

## Summary

**Recommended Configuration:**
```python
ENCODING_SCHEME = "chain"              # Strong multi-layer
USE_MULTILAYER_ENCODING = True         # Fernet + Base64 + Hex
ENABLE_EVASION = True                  # Random UA, jitter, sandbox detect
PROXY_SUPPORT = {"http": "proxy:port"} # Route through proxy
```

This provides enterprise-grade stealth and evasion for authorized testing.

---

**For more information:** See [ENHANCEMENTS.md](ENHANCEMENTS.md) and [utils.py](utils.py)
