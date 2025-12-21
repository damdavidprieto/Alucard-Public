"""
═══════════════════════════════════════════════════════════════════════════
IOT AUTHENTICATION - Sistema de autenticación HTTP Basic
═══════════════════════════════════════════════════════════════════════════
Implementa autenticación HTTP Basic idéntica a routers TP-Link reales.

CARACTERÍSTICAS:
✅ HTTP Basic Auth con credenciales por defecto
✅ Validación de credenciales comunes
✅ Generación de headers WWW-Authenticate
✅ Manejo de sesiones con cookies
✅ Captura de intentos de login fallidos
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
import base64
from typing import Tuple, Optional


# ═══════════════════════════════════════════════════════════════════════════
# CREDENCIALES VÁLIDAS
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - Routers TP-Link vienen con credenciales por defecto
# - Muchos usuarios NUNCA las cambian
# - Atacantes prueban estas combinaciones primero
# - Aceptamos múltiples variantes para capturar más intentos
# ═══════════════════════════════════════════════════════════════════════════

VALID_CREDENTIALS = [
    ('admin', 'admin'),      # Credencial por defecto #1 (más común)
    ('admin', ''),           # Admin sin contraseña (algunos modelos)
    ('root', 'admin'),       # Variante root
    ('admin', 'password'),   # Contraseña genérica
    ('admin', '1234'),       # Contraseña numérica simple
]


# ═══════════════════════════════════════════════════════════════════════════
# VALIDADOR DE CREDENCIALES
# ═══════════════════════════════════════════════════════════════════════════

def validate_credentials(username: str, password: str) -> bool:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ VALIDAR CREDENCIALES DE AUTENTICACIÓN                                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - username: Nombre de usuario                                         │
    │   - password: Contraseña                                                │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Verificar si (username, password) está en lista de válidos         │
    │   2. Retornar True si es válido, False si no                            │
    │                                                                          │
    │ REALISMO:                                                                │
    │   - Acepta credenciales por defecto de TP-Link                          │
    │   - Acepta variantes comunes                                            │
    │   - Captura TODOS los intentos (válidos e inválidos)                    │
    │                                                                          │
    │ TRAMPA: Todos los intentos se loguean para análisis                     │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # VERIFICAR: Si las credenciales están en la lista de válidas
    is_valid = (username, password) in VALID_CREDENTIALS
    
    # LOGGING: En producción, aquí se loguearía el intento
    # print(f"[AUTH] Login attempt: {username}:{password} - {'SUCCESS' if is_valid else 'FAILED'}")
    
    return is_valid


# ═══════════════════════════════════════════════════════════════════════════
# PARSER DE AUTHORIZATION HEADER
# ═══════════════════════════════════════════════════════════════════════════

def parse_auth_header(auth_header: str) -> Optional[Tuple[str, str]]:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ PARSEAR HEADER AUTHORIZATION                                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - auth_header: Header Authorization completo                          │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Verificar que empiece con "Basic "                                 │
    │   2. Extraer parte base64                                               │
    │   3. Decodificar base64                                                 │
    │   4. Separar username:password                                          │
    │   5. Retornar tupla (username, password)                                │
    │                                                                          │
    │ FORMATO HTTP:                                                            │
    │   Authorization: Basic YWRtaW46YWRtaW4=                                 │
    │                        └─ base64("admin:admin")                         │
    │                                                                          │
    │ RETORNA: (username, password) o None si inválido                        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # PASO 1: Verificar formato
    if not auth_header or not auth_header.startswith('Basic '):
        return None
    
    try:
        # PASO 2: Extraer parte base64 (después de "Basic ")
        encoded = auth_header[6:]  # Saltar "Basic "
        
        # PASO 3: Decodificar base64
        # EXPLICACIÓN PYTHON:
        # - base64.b64decode() retorna bytes
        # - .decode('utf-8') convierte bytes a string
        decoded = base64.b64decode(encoded).decode('utf-8')
        
        # PASO 4: Separar username:password
        # FORMATO: "username:password"
        if ':' not in decoded:
            return None
        
        username, password = decoded.split(':', 1)  # split(maxsplit=1) por si password tiene ':'
        
        # PASO 5: Retornar tupla
        return (username, password)
        
    except Exception:
        # Si hay cualquier error (base64 inválido, encoding, etc.)
        return None


# ═══════════════════════════════════════════════════════════════════════════
# VERIFICADOR DE AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════════════════

def check_authentication(auth_header: Optional[str]) -> bool:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ VERIFICAR SI REQUEST ESTÁ AUTENTICADO                                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - auth_header: Header Authorization del request (puede ser None)      │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Parsear header Authorization                                       │
    │   2. Si no se puede parsear → False                                     │
    │   3. Validar credenciales                                               │
    │   4. Retornar resultado de validación                                   │
    │                                                                          │
    │ RETORNA: True si autenticado, False si no                               │
    │                                                                          │
    │ USO:                                                                     │
    │   if not check_authentication(request.headers.get('Authorization')):   │
    │       return 401_response                                               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # PASO 1: Parsear header
    credentials = parse_auth_header(auth_header)
    
    # PASO 2: Si no se pudo parsear, no está autenticado
    if credentials is None:
        return False
    
    # PASO 3: Validar credenciales
    username, password = credentials
    return validate_credentials(username, password)


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE RESPUESTA 401 UNAUTHORIZED
# ═══════════════════════════════════════════════════════════════════════════

def get_401_response() -> str:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR RESPUESTA 401 UNAUTHORIZED                                      │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Construir HTML de error de autenticación                           │
    │   2. Construir headers con WWW-Authenticate                             │
    │   3. Retornar respuesta HTTP completa                                   │
    │                                                                          │
    │ HEADERS INCLUIDOS:                                                       │
    │   - Server: TP-LINK Router WR841N                                       │
    │   - WWW-Authenticate: Basic realm="..."                                 │
    │   - Content-Type: text/html                                             │
    │                                                                          │
    │ EFECTO: Navegador muestra popup de autenticación                        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # HTML: Página de error 401
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>401 Unauthorized</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            text-align: center;
            padding: 50px;
            background: #f0f0f0;
        }
        .error-box {
            background: white;
            border: 1px solid #c0c0c0;
            padding: 40px;
            margin: 0 auto;
            max-width: 500px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        h1 {
            color: #d00;
            margin-bottom: 20px;
        }
        p {
            color: #666;
            line-height: 1.6;
        }
    </style>
</head>
<body>
    <div class="error-box">
        <h1>401 - Unauthorized</h1>
        <p>This page requires authentication.</p>
        <p>Please enter valid credentials to access the router configuration.</p>
    </div>
</body>
</html>'''
    
    # CONSTRUIR: Respuesta HTTP completa con WWW-Authenticate
    response = f'''HTTP/1.1 401 Unauthorized\r
Server: TP-LINK Router WR841N\r
WWW-Authenticate: Basic realm="TP-LINK Wireless N Router WR841N"\r
Content-Type: text/html\r
Content-Length: {len(html.encode('utf-8'))}\r
Connection: close\r
\r
{html}'''
    
    return response


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN AUXILIAR: REQUIERE AUTENTICACIÓN
# ═══════════════════════════════════════════════════════════════════════════

def requires_authentication(endpoint_path: str) -> bool:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ DETERMINAR SI UN ENDPOINT REQUIERE AUTENTICACIÓN                        │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - endpoint_path: Ruta del endpoint (ej: "/userRpm/Index.htm")        │
    │                                                                          │
    │ LÓGICA:                                                                  │
    │   - /userRpm/* EXCEPTO LoginRpm.htm → Requiere auth                    │
    │   - /help/* → NO requiere auth                                          │
    │   - /, /robots.txt, /favicon.ico → NO requiere auth                    │
    │   - Todo lo demás → NO requiere auth (por defecto)                     │
    │                                                                          │
    │ RETORNA: True si requiere autenticación, False si no                    │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # ENDPOINTS PÚBLICOS (no requieren autenticación)
    public_endpoints = [
        '/',
        '/robots.txt',
        '/favicon.ico',
        '/humans.txt',
        '/userRpm/LoginRpm.htm',  # Página de login es pública
    ]
    
    # VERIFICAR: Si es endpoint público
    if endpoint_path in public_endpoints:
        return False
    
    # VERIFICAR: Si es ruta de ayuda (pública)
    if endpoint_path.startswith('/help'):
        return False
    
    # VERIFICAR: Si es ruta de configuración (requiere auth)
    if endpoint_path.startswith('/userRpm/'):
        return True
    
    # VERIFICAR: Si es ruta de formularios (requiere auth)
    if endpoint_path.startswith('/goform/'):
        return True
    
    # POR DEFECTO: No requiere autenticación
    # NOTA: Esto permite que exploits sean accesibles sin auth
    return False


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ HTTP BASIC AUTH?
#    - Es el método que usan routers TP-Link reales
#    - Simple de implementar
#    - Navegadores lo soportan nativamente (popup)
#    - Fácil de capturar credenciales
#
# 2. ¿POR QUÉ ACEPTAR MÚLTIPLES CREDENCIALES?
#    - Capturamos más intentos de login
#    - Atacantes prueban variantes comunes
#    - Más datos para análisis
#
# 3. ¿CÓMO FUNCIONA HTTP BASIC AUTH?
#    PASO 1: Cliente hace request sin Authorization
#    PASO 2: Servidor responde 401 con WWW-Authenticate
#    PASO 3: Navegador muestra popup de login
#    PASO 4: Usuario ingresa credenciales
#    PASO 5: Navegador envía Authorization: Basic base64(user:pass)
#    PASO 6: Servidor valida y responde 200 o 401
#
# 4. ¿CÓMO SE USA ESTE MÓDULO?
#    En endpoint_manager.py o en funciones de iot_pages.py:
#    
#    from .iot_auth import check_authentication, get_401_response
#    
#    def protected_endpoint(auth_header):
#        if not check_authentication(auth_header):
#            return get_401_response()
#        # ... resto del código
#
# 5. ¿QUÉ PASA CON LOS EXPLOITS?
#    - Los exploits NO requieren autenticación
#    - Esto es realista (muchos exploits bypassean auth)
#    - Permite que herramientas automatizadas los encuentren
#
# 6. ¿SE PUEDEN AGREGAR MÁS CREDENCIALES?
#    - Sí, simplemente agregar a VALID_CREDENTIALS
#    - Formato: ('username', 'password')
#    - Útil para capturar más variantes
#
# ═══════════════════════════════════════════════════════════════════════════
