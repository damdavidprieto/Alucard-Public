"""
═══════════════════════════════════════════════════════════════════════════
DEVICE COMMON PROFILE - Dispositivos IoT y Routers
═══════════════════════════════════════════════════════════════════════════
Este generador crea endpoints comunes temáticos para simular dispositivos
IoT, routers, cámaras IP, y otros dispositivos embebidos.

USO:
- Routers (TP-Link, Netgear, D-Link, etc.)
- Cámaras IP
- NAS (Network Attached Storage)
- Dispositivos IoT embebidos

APARIENCIA:
- Página principal: Login page estilo router
- robots.txt: Disallow all (dispositivos no quieren crawlers)
- humans.txt: Información del fabricante
- Favicon: Logo del dispositivo

EFECTO PSICOLÓGICO:
El atacante piensa: "Dispositivo IoT = credenciales por defecto = fácil acceso"
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from ...utils.http_builder import HTTPResponseBuilder
from ...utils.dynamic_content import DynamicContentGenerator
from .base import (
    get_favicon_response,
    build_robots_txt,
    build_sitemap_xml
)


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE PÁGINA PRINCIPAL - DEVICE LOGIN
# ═══════════════════════════════════════════════════════════════════════════

def get_device_login_page(device_brand, device_model, firmware_version):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE LOGIN ESTILO ROUTER/DISPOSITIVO IoT                  │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - device_brand: Marca del dispositivo (ej: "TP-Link")                 │
    │   - device_model: Modelo (ej: "TL-WR841N")                              │
    │   - firmware_version: Versión de firmware (ej: "3.16.9 Build 20190208") │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener uptime del dispositivo (dinámico)                          │
    │   2. Construir HTML estilo login de router                              │
    │   3. Incluir formulario de autenticación                                │
    │   4. Mostrar info del dispositivo en footer                             │
    │                                                                          │
    │ REALISMO: Parece un router real con página de login típica              │
    │ TRAMPA: Formulario captura intentos de login                            │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # DATO DINÁMICO: Uptime del dispositivo
    uptime = DynamicContentGenerator.get_uptime_days()
    
    # HTML: Página de login estilo router
    # INSPIRADO EN: TP-Link, Netgear, D-Link routers
    body = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{device_brand} {device_model}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            background: #f0f0f0;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }}
        
        .login-container {{
            background: white;
            border-radius: 8px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            width: 400px;
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(to right, #1e3c72, #2a5298);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 24px;
            margin-bottom: 5px;
        }}
        
        .header p {{
            font-size: 14px;
            opacity: 0.9;
        }}
        
        .login-form {{
            padding: 30px;
        }}
        
        .form-group {{
            margin-bottom: 20px;
        }}
        
        .form-group label {{
            display: block;
            margin-bottom: 8px;
            color: #333;
            font-weight: bold;
            font-size: 14px;
        }}
        
        .form-group input {{
            width: 100%;
            padding: 12px;
            border: 1px solid #ddd;
            border-radius: 4px;
            font-size: 14px;
        }}
        
        .form-group input:focus {{
            outline: none;
            border-color: #2a5298;
        }}
        
        .login-button {{
            width: 100%;
            padding: 12px;
            background: linear-gradient(to right, #1e3c72, #2a5298);
            color: white;
            border: none;
            border-radius: 4px;
            font-size: 16px;
            font-weight: bold;
            cursor: pointer;
            transition: opacity 0.3s;
        }}
        
        .login-button:hover {{
            opacity: 0.9;
        }}
        
        .device-info {{
            background: #f8f8f8;
            padding: 20px;
            border-top: 1px solid #e0e0e0;
            font-size: 12px;
            color: #666;
        }}
        
        .device-info table {{
            width: 100%;
        }}
        
        .device-info td {{
            padding: 5px 0;
        }}
        
        .device-info td:first-child {{
            font-weight: bold;
            width: 40%;
        }}
        
        .warning {{
            background: #fff3cd;
            border: 1px solid #ffc107;
            color: #856404;
            padding: 10px;
            border-radius: 4px;
            margin-bottom: 20px;
            font-size: 13px;
        }}
    </style>
</head>
<body>
    <div class="login-container">
        <div class="header">
            <h1>{device_brand}</h1>
            <p>{device_model} Wireless Router</p>
        </div>
        
        <div class="login-form">
            <div class="warning">
                ⚠️ For security reasons, please change the default password after first login.
            </div>
            
            <form method="POST" action="/login">
                <div class="form-group">
                    <label for="username">Username:</label>
                    <input type="text" id="username" name="username" placeholder="admin" autocomplete="username">
                </div>
                
                <div class="form-group">
                    <label for="password">Password:</label>
                    <input type="password" id="password" name="password" placeholder="Enter password" autocomplete="current-password">
                </div>
                
                <button type="submit" class="login-button">Login</button>
            </form>
        </div>
        
        <div class="device-info">
            <table>
                <tr>
                    <td>Device Model:</td>
                    <td>{device_model}</td>
                </tr>
                <tr>
                    <td>Firmware Version:</td>
                    <td>{firmware_version}</td>
                </tr>
                <tr>
                    <td>Hardware Version:</td>
                    <td>V5.0</td>
                </tr>
                <tr>
                    <td>Uptime:</td>
                    <td>{uptime} days</td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>'''
    
    return HTTPResponseBuilder.build_html(f"{device_brand} {device_model}", body)


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE HUMANS.TXT - DEVICE
# ═══════════════════════════════════════════════════════════════════════════

def get_device_humans(device_brand, device_model, firmware_version):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR HUMANS.TXT PARA DISPOSITIVO IoT                                 │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - device_brand: Marca del dispositivo                                 │
    │   - device_model: Modelo del dispositivo                                │
    │   - firmware_version: Versión de firmware                               │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Construir humans.txt con info del fabricante                       │
    │   2. Mencionar modelo y firmware                                        │
    │   3. Incluir info de soporte técnico                                    │
    │                                                                          │
    │ EFECTO: Parece un dispositivo real con documentación oficial            │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    content = f'''/* DEVICE */
Manufacturer: {device_brand}
Model: {device_model}
Firmware: {firmware_version}
Type: Wireless Router

/* SUPPORT */
Contact: support [at] {device_brand.lower().replace(' ', '')}.com
Documentation: /help/
Manual: /manual.pdf

/* TECHNICAL */
Chipset: Atheros AR9341
RAM: 32MB
Flash: 4MB
Wireless: 802.11n 2.4GHz'''
    
    return HTTPResponseBuilder.build_text(content)


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL: OBTENER TODOS LOS ENDPOINTS COMUNES - DEVICE
# ═══════════════════════════════════════════════════════════════════════════

def get_device_common_endpoints(device_brand="TP-Link",
                                device_model="TL-WR841N",
                                firmware_version="3.16.9 Build 20190208"):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR DICCIONARIO COMPLETO DE ENDPOINTS COMUNES - DEVICE              │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS CONFIGURABLES:                                                │
    │   - device_brand: Marca (default: "TP-Link")                            │
    │   - device_model: Modelo (default: "TL-WR841N")                         │
    │   - firmware_version: Versión firmware (default: "3.16.9 Build...")     │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Crear diccionario con rutas comunes de dispositivos                │
    │   2. Configurar cada endpoint con parámetros del dispositivo            │
    │   3. Retornar diccionario completo                                      │
    │                                                                          │
    │ RETORNO: Diccionario {ruta: función_generadora}                         │
    │                                                                          │
    │ USO:                                                                     │
    │   from .common.device import get_device_common_endpoints                │
    │   IOT_ENDPOINTS = {                                                      │
    │       **get_device_common_endpoints(                                    │
    │           device_brand="Netgear",                                       │
    │           device_model="R6700",                                         │
    │           firmware_version="1.0.2.68"                                   │
    │       ),                                                                 │
    │       '/cgi-bin/config.exp': ...,  # Endpoints específicos IoT          │
    │   }                                                                      │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    return {
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: / (Página Principal)                                      │
        # │ FUNCIÓN: Lambda que llama get_device_login_page                 │
        # │ APARIENCIA: Login page estilo router                            │
        # └─────────────────────────────────────────────────────────────────┘
        '/': lambda: get_device_login_page(device_brand, device_model, firmware_version),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /robots.txt                                               │
        # │ CONFIGURACIÓN: Disallow ALL (dispositivos no quieren crawlers)  │
        # │ REALISMO: Los routers reales bloquean crawlers                  │
        # └─────────────────────────────────────────────────────────────────┘
        '/robots.txt': lambda: build_robots_txt(
            disallow_paths=['/'],  # Bloquear TODO
            allow_paths=[],        # No permitir nada
            crawl_delay=30,        # Delay alto (no queremos crawlers)
            include_sitemap=False  # Dispositivos no tienen sitemap
        ),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /favicon.ico                                              │
        # │ CONTENIDO: Favicon genérico (dispositivos suelen tener uno)     │
        # └─────────────────────────────────────────────────────────────────┘
        '/favicon.ico': get_favicon_response,
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /humans.txt                                               │
        # │ FUNCIÓN: Lambda que llama get_device_humans                     │
        # │ CONTENIDO: Info del fabricante y especificaciones técnicas      │
        # └─────────────────────────────────────────────────────────────────┘
        '/humans.txt': lambda: get_device_humans(device_brand, device_model, firmware_version),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ NOTA: Los dispositivos IoT NO suelen tener:                     │
        # │   - sitemap.xml (no necesitan SEO)                              │
        # │   - security.txt (no son empresas)                              │
        # │ Por eso NO los incluimos aquí                                   │
        # └─────────────────────────────────────────────────────────────────┘
    }


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ DEVICE PROFILE?
#    - Dispositivos IoT son objetivos MUY comunes
#    - Suelen tener credenciales por defecto (admin/admin)
#    - Firmware desactualizado con vulnerabilidades conocidas
#    - Atacantes buscan específicamente routers, cámaras, NAS
#
# 2. ¿POR QUÉ NO INCLUIR SITEMAP.XML NI SECURITY.TXT?
#    - Los dispositivos IoT NO son sitios web
#    - No necesitan SEO (sitemap.xml)
#    - No son empresas (security.txt)
#    - Incluirlos sería POCO REALISTA
#
# 3. ¿POR QUÉ ROBOTS.TXT CON DISALLOW ALL?
#    - Los routers reales bloquean crawlers
#    - No quieren aparecer en Google
#    - Es el comportamiento esperado
#
# 4. ¿CÓMO SE USA ESTE GENERADOR?
#    - En iot.py:
#      from .common.device import get_device_common_endpoints
#      IOT_ENDPOINTS = {
#          **get_device_common_endpoints(
#              device_brand="TP-Link",
#              device_model="TL-WR841N",
#              firmware_version="3.16.9 Build 20190208"
#          ),
#          '/cgi-bin/config.exp': ...,
#          '/camera/stream': ...,
#      }
#
# 5. ¿QUÉ DISPOSITIVOS PODEMOS SIMULAR?
#    - Routers: TP-Link, Netgear, D-Link, Linksys
#    - Cámaras IP: Hikvision, Dahua, Axis
#    - NAS: Synology, QNAP, WD MyCloud
#    - IoT: Smart home devices, thermostats, etc.
#
# 6. ¿POR QUÉ MOSTRAR FIRMWARE VERSION?
#    - Atacantes buscan versiones específicas con exploits conocidos
#    - Hace parecer el dispositivo más vulnerable
#    - Aumenta el interés del atacante
#
# ═══════════════════════════════════════════════════════════════════════════
