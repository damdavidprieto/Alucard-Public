"""
═══════════════════════════════════════════════════════════════════════════
SCANNER DETECTOR - Detección de Herramientas de Hacking
═══════════════════════════════════════════════════════════════════════════
Detecta y responde a herramientas de hacking conocidas mediante análisis
del User-Agent. Devuelve respuestas trampa específicas para cada tipo.
═══════════════════════════════════════════════════════════════════════════
"""

class ScannerDetector:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ DETECTOR DE HERRAMIENTAS DE HACKING                                     │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ QUÉ HACE: Analiza el User-Agent para detectar herramientas conocidas    │
    │ ESTRATEGIA:                                                              │
    │   1. Compara User-Agent contra firmas conocidas                         │
    │   2. Devuelve respuesta trampa específica para cada herramienta         │
    │   3. Si no detecta nada, devuelve None (continuar normal)               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ FIRMAS DE SCANNERS CONOCIDOS                                            │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Diccionario de herramientas de hacking y su descripción                 │
    # │ La clave es el string a buscar en el User-Agent (case-insensitive)      │
    # └─────────────────────────────────────────────────────────────────────────┘
    SCANNER_SIGNATURES = {
        'sqlmap': 'SQL Injection Tool',
        'nmap': 'Network Scanner',
        'nikto': 'Web Vulnerability Scanner',
        'gobuster': 'Directory Brute Forcer',
        'dirbuster': 'Directory Brute Forcer',
        'wpscan': 'WordPress Scanner',
        'burp': 'Burp Suite Proxy',
        'metasploit': 'Exploitation Framework',
        'nessus': 'Vulnerability Scanner',
        'acunetix': 'Web Vulnerability Scanner',
        'masscan': 'Port Scanner',
        'zap': 'OWASP ZAP Scanner',
    }
    
    @classmethod
    def detect(cls, user_agent: str) -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ MÉTODO PRINCIPAL DE DETECCIÓN                                       │
        ├─────────────────────────────────────────────────────────────────────┤
        │ PARÁMETROS:                                                          │
        │   user_agent: String del User-Agent HTTP                            │
        │                                                                      │
        │ RETORNA:                                                             │
        │   - Respuesta HTTP trampa si detecta scanner                        │
        │   - None si no detecta nada sospechoso                              │
        └─────────────────────────────────────────────────────────────────────┘
        """
        # Si no hay User-Agent, no podemos detectar nada
        if not user_agent:
            return None
        
        # Convertir a minúsculas para comparación case-insensitive
        ua_lower = user_agent.lower()
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ TRAMPA ESPECIAL 1: SQLMap                                       │
        # ├─────────────────────────────────────────────────────────────────┤
        # │ SQLMap busca SQL Injection, le damos un error SQL falso         │
        # │ para que piense que encontró una vulnerabilidad                 │
        # └─────────────────────────────────────────────────────────────────┘
        if 'sqlmap' in ua_lower:
            return cls._sqlmap_trap()
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ TRAMPA ESPECIAL 2: Otros Scanners                               │
        # ├─────────────────────────────────────────────────────────────────┤
        # │ Para otros scanners, simulamos un WAF (firewall) bloqueándolos  │
        # │ Esto hace que el atacante piense que hay seguridad activa       │
        # └─────────────────────────────────────────────────────────────────┘
        for scanner_signature in cls.SCANNER_SIGNATURES:
            if scanner_signature in ua_lower:
                return cls._waf_block()
        
        # No detectamos nada sospechoso
        return None
    
    @staticmethod
    def _sqlmap_trap() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ TRAMPA PARA SQLMAP                                                  │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Devuelve un error SQL falso para que SQLMap piense que encontró    │
        │ una vulnerabilidad de SQL Injection                                 │
        │                                                                      │
        │ EFECTO: El atacante perderá tiempo intentando explotar una BBDD     │
        │         que no existe                                               │
        └─────────────────────────────────────────────────────────────────────┘
        """
        return 'HTTP/1.1 500 Internal Server Error\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Database Error</h1><p>MySQL Error: Syntax error in query near \'\' limit 1\'</p></body></html>'
    
    @staticmethod
    def _waf_block() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ TRAMPA PARA SCANNERS GENERALES                                      │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Simula que un WAF (Web Application Firewall) bloqueó la petición   │
        │                                                                      │
        │ EFECTO: El atacante puede:                                          │
        │   - Pensar que hay seguridad activa y abandonar                     │
        │   - Intentar evadir el "WAF" (perdiendo tiempo)                     │
        └─────────────────────────────────────────────────────────────────────┘
        """
        return 'HTTP/1.1 403 Forbidden\r\nContent-Type: text/html\r\n\r\n<html><body><h1>WAF Blocked</h1><p>Suspicious activity detected.</p></body></html>'
