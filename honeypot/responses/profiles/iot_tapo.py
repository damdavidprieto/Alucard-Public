"""
═══════════════════════════════════════════════════════════════════════════
PERFIL IOT TAPO - TP-Link Tapo C200 (CLON EXACTO)
═══════════════════════════════════════════════════════════════════════════
Simula una cámara IP TP-Link Tapo C200.
Este dispositivo NO expone interfaz web, sino una API segura (HTTPS) 
que responde con JSON y errores 405/404 si se intenta acceder vía navegador.

PUERTOS CRÍTICOS:
- 443 (HTTPS): Responde JSON 405 Method Not Allowed
- 554 (RTSP): Pide autenticación Digest/Basic
- 2020 (ONVIF): Servicio de descubrimiento

CARACTERÍSTICAS DE ESTE PERFIL:
✅ Headers HTTP idénticos a la cámara real
✅ Respuesta JSON 405 en raiz
✅ Ausencia de interfaz web (para evitar fingerprints de honeypot obvios)
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL DISPOSITIVO
# ═══════════════════════════════════════════════════════════════════════════

IOT_DEVICE_BRAND = "TP-Link"
IOT_DEVICE_MODEL = "Tapo C200"

# ═══════════════════════════════════════════════════════════════════════════
# RESPUESTAS ESPECÍFICAS (CLONADAS)
# ═══════════════════════════════════════════════════════════════════════════

# RESPUESTA 405 METHOD NOT ALLOWED (La más común al navegar)
# Headers capturados de dispositivo real:
# < HTTP/1.1 405 Method Not Allowed
# < Connection: close
# < Cache-Control: no-cache
# < Content-Type: application/json;charset=UTF-8
# < Content-Length: 23
TAPO_405_RESPONSE = (
    "HTTP/1.1 405 Method Not Allowed\r\n"
    "Connection: close\r\n"
    "Cache-Control: no-cache\r\n"
    "Content-Type: application/json;charset=UTF-8\r\n"
    "Content-Length: 22\r\n"
    "\r\n"
    "{\"error_code\": -40401}"  # Body inferido o genérico para Tapo
)

# RESPUESTA 404 NOT FOUND (Para rutas inexistentes)
TAPO_404_RESPONSE = (
    "HTTP/1.1 404 Not Found\r\n"
    "Connection: close\r\n"
    "Cache-Control: no-cache\r\n"
    "Content-Type: application/json;charset=UTF-8\r\n"
    "Content-Length: 22\r\n"
    "\r\n"
    "{\"error_code\": -40405}"
)

# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS
# ═══════════════════════════════════════════════════════════════════════════

IOT_TAPO_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RAIZ (/)                                                                │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ La cámara real responde 405 si intentas GET /                           │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/': TAPO_405_RESPONSE,
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTAS COMUNES DE ESCANEO (Bloqueadas realisticamente)                   │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Cualquier intento de buscar panels de admin o configuración             │
    # │ recibe la respuesta JSON standard de la cámara.                         │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/admin': TAPO_404_RESPONSE,
    '/login': TAPO_404_RESPONSE,
    '/config': TAPO_404_RESPONSE,
    '/favicon.ico': TAPO_404_RESPONSE,
}
