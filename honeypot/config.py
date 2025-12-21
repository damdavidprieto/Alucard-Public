"""
Configuration file for the honeypot system.
Centralized configuration for all services and modules.
"""

# Network Configuration
HTTP_HOST = '0.0.0.0'
HTTP_PORT = 8080

SSH_HOST = '0.0.0.0'
SSH_PORT = 2222

# File Paths
LOG_FILE = 'honeypot.log'
SSH_HOST_KEY_FILE = '/app/ssh_host_key'

# Service Configuration
SOCKET_TIMEOUT = 30
SOCKET_BACKLOG = 5
BUFFER_SIZE = 4096

# SSH Configuration
SSH_KEY_SIZE = 2048
SSH_AUTH_ATTEMPTS_THRESHOLD = 2  # Accept after N attempts

# Logging Configuration
LOG_DATA_MAX_LENGTH = 500  # Max chars to log from data payload

# Geolocation Configuration
GEOLOCATION_TIMEOUT = 2  # seconds
GEOLOCATION_CACHE_ENABLED = True

# Honeypot Profile Configuration
# Options: 'all' (default), 'generic', 'wordpress', 'api', 'database', 'iot', 'devops'
# Can be overridden by env var: HONEYPOT_PROFILE=iot python main.py
import os
HONEYPOT_PROFILE = os.environ.get('HONEYPOT_PROFILE', 'all').lower()
