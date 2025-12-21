"""
HTTP attack detection module.
Identifies common web attack patterns.
"""

from typing import List, Dict


class HTTPAttackDetector:
    """Detector for HTTP-based attacks"""
    
    # Attack patterns
    SQL_INJECTION_PATTERNS = [
        'union select',
        "' or '1'='1",
        'drop table',
        'insert into',
        'delete from',
        'update set',
        '--',
        ';--'
    ]
    
    XSS_PATTERNS = [
        '<script>',
        'javascript:',
        'onerror=',
        'onload=',
        '<iframe',
        'alert(',
        'document.cookie'
    ]
    
    PATH_TRAVERSAL_PATTERNS = [
        '../',
        '..\\',
        '%2e%2e/',
        '%2e%2e\\',
        '..../'
    ]
    
    COMMAND_INJECTION_PATTERNS = [
        '|',
        ';',
        '&&',
        '||',
        '`',
        '$(',
        '${',
        '\n',
        '\r'
    ]
    
    @classmethod
    def detect(cls, request_data: str) -> List[str]:
        """
        Detect attacks in HTTP request data.
        
        Args:
            request_data: Raw HTTP request data
            
        Returns:
            List of detected attack types
        """
        detected = []
        data_lower = request_data.lower()
        
        # SQL Injection
        if any(pattern in data_lower for pattern in cls.SQL_INJECTION_PATTERNS):
            detected.append('sql_injection')
        
        # XSS
        if any(pattern in data_lower for pattern in cls.XSS_PATTERNS):
            detected.append('xss')
        
        # Path Traversal
        if any(pattern in request_data for pattern in cls.PATH_TRAVERSAL_PATTERNS):
            detected.append('path_traversal')
        
        # Command Injection
        if any(pattern in request_data for pattern in cls.COMMAND_INJECTION_PATTERNS):
            detected.append('command_injection')
        
        return detected
    
    @classmethod
    def get_attack_details(cls, attack_type: str, request_data: str) -> Dict:
        """
        Get detailed information about a detected attack.
        
        Args:
            attack_type: Type of attack
            request_data: Request data
            
        Returns:
            Dictionary with attack details
        """
        return {
            'type': attack_type,
            'severity': cls._get_severity(attack_type),
            'sample': request_data[:200]
        }
    
    @staticmethod
    def _get_severity(attack_type: str) -> str:
        """Get severity level for attack type"""
        severity_map = {
            'sql_injection': 'high',
            'command_injection': 'critical',
            'xss': 'medium',
            'path_traversal': 'medium'
        }
        return severity_map.get(attack_type, 'low')
