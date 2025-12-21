"""
Attack detection modules.
Provides pattern matching and attack identification.
"""

from .http_attacks import HTTPAttackDetector
from .ssh_attacks import SSHAttackDetector

__all__ = ['HTTPAttackDetector', 'SSHAttackDetector']
