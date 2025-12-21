"""
Response modules for the honeypot.
Provides fake endpoints and shell responses.
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS PRINCIPALES
# ═══════════════════════════════════════════════════════════════════════════
# Importamos desde endpoint_manager (nueva arquitectura modular)
# Esto reemplaza el antiguo http_endpoints.py

from .endpoint_manager import HTTPEndpoints
from .ssh_shell import FakeShell

__all__ = ['HTTPEndpoints', 'FakeShell']
