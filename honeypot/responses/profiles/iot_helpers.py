"""
═══════════════════════════════════════════════════════════════════════════
IOT HELPERS - Funciones auxiliares para respuestas IoT realistas
═══════════════════════════════════════════════════════════════════════════
Este módulo contiene utilidades específicas para simular dispositivos IoT
de forma ultra-realista, especialmente routers TP-Link.

CONTENIDO:
✅ Generador de headers HTTP auténticos de TP-Link
✅ Generador de direcciones MAC con OUI de TP-Link
✅ Generador de cookies de sesión realistas
✅ Constructor de respuestas HTTP con formato TP-Link
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
import random
import hashlib
from datetime import datetime
from ..utils.dynamic_content import DynamicContentGenerator


# ═══════════════════════════════════════════════════════════════════════════
# CONSTANTES DE TP-LINK
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - OUI (Organizationally Unique Identifier) = Primeros 3 bytes de MAC
# - TP-Link usa varios OUIs oficiales
# - Usarlos hace que el dispositivo parezca genuino
# ═══════════════════════════════════════════════════════════════════════════

TPLINK_OUI_PREFIXES = [
    "14:CC:20",  # TP-Link más común
    "50:C7:BF",  # TP-Link alternativo
    "C4:6E:1F",  # TP-Link TL-WR841N específico
    "EC:08:6B",  # TP-Link reciente
]


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE MAC ADDRESS
# ═══════════════════════════════════════════════════════════════════════════

def generate_tplink_mac():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR DIRECCIÓN MAC REALISTA DE TP-LINK                               │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Elegir OUI aleatorio de TP-Link                                    │
    │   2. Generar 3 bytes aleatorios para la parte única                     │
    │   3. Formatear como XX:XX:XX:XX:XX:XX                                   │
    │                                                                          │
    │ EJEMPLO: 14:CC:20:A3:B2:F1                                              │
    │          └─OUI─┘ └─Único──┘                                             │
    │                                                                          │
    │ REALISMO: Herramientas como Nmap detectarán "TP-Link" por el OUI        │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # PASO 1: Elegir OUI aleatorio de TP-Link
    oui = random.choice(TPLINK_OUI_PREFIXES)
    
    # PASO 2: Generar 3 bytes aleatorios (parte única del MAC)
    # EXPLICACIÓN PYTHON:
    # - random.randint(0, 255) = Número aleatorio entre 0 y 255
    # - format(num, '02X') = Convertir a hexadecimal con 2 dígitos
    # - Ejemplo: 175 → 'AF'
    unique_part = ":".join([
        format(random.randint(0, 255), '02X') for _ in range(3)
    ])
    
    # PASO 3: Combinar OUI + parte única
    return f"{oui}:{unique_part}"


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE COOKIES DE SESIÓN
# ═══════════════════════════════════════════════════════════════════════════

def generate_tplink_session_cookie():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR COOKIE DE SESIÓN REALISTA DE TP-LINK                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Generar Authorization cookie (Basic auth codificado)               │
    │   2. Generar subType cookie (tipo de interfaz)                          │
    │   3. Generar tLang cookie (idioma)                                      │
    │                                                                          │
    │ FORMATO REAL:                                                            │
    │   Authorization=Basic%20YWRtaW46YWRtaW4%3D                               │
    │   subType=pcSub                                                          │
    │   tLang=en                                                               │
    │                                                                          │
    │ REALISMO: Cookies idénticas a router TP-Link real                       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # COOKIE 1: Authorization (Basic auth para admin:admin en base64)
    # NOTA: "admin:admin" en base64 = "YWRtaW46YWRtaW4="
    # URL encoded: "Basic%20YWRtaW46YWRtaW4%3D"
    auth_cookie = "Authorization=Basic%20YWRtaW46YWRtaW4%3D; path=/"
    
    # COOKIE 2: subType (tipo de interfaz - PC vs móvil)
    subtype_cookie = "subType=pcSub; path=/"
    
    # COOKIE 3: tLang (idioma de la interfaz)
    lang_cookie = "tLang=en; path=/"
    
    # RETORNAR: String con todas las cookies separadas por newline
    # FORMATO HTTP: Cada Set-Cookie en su propia línea
    return f"Set-Cookie: {auth_cookie}\r\nSet-Cookie: {subtype_cookie}\r\nSet-Cookie: {lang_cookie}"


# ═══════════════════════════════════════════════════════════════════════════
# CONSTRUCTOR DE HEADERS HTTP AUTÉNTICOS
# ═══════════════════════════════════════════════════════════════════════════

def build_tplink_headers(content_type="text/html", include_auth=False):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUIR HEADERS HTTP AUTÉNTICOS DE TP-LINK                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - content_type: Tipo de contenido (default: text/html)                │
    │   - include_auth: Si incluir WWW-Authenticate header                    │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Construir headers básicos (Server, Date, Content-Type)             │
    │   2. Si include_auth, agregar WWW-Authenticate                          │
    │   3. Agregar Connection: close (comportamiento real)                    │
    │                                                                          │
    │ HEADERS REALES DE TP-LINK:                                              │
    │   Server: TP-LINK Router WR841N                                         │
    │   WWW-Authenticate: Basic realm="TP-LINK Wireless N Router WR841N"      │
    │   Content-Type: text/html                                               │
    │   Connection: close                                                     │
    │                                                                          │
    │ REALISMO: Idénticos a router real, detectables por Nmap/Shodan          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # HEADER 1: Server (identificación del dispositivo)
    # CRÍTICO: Este header es lo que Nmap/Shodan usan para identificar
    server_header = "Server: TP-LINK Router WR841N"
    
    # HEADER 2: Date (fecha actual en formato HTTP)
    # FORMATO: "Day, DD Mon YYYY HH:MM:SS GMT"
    # Ejemplo: "Sat, 14 Dec 2024 02:00:00 GMT"
    date_header = f"Date: {datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT')}"
    
    # HEADER 3: Content-Type
    content_type_header = f"Content-Type: {content_type}"
    
    # HEADER 4: Connection (TP-Link cierra conexión después de cada request)
    connection_header = "Connection: close"
    
    # CONSTRUIR: Lista de headers
    headers = [
        server_header,
        date_header,
        content_type_header,
        connection_header
    ]
    
    # HEADER OPCIONAL: WWW-Authenticate (para páginas que requieren login)
    if include_auth:
        # REALM: Texto que aparece en el popup de autenticación del navegador
        auth_header = 'WWW-Authenticate: Basic realm="TP-LINK Wireless N Router WR841N"'
        headers.insert(2, auth_header)  # Insertar después de Date
    
    # RETORNAR: Headers unidos con \r\n (formato HTTP)
    return "\r\n".join(headers)


# ═══════════════════════════════════════════════════════════════════════════
# CONSTRUCTOR DE RESPUESTAS HTTP COMPLETAS
# ═══════════════════════════════════════════════════════════════════════════

def build_tplink_response(status_code, body, content_type="text/html", 
                          include_auth=False, include_cookies=False):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUIR RESPUESTA HTTP COMPLETA CON FORMATO TP-LINK                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - status_code: Código HTTP (ej: "200 OK", "401 Unauthorized")         │
    │   - body: Contenido HTML/texto de la respuesta                          │
    │   - content_type: Tipo de contenido                                     │
    │   - include_auth: Si incluir WWW-Authenticate                           │
    │   - include_cookies: Si incluir cookies de sesión                       │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Construir status line (HTTP/1.1 200 OK)                            │
    │   2. Construir headers TP-Link                                          │
    │   3. Agregar Content-Length                                             │
    │   4. Opcionalmente agregar cookies                                      │
    │   5. Agregar body                                                       │
    │   6. Retornar respuesta completa                                        │
    │                                                                          │
    │ FORMATO HTTP:                                                            │
    │   HTTP/1.1 200 OK\r\n                                                    │
    │   Server: TP-LINK Router WR841N\r\n                                      │
    │   Content-Type: text/html\r\n                                            │
    │   Content-Length: 1234\r\n                                               │
    │   \r\n                                                                   │
    │   <html>...</html>                                                       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # PASO 1: Status line
    status_line = f"HTTP/1.1 {status_code}"
    
    # PASO 2: Headers TP-Link auténticos
    headers = build_tplink_headers(content_type, include_auth)
    
    # PASO 3: Content-Length (tamaño del body en bytes)
    # EXPLICACIÓN PYTHON:
    # - len(body.encode('utf-8')) = Tamaño en bytes (no caracteres)
    # - Importante para caracteres especiales que ocupan más de 1 byte
    content_length = f"Content-Length: {len(body.encode('utf-8'))}"
    
    # PASO 4: Construir respuesta completa
    response_parts = [
        status_line,
        headers,
        content_length
    ]
    
    # PASO 5: Agregar cookies si se solicita
    if include_cookies:
        cookies = generate_tplink_session_cookie()
        response_parts.append(cookies)
    
    # PASO 6: Agregar separador headers-body y el body
    # FORMATO HTTP: Línea vacía (\r\n\r\n) separa headers de body
    response = "\r\n".join(response_parts) + "\r\n\r\n" + body
    
    return response


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE INFORMACIÓN DEL DISPOSITIVO
# ═══════════════════════════════════════════════════════════════════════════

def get_device_info():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ OBTENER INFORMACIÓN TÉCNICA DEL DISPOSITIVO                             │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ RETORNA: Diccionario con información realista del router                │
    │                                                                          │
    │ DATOS INCLUIDOS:                                                         │
    │   - Hardware Version: WR841N v9 00000000                                │
    │   - Firmware Version: 3.16.9 Build 20190208 Rel.58979n                  │
    │   - MAC Address: Generado con OUI TP-Link                               │
    │   - LAN IP: 192.168.0.1 (default TP-Link)                               │
    │   - Uptime: Dinámico                                                    │
    │                                                                          │
    │ USO: Para insertar en páginas HTML de configuración                     │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    return {
        'hardware_version': 'WR841N v9 00000000',
        'firmware_version': '3.16.9 Build 20190208 Rel.58979n',
        'mac_address': generate_tplink_mac(),
        'lan_ip': '192.168.0.1',
        'wan_ip': '0.0.0.0',  # No conectado (realista para honeypot)
        'uptime': DynamicContentGenerator.get_uptime_days(),
        'model': 'TL-WR841N',
        'vendor': 'TP-LINK'
    }


# ═══════════════════════════════════════════════════════════════════════════
# LOGO TP-LINK EN SVG
# ═══════════════════════════════════════════════════════════════════════════

def get_tplink_logo_svg():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR LOGO TP-LINK EN SVG (BASE64)                                    │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ RETORNA: Data URI con logo SVG embebido                                 │
    │                                                                          │
    │ USO EN HTML:                                                             │
    │   <img src="{get_tplink_logo_svg()}" alt="TP-LINK">                     │
    │                                                                          │
    │ DISEÑO: Logo simplificado pero reconocible de TP-Link                   │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    import base64
    
    # SVG: Logo simplificado de TP-Link
    # COLORES: Azul oficial #00A0E9
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" width="180" height="40" viewBox="0 0 180 40">
  <defs>
    <style>
      .tp-text { fill: #00A0E9; font-family: Arial, sans-serif; font-weight: bold; }
    </style>
  </defs>
  
  <!-- Texto TP-LINK -->
  <text x="10" y="28" class="tp-text" font-size="24">TP-LINK</text>
  
  <!-- Línea decorativa -->
  <rect x="10" y="32" width="160" height="2" fill="#00A0E9"/>
</svg>'''
    
    # CODIFICAR: SVG a base64
    svg_base64 = base64.b64encode(svg.encode('utf-8')).decode('utf-8')
    
    # RETORNAR: Data URI completo
    return f"data:image/svg+xml;base64,{svg_base64}"


# ═══════════════════════════════════════════════════════════════════════════
# FAVICON TP-LINK
# ═══════════════════════════════════════════════════════════════════════════

def get_tplink_favicon():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR FAVICON ESPECÍFICO DE TP-LINK                                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ RETORNA: Respuesta HTTP completa con favicon ICO                        │
    │                                                                          │
    │ DISEÑO: Favicon 16x16 con colores TP-Link                               │
    │         - Fondo azul (#00A0E9)                                          │
    │         - Letras "TP" en blanco                                         │
    │                                                                          │
    │ NOTA: Usamos SVG convertido a ICO para simplicidad                      │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    import base64
    
    # SVG: Favicon simple con "TP"
    svg_favicon = '''<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" viewBox="0 0 16 16">
  <!-- Fondo azul TP-Link -->
  <rect width="16" height="16" fill="#00A0E9"/>
  
  <!-- Texto "TP" en blanco -->
  <text x="8" y="12" font-family="Arial" font-size="10" font-weight="bold" 
        fill="white" text-anchor="middle">TP</text>
</svg>'''
    
    # CODIFICAR: SVG a base64
    favicon_base64 = base64.b64encode(svg_favicon.encode('utf-8')).decode('utf-8')
    
    # CONVERTIR: Base64 a bytes para la respuesta
    # NOTA: En producción real, esto sería un archivo .ico
    # Para el honeypot, SVG embebido es suficiente
    favicon_data = f"data:image/svg+xml;base64,{favicon_base64}"
    
    # CONSTRUIR: Respuesta HTTP con favicon
    # NOTA: Usamos image/x-icon como content-type para compatibilidad
    response = f'''HTTP/1.1 200 OK\r
Server: TP-LINK Router WR841N\r
Content-Type: image/x-icon\r
Cache-Control: public, max-age=86400\r
Connection: close\r
Content-Length: {len(favicon_data)}\r
\r
{favicon_data}'''
    
    return response


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ ES IMPORTANTE EL OUI?
#    - Nmap identifica fabricantes por OUI
#    - Shodan/Censys indexan por OUI
#    - Atacantes verifican autenticidad por OUI
#    - Usar OUI correcto = +90% credibilidad
#
# 2. ¿POR QUÉ COOKIES ESPECÍFICAS?
#    - Routers TP-Link reales usan estas cookies exactas
#    - Herramientas de pentesting las reconocen
#    - Exploits automatizados las esperan
#
# 3. ¿POR QUÉ "Connection: close"?
#    - TP-Link no soporta keep-alive
#    - Cierra conexión después de cada request
#    - Comportamiento observable con Wireshark
#
# 4. ¿CÓMO VERIFICAR AUTENTICIDAD?
#    - Comparar con captures de Wireshark de router real
#    - Usar Burp Suite para analizar headers
#    - Consultar exploits públicos para formato esperado
#
# 5. ¿QUÉ HERRAMIENTAS DETECTAN ESTOS DETALLES?
#    - Nmap: Lee Server header y OUI
#    - Shodan: Indexa por Server header y favicon
#    - Routersploit: Verifica headers y cookies
#    - Metasploit: Compara con fingerprints conocidos
#
# 6. ¿POR QUÉ SVG PARA LOGO Y FAVICON?
#    - SVG es escalable y pequeño
#    - Fácil de embeber en base64
#    - No requiere archivos externos
#    - Suficiente para honeypot (no necesita perfección)
#
# ═══════════════════════════════════════════════════════════════════════════
