"""
SSH attack detection module.
Identifies SSH-based attacks and suspicious behavior.
"""

from typing import List, Dict


class SSHAttackDetector:
    """Detector for SSH-based attacks"""
    
    # Suspicious commands
    SUSPICIOUS_COMMANDS = [
        'wget',
        'curl',
        'nc',
        'netcat',
        'bash -i',
        '/dev/tcp',
        'python -c',
        'perl -e',
        'chmod +x',
        'rm -rf',
        'dd if=',
        'mkfs',
        '>',
        '>>',
        'base64',
        'uuencode'
    ]
    
    RECON_COMMANDS = [
        'uname',
        'whoami',
        'id',
        'ifconfig',
        'ip addr',
        'netstat',
        'ps aux',
        'cat /etc/passwd',
        'cat /etc/shadow',
        'ls -la'
    ]
    
    @classmethod
    def detect_command_attack(cls, command: str) -> List[str]:
        """
        Detect attacks in SSH commands.
        
        Args:
            command: Command executed
            
        Returns:
            List of detected attack types
        """
        detected = []
        command_lower = command.lower()
        
        # Check for suspicious commands
        if any(pattern in command_lower for pattern in cls.SUSPICIOUS_COMMANDS):
            detected.append('suspicious_command')
        
        # Check for reconnaissance
        if any(pattern in command_lower for pattern in cls.RECON_COMMANDS):
            detected.append('reconnaissance')
        
        return detected
    
    @classmethod
    def is_brute_force(cls, auth_attempts: int, threshold: int = 3) -> bool:
        """
        Detect brute force attempts.
        
        Args:
            auth_attempts: Number of authentication attempts
            threshold: Threshold for brute force
            
        Returns:
            True if brute force detected
        """
        return auth_attempts >= threshold
    
    @classmethod
    def get_attack_details(cls, attack_type: str, command: str = None) -> Dict:
        """
        Get detailed information about a detected attack.
        
        Args:
            attack_type: Type of attack
            command: Command executed (if applicable)
            
        Returns:
            Dictionary with attack details
        """
        return {
            'type': attack_type,
            'severity': cls._get_severity(attack_type),
            'command': command
        }
    
    @staticmethod
    def _get_severity(attack_type: str) -> str:
        """Get severity level for attack type"""
        severity_map = {
            'brute_force': 'high',
            'suspicious_command': 'critical',
            'reconnaissance': 'low'
        }
        return severity_map.get(attack_type, 'medium')
