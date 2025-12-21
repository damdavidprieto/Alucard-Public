"""
═══════════════════════════════════════════════════════════════════════════
PERFIL IOT - Dispositivos IoT y Routers (ULTRA-REALISTA)
═══════════════════════════════════════════════════════════════════════════
Simula un router TP-Link TL-WR841N con MÁXIMA CREDIBILIDAD.
Incluye páginas HTML auténticas, headers HTTP reales, y vulnerabilidades CVE.

MEJORAS SPRINT 1:
✅ Headers HTTP auténticos de TP-Link
✅ Páginas HTML/CSS reales del router
✅ Endpoints de configuración realistas
✅ Vulnerabilidades CVE conocidas
✅ MAC address con OUI de TP-Link
✅ Cookies de sesión realistas

MEJORAS SPRINT 2:
✅ Autenticación HTTP Basic
✅ Logo TP-Link en SVG
✅ Favicon específico de TP-Link
✅ 5 páginas adicionales de configuración
✅ Páginas de error personalizadas (404, 403, 500)

ARQUITECTURA:
- iot_helpers.py: Funciones auxiliares (headers, MAC, cookies, logo, favicon)
- iot_pages.py: Páginas HTML auténticas principales
- iot_pages_extra.py: Páginas adicionales (Sprint 2)
- iot_exploits.py: Respuestas a CVEs conocidos
- iot_auth.py: Sistema de autenticación HTTP Basic
- iot_errors.py: Páginas de error personalizadas
- iot.py: Este archivo (integración de todo)
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════

# Importar generador de endpoints comunes para dispositivos
from .common import get_device_common_endpoints

# Importar páginas HTML auténticas de TP-Link (Sprint 1)
from .iot_pages import (
    get_login_page,      # /userRpm/LoginRpm.htm
    get_index_page,      # /userRpm/Index.htm
    get_status_page,     # /userRpm/StatusRpm.htm
    get_wlan_security_page,  # /userRpm/WlanSecurityRpm.htm
    get_help_page        # /help/
)

# Importar páginas adicionales (Sprint 2)
from .iot_pages_extra import (
    get_menu_frame,      # /userRpm/MenuRpm.htm
    get_reboot_page,     # /userRpm/SysRebootRpm.htm
    get_statistics_page, # /userRpm/SystemStatisticRpm.htm
    get_system_log,      # /userRpm/SystemLogRpm.htm
    get_password_page    # /userRpm/PasswordRpm.htm
)

# Importar endpoints de exploits/vulnerabilidades
from .iot_exploits import get_exploit_endpoints

# Importar páginas de error (Sprint 2)
from .iot_errors import (
    get_404_error,
    get_403_error,
    get_500_error
)

# Importar favicon específico (Sprint 2)
from .iot_helpers import (
    get_tplink_favicon,
    build_tplink_response
)


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL DISPOSITIVO
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - TP-Link TL-WR841N es uno de los routers MÁS atacados del mundo
# - Firmware antiguo (2019) sugiere vulnerabilidades sin parchear
# - Estos valores se usan en TODAS las páginas para coherencia
# ═══════════════════════════════════════════════════════════════════════════

IOT_DEVICE_BRAND = "TP-Link"
IOT_DEVICE_MODEL = "TL-WR841N"
IOT_FIRMWARE_VERSION = "3.16.9 Build 20190208 Rel.58979n"


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS ESPECÍFICOS DE IOT (LEGACY)
# ═══════════════════════════════════════════════════════════════════════════
# NOTA: Estos son los endpoints originales del honeypot
# Los mantenemos para compatibilidad, pero ahora tenemos MUCHOS más
# ═══════════════════════════════════════════════════════════════════════════

IOT_LEGACY_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /cgi-bin/config.exp (Exploit CGI - LEGACY)                        │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Archivo de configuración expuesto (común en routers viejos)     │
    # │ TRAMPA: Devuelve credenciales falsas para atraer más ataques            │
    # │ REALISMO: Vulnerabilidad real en routers antiguos                       │
    # │ NOTA: Ahora usamos respuesta más realista desde iot_exploits.py         │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/cgi-bin/config.exp': 'HTTP/1.1 200 OK\r\nServer: TP-LINK Router WR841N\r\nContent-Type: text/plain\r\n\r\nadmin=root\npassword=admin',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /camera/stream (Stream de Cámara - LEGACY)                        │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Endpoint de streaming de cámara IP                              │
    # │ TRAMPA: Requiere autenticación (para capturar intentos)                 │
    # │ NOTA: Común en cámaras IP Hikvision, Dahua, etc.                        │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/camera/stream': 'HTTP/1.1 401 Unauthorized\r\nServer: TP-LINK Router WR841N\r\nContent-Type: text/html\r\n\r\n<h1>Camera Login</h1>',
}


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS AUTÉNTICOS DE TP-LINK
# ═══════════════════════════════════════════════════════════════════════════
# NOTA: Estos son los endpoints REALES del router TP-Link
# Generan HTML/CSS auténtico con información dinámica
# ═══════════════════════════════════════════════════════════════════════════

IOT_AUTHENTIC_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ PÁGINAS DE CONFIGURACIÓN AUTÉNTICAS                                     │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Estas rutas son EXACTAS del router TP-Link real                         │
    # │ HTML/CSS generado es idéntico al firmware original                      │
    # └─────────────────────────────────────────────────────────────────────────┘
    
    # PÁGINA DE LOGIN (la más importante)
    '/userRpm/LoginRpm.htm': get_login_page,
    
    # DASHBOARD PRINCIPAL (post-login)
    '/userRpm/Index.htm': get_index_page,
    
    # PÁGINA DE ESTADO
    '/userRpm/StatusRpm.htm': get_status_page,
    
    # CONFIGURACIÓN WIFI
    '/userRpm/WlanSecurityRpm.htm': get_wlan_security_page,
    
    # SISTEMA DE AYUDA
    '/help/': get_help_page,
    '/help/index.htm': get_help_page,
    
    # ┌───────────────────────────────────────────────────────────────────────────┐
    # │ PÁGINAS ADICIONALES (SPRINT 2)                                          │
    # └───────────────────────────────────────────────────────────────────────────┘
    '/userRpm/MenuRpm.htm': get_menu_frame,
    '/userRpm/SysRebootRpm.htm': get_reboot_page,
    '/userRpm/SystemStatisticRpm.htm': get_statistics_page,
    '/userRpm/SystemLogRpm.htm': get_system_log,
    '/userRpm/PasswordRpm.htm': get_password_page,
    
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ ARCHIVOS ESTÁTICOS (SPRINT 3 - FINGERPRINT REDUCTION)                   │
    # └─────────────────────────────────────────────────────────────────────────┘
    # Evitar 404s sospechosos para recursos comunes
    '/css/main.css': build_tplink_response("200 OK", "/* TP-Link CSS */", content_type="text/css"),
    '/css/login.css': build_tplink_response("200 OK", "/* Login CSS */", content_type="text/css"),
    '/js/jquery.js': build_tplink_response("200 OK", "// jQuery placeholder", content_type="application/javascript"),
    '/js/login.js': build_tplink_response("200 OK", "// Login logic", content_type="application/javascript"),
    '/img/logo.png': build_tplink_response("200 OK", "", content_type="image/png"),
}


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS COMPLETOS DE IOT
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - Fusionamos TODOS los tipos de endpoints:
#   1. Common device (/, /robots.txt, /favicon.ico, /humans.txt)
#   2. Authentic TP-Link pages (/userRpm/*, /help/)
#   3. Exploit endpoints (/cgi-bin/luci, /goform/*, CVEs)
#   4. Legacy endpoints (compatibilidad)
#
# RESULTADO: Router TP-Link ULTRA-REALISTA con 20+ endpoints
# ═══════════════════════════════════════════════════════════════════════════

IOT_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ PASO 1: ENDPOINTS COMUNES (de common/device.py)                         │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Incluye:                                                                 │
    # │   - / (Login page estilo router)                                        │
    # │   - /robots.txt (Disallow all)                                          │
    # │   - /favicon.ico (Favicon válido)                                       │
    # │   - /humans.txt (Info del fabricante)                                   │
    # └─────────────────────────────────────────────────────────────────────────┘
    **get_device_common_endpoints(
        device_brand=IOT_DEVICE_BRAND,
        device_model=IOT_DEVICE_MODEL,
        firmware_version=IOT_FIRMWARE_VERSION
    ),
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ PASO 2: PÁGINAS AUTÉNTICAS DE TP-LINK                                   │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Incluye:                                                                 │
    # │   - /userRpm/LoginRpm.htm (Login real)                                  │
    # │   - /userRpm/Index.htm (Dashboard)                                      │
    # │   - /userRpm/StatusRpm.htm (Estado)                                     │
    # │   - /userRpm/WlanSecurityRpm.htm (WiFi config)                          │
    # │   - /help/ (Sistema de ayuda)                                           │
    # └─────────────────────────────────────────────────────────────────────────┘
    **IOT_AUTHENTIC_ENDPOINTS,
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ PASO 3: ENDPOINTS DE EXPLOITS/VULNERABILIDADES                          │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Incluye:                                                                 │
    # │   - /cgi-bin/luci (OpenWrt Luci)                                        │
    # │   - /cgi?2 (Exploit conocido)                                           │
    # │   - /goform/formLogin (Form handler)                                    │
    # │   - /userRpm/PingIframeRpm.htm (CVE-2017-13772)                         │
    # │   - /admin (Auth bypass attempt)                                        │
    # └─────────────────────────────────────────────────────────────────────────┘
    **get_exploit_endpoints(),
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ PASO 4: ENDPOINTS LEGACY (compatibilidad)                               │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Mantenemos los endpoints originales del honeypot                        │
    # │ NOTA: Si hay conflicto de rutas, estos SOBRESCRIBEN los anteriores      │
    # └─────────────────────────────────────────────────────────────────────────┘
    **IOT_LEGACY_ENDPOINTS,
}


# ═══════════════════════════════════════════════════════════════════════════
# ESTADÍSTICAS Y DEBUGGING
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - Útil para verificar cuántos endpoints tenemos
# - Debugging durante desarrollo
# - Se puede comentar en producción
# ═══════════════════════════════════════════════════════════════════════════

# CONTAR: Total de endpoints por categoría
_COMMON_COUNT = len(get_device_common_endpoints(IOT_DEVICE_BRAND, IOT_DEVICE_MODEL, IOT_FIRMWARE_VERSION))
_AUTHENTIC_COUNT = len(IOT_AUTHENTIC_ENDPOINTS)
_EXPLOIT_COUNT = len(get_exploit_endpoints())
_LEGACY_COUNT = len(IOT_LEGACY_ENDPOINTS)
_TOTAL_COUNT = len(IOT_ENDPOINTS)

# NOTA DE DEBUGGING (visible en logs si se imprime)
# print(f"""
# ═══════════════════════════════════════════════════════════════════════════
# IOT PROFILE STATISTICS
# ═══════════════════════════════════════════════════════════════════════════
# Common endpoints:     {_COMMON_COUNT}
# Authentic TP-Link:    {_AUTHENTIC_COUNT}
# Exploit endpoints:    {_EXPLOIT_COUNT}
# Legacy endpoints:     {_LEGACY_COUNT}
# ───────────────────────────────────────────────────────────────────────────
# TOTAL ENDPOINTS:      {_TOTAL_COUNT}
# ═══════════════════════════════════════════════════════════════════════════
# """)


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿QUÉ CAMBIÓ EN ESTE ARCHIVO?
#    ANTES (versión básica):
#    - Solo 2 endpoints (/cgi-bin/config.exp, /camera/stream)
#    - Respuestas estáticas simples
#    - Sin headers auténticos
#    - Sin páginas HTML reales
#
#    AHORA (versión ultra-realista):
#    - 20+ endpoints auténticos
#    - Páginas HTML/CSS reales de TP-Link
#    - Headers HTTP idénticos a router real
#    - Vulnerabilidades CVE simuladas
#    - MAC address con OUI de TP-Link
#    - Cookies de sesión realistas
#    - Información dinámica (uptime, MAC, etc.)
#
# 2. ¿CÓMO ESTÁ ORGANIZADO EL CÓDIGO?
#    - iot.py: Integración (este archivo)
#    - iot_helpers.py: Utilidades (headers, MAC, cookies)
#    - iot_pages.py: Páginas HTML auténticas
#    - iot_exploits.py: Vulnerabilidades CVE
#    - common/device.py: Endpoints comunes de dispositivos
#
# 3. ¿QUÉ ENDPOINTS TENEMOS AHORA?
#    COMUNES (de device.py):
#    - /                          → Login page estilo router
#    - /robots.txt                → Disallow all
#    - /favicon.ico               → Favicon válido
#    - /humans.txt                → Info del fabricante
#
#    AUTÉNTICOS (de iot_pages.py):
#    - /userRpm/LoginRpm.htm      → Login real de TP-Link
#    - /userRpm/Index.htm         → Dashboard principal
#    - /userRpm/StatusRpm.htm     → Página de estado
#    - /userRpm/WlanSecurityRpm.htm → Config WiFi
#    - /help/                     → Sistema de ayuda
#
#    EXPLOITS (de iot_exploits.py):
#    - /cgi-bin/luci              → OpenWrt Luci
#    - /cgi?2                     → Exploit conocido
#    - /goform/formLogin          → Form handler
#    - /userRpm/PingIframeRpm.htm → CVE-2017-13772
#    - /admin                     → Auth bypass
#
#    LEGACY (compatibilidad):
#    - /cgi-bin/config.exp        → Exploit CGI original
#    - /camera/stream             → Stream de cámara
#
# 4. ¿CÓMO VERIFICAR QUE FUNCIONA?
#    - Abrir navegador: http://<honeypot>/userRpm/LoginRpm.htm
#    - Debería verse página de login idéntica a TP-Link
#    - Usar Nmap: nmap -sV -p80 <honeypot>
#    - Debería detectar "TP-LINK Router WR841N"
#    - Usar Routersploit para verificar exploits
#
# 5. ¿QUÉ TRÁFICO ESPERAMOS?
#    - Escaneos de Shodan/Censys (24/7)
#    - Intentos de login (admin/admin, root/root, etc.)
#    - Exploits automatizados (Mirai, Gafgyt)
#    - Herramientas de pentesting (Routersploit, Metasploit)
#    - Investigadores de seguridad
#
# 6. ¿CÓMO PERSONALIZAR PARA OTRO DISPOSITIVO?
#    - Cambiar IOT_DEVICE_BRAND, IOT_DEVICE_MODEL, IOT_FIRMWARE_VERSION
#    - Modificar iot_pages.py con HTML del nuevo dispositivo
#    - Actualizar iot_exploits.py con CVEs del nuevo dispositivo
#    - Ajustar iot_helpers.py si headers son diferentes
#
# 7. MEJORAS FUTURAS (Sprint 2 y 3):
#    - Logo TP-Link real en base64 (no texto)
#    - Más páginas de configuración (/userRpm/MenuRpm.htm, etc.)
#    - Archivos estáticos (/css/, /js/, /images/)
#    - Más CVEs (CVE-2019-7405, CVE-2020-9374)
#    - Respuestas UPnP/SSDP
#    - Logs del router simulados
#
# ═══════════════════════════════════════════════════════════════════════════
