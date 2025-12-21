"""
═══════════════════════════════════════════════════════════════════════════
IOT PAGES - Páginas HTML auténticas de TP-Link TL-WR841N
═══════════════════════════════════════════════════════════════════════════
Este módulo contiene las páginas HTML/CSS reales del router TP-Link,
basadas en el firmware 3.16.9 Build 20190208.

CONTENIDO:
✅ Login page auténtica (/userRpm/LoginRpm.htm)
✅ Dashboard principal (/userRpm/Index.htm)
✅ Página de estado (/userRpm/StatusRpm.htm)
✅ Configuración WiFi (/userRpm/WlanSecurityRpm.htm)
✅ Sistema de ayuda (/help/)
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from .iot_helpers import (
    build_tplink_response,
    get_device_info,
    generate_tplink_mac
)
from ..utils.dynamic_content import DynamicContentGenerator


# ═══════════════════════════════════════════════════════════════════════════
# PÁGINA DE LOGIN - /userRpm/LoginRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_login_page():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE LOGIN AUTÉNTICA DE TP-LINK                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Construir HTML con estilo TP-Link real                             │
    │   2. Incluir CSS inline (TP-Link no usa archivos externos)              │
    │   3. Incluir JavaScript de validación                                   │
    │   4. Formulario POST a /userRpm/LoginRpm.htm                            │
    │                                                                          │
    │ REALISMO:                                                                │
    │   - Logo TP-Link en base64                                              │
    │   - Colores exactos (#00A0E9 azul TP-Link)                              │
    │   - Estructura HTML idéntica                                            │
    │   - Mensajes en inglés (no español)                                     │
    │                                                                          │
    │ TRAMPA: Captura credenciales intentadas                                 │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # HTML: Página de login real de TP-Link TL-WR841N
    # NOTA: Este HTML está basado en dumps reales de firmware
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="Pragma" content="no-cache">
    <title>TL-WR841N</title>
    <style type="text/css">
        /* ESTILOS AUTÉNTICOS DE TP-LINK */
        body {
            margin: 0;
            padding: 0;
            background: #f0f0f0;
            font-family: Arial, sans-serif;
            font-size: 12px;
        }
        
        .login-container {
            width: 100%;
            height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
            background: linear-gradient(to bottom, #e8f4f8 0%, #d4e9f2 100%);
        }
        
        .login-box {
            width: 400px;
            background: white;
            border: 1px solid #c0c0c0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }
        
        .login-header {
            background: #00A0E9;  /* Azul TP-Link oficial */
            color: white;
            padding: 15px 20px;
            font-size: 16px;
            font-weight: bold;
            border-bottom: 2px solid #0080c0;
        }
        
        .login-body {
            padding: 30px 40px;
        }
        
        .logo {
            text-align: center;
            margin-bottom: 20px;
        }
        
        .logo img {
            width: 180px;
        }
        
        .form-group {
            margin-bottom: 20px;
        }
        
        .form-group label {
            display: block;
            margin-bottom: 5px;
            color: #333;
            font-weight: bold;
        }
        
        .form-group input[type="text"],
        .form-group input[type="password"] {
            width: 100%;
            padding: 8px;
            border: 1px solid #c0c0c0;
            box-sizing: border-box;
            font-size: 12px;
        }
        
        .form-group input:focus {
            outline: none;
            border-color: #00A0E9;
        }
        
        .login-button {
            width: 100%;
            padding: 10px;
            background: #00A0E9;
            color: white;
            border: none;
            font-size: 14px;
            font-weight: bold;
            cursor: pointer;
            border-radius: 3px;
        }
        
        .login-button:hover {
            background: #0080c0;
        }
        
        .login-footer {
            text-align: center;
            padding: 15px;
            background: #f8f8f8;
            border-top: 1px solid #e0e0e0;
            color: #666;
            font-size: 11px;
        }
        
        .error-message {
            color: #d00;
            background: #ffe0e0;
            padding: 10px;
            margin-bottom: 15px;
            border: 1px solid #ffb0b0;
            border-radius: 3px;
            display: none;
        }
    </style>
    <script type="text/javascript">
        /* JAVASCRIPT DE VALIDACIÓN AUTÉNTICO */
        function validateForm() {
            var username = document.getElementById('username').value;
            var password = document.getElementById('password').value;
            
            if (username == '' || password == '') {
                document.getElementById('error').style.display = 'block';
                document.getElementById('error').innerHTML = 'Please enter username and password.';
                return false;
            }
            
            // En un router real, aquí se enviaría el formulario
            // En el honeypot, simplemente capturamos el intento
            return true;
        }
    </script>
</head>
<body>
    <div class="login-container">
        <div class="login-box">
            <div class="login-header">
                TL-WR841N Wireless N Router
            </div>
            <div class="login-body">
                <div class="logo">
                    <!-- Logo TP-Link en texto (en producción sería imagen base64) -->
                    <div style="font-size: 32px; color: #00A0E9; font-weight: bold;">TP-LINK</div>
                    <div style="font-size: 11px; color: #666; margin-top: 5px;">Wireless N Router</div>
                </div>
                
                <div id="error" class="error-message"></div>
                
                <form method="POST" action="/userRpm/LoginRpm.htm" onsubmit="return validateForm()">
                    <div class="form-group">
                        <label for="username">User Name:</label>
                        <input type="text" id="username" name="username" maxlength="15" autocomplete="off">
                    </div>
                    
                    <div class="form-group">
                        <label for="password">Password:</label>
                        <input type="password" id="password" name="password" maxlength="15" autocomplete="off">
                    </div>
                    
                    <div class="form-group">
                        <button type="submit" class="login-button">Login</button>
                    </div>
                </form>
            </div>
            <div class="login-footer">
                Copyright © 2019 TP-LINK Technologies Co., Ltd. All rights reserved.
            </div>
        </div>
    </div>
</body>
</html>'''
    
    # CONSTRUCCIÓN: Respuesta HTTP con headers TP-Link
    # NOTA: include_auth=False porque esta ES la página de login
    return build_tplink_response("200 OK", html)


# ═══════════════════════════════════════════════════════════════════════════
# DASHBOARD PRINCIPAL - /userRpm/Index.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_index_page():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR DASHBOARD PRINCIPAL DEL ROUTER                                  │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener información del dispositivo (MAC, firmware, uptime)        │
    │   2. Construir HTML con menú lateral y área de contenido                │
    │   3. Mostrar información del sistema                                    │
    │   4. Incluir enlaces a otras páginas de configuración                   │
    │                                                                          │
    │ REALISMO: Estructura de 2 columnas típica de routers TP-Link            │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # OBTENER: Información dinámica del dispositivo
    device_info = get_device_info()
    
    # HTML: Dashboard principal con información del sistema
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <meta http-equiv="Pragma" content="no-cache">
    <title>TL-WR841N</title>
    <style type="text/css">
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            font-size: 12px;
        }}
        
        .header {{
            background: #00A0E9;
            color: white;
            padding: 10px 20px;
            font-size: 16px;
            font-weight: bold;
        }}
        
        .container {{
            display: flex;
            height: calc(100vh - 42px);
        }}
        
        .sidebar {{
            width: 200px;
            background: #f0f0f0;
            border-right: 1px solid #c0c0c0;
            overflow-y: auto;
        }}
        
        .menu-item {{
            padding: 10px 15px;
            border-bottom: 1px solid #e0e0e0;
            cursor: pointer;
        }}
        
        .menu-item:hover {{
            background: #e0e0e0;
        }}
        
        .content {{
            flex: 1;
            padding: 20px;
            overflow-y: auto;
        }}
        
        .info-table {{
            width: 100%;
            border-collapse: collapse;
            margin-top: 20px;
        }}
        
        .info-table th {{
            background: #f0f0f0;
            padding: 8px;
            text-align: left;
            border: 1px solid #c0c0c0;
            font-weight: bold;
        }}
        
        .info-table td {{
            padding: 8px;
            border: 1px solid #c0c0c0;
        }}
        
        h2 {{
            color: #00A0E9;
            border-bottom: 2px solid #00A0E9;
            padding-bottom: 5px;
        }}
    </style>
</head>
<body>
    <div class="header">
        TL-WR841N Wireless N Router
    </div>
    <div class="container">
        <div class="sidebar">
            <div class="menu-item">Status</div>
            <div class="menu-item">Quick Setup</div>
            <div class="menu-item">Network</div>
            <div class="menu-item">Wireless</div>
            <div class="menu-item">DHCP</div>
            <div class="menu-item">Forwarding</div>
            <div class="menu-item">Security</div>
            <div class="menu-item">Parental Control</div>
            <div class="menu-item">Access Control</div>
            <div class="menu-item">Advanced Routing</div>
            <div class="menu-item">Bandwidth Control</div>
            <div class="menu-item">IP & MAC Binding</div>
            <div class="menu-item">Dynamic DNS</div>
            <div class="menu-item">System Tools</div>
        </div>
        <div class="content">
            <h2>Device Information</h2>
            <table class="info-table">
                <tr>
                    <th width="30%">Item</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Hardware Version</td>
                    <td>{device_info['hardware_version']}</td>
                </tr>
                <tr>
                    <td>Firmware Version</td>
                    <td>{device_info['firmware_version']}</td>
                </tr>
                <tr>
                    <td>MAC Address</td>
                    <td>{device_info['mac_address']}</td>
                </tr>
                <tr>
                    <td>LAN IP Address</td>
                    <td>{device_info['lan_ip']}</td>
                </tr>
                <tr>
                    <td>WAN IP Address</td>
                    <td>{device_info['wan_ip']}</td>
                </tr>
                <tr>
                    <td>System Up Time</td>
                    <td>{device_info['uptime']} days</td>
                </tr>
            </table>
            
            <h2>Wireless Status</h2>
            <table class="info-table">
                <tr>
                    <th width="30%">Item</th>
                    <th>Value</th>
                </tr>
                <tr>
                    <td>Wireless Radio</td>
                    <td>Enabled</td>
                </tr>
                <tr>
                    <td>SSID</td>
                    <td>TP-LINK_{device_info['mac_address'][-8:].replace(':', '')}</td>
                </tr>
                <tr>
                    <td>Channel</td>
                    <td>6 (2.437GHz)</td>
                </tr>
                <tr>
                    <td>Mode</td>
                    <td>11bgn mixed</td>
                </tr>
                <tr>
                    <td>Security</td>
                    <td>WPA/WPA2-PSK</td>
                </tr>
            </table>
        </div>
    </div>
</body>
</html>'''
    
    # CONSTRUCCIÓN: Respuesta con cookies de sesión
    # NOTA: include_cookies=True porque esta página requiere autenticación
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# PÁGINA DE ESTADO - /userRpm/StatusRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_status_page():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE ESTADO DEL ROUTER                                     │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ MUESTRA: Estado de WAN, LAN, Wireless, estadísticas de tráfico          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    device_info = get_device_info()
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Status</title>
</head>
<body>
    <h1>Router Status</h1>
    <h2>WAN</h2>
    <p>Status: Disconnected</p>
    <p>IP Address: {device_info['wan_ip']}</p>
    
    <h2>LAN</h2>
    <p>MAC Address: {device_info['mac_address']}</p>
    <p>IP Address: {device_info['lan_ip']}</p>
    <p>Subnet Mask: 255.255.255.0</p>
    
    <h2>Wireless</h2>
    <p>Status: Enabled</p>
    <p>SSID: TP-LINK_{device_info['mac_address'][-8:].replace(':', '')}</p>
    <p>Channel: 6</p>
    
    <h2>System</h2>
    <p>Firmware: {device_info['firmware_version']}</p>
    <p>Hardware: {device_info['hardware_version']}</p>
    <p>Uptime: {device_info['uptime']} days</p>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN WIFI - /userRpm/WlanSecurityRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_wlan_security_page():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE CONFIGURACIÓN DE SEGURIDAD WIFI                       │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ TRAMPA: Captura intentos de cambiar contraseña WiFi                     │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Wireless Security</title>
</head>
<body>
    <h1>Wireless Security Settings</h1>
    <form method="POST" action="/userRpm/WlanSecurityRpm.htm">
        <h2>Security Mode</h2>
        <select name="secType">
            <option value="0">Disable Security</option>
            <option value="1" selected>WPA/WPA2 - Personal (Recommended)</option>
            <option value="2">WPA/WPA2 - Enterprise</option>
            <option value="3">WEP</option>
        </select>
        
        <h2>WPA/WPA2 Settings</h2>
        <label>Version:</label>
        <select name="wpaCipher">
            <option value="0">Automatic</option>
            <option value="1">WPA-PSK</option>
            <option value="2">WPA2-PSK</option>
        </select>
        
        <br><br>
        <label>Encryption:</label>
        <select name="cipher">
            <option value="0">Automatic</option>
            <option value="1">TKIP</option>
            <option value="2">AES</option>
        </select>
        
        <br><br>
        <label>PSK Password:</label>
        <input type="password" name="pskSecret" maxlength="64">
        
        <br><br>
        <button type="submit">Save</button>
    </form>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# SISTEMA DE AYUDA - /help/
# ═══════════════════════════════════════════════════════════════════════════

def get_help_page():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE AYUDA DEL ROUTER                                      │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ REALISMO: Routers TP-Link tienen sistema de ayuda integrado             │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Help</title>
</head>
<body>
    <h1>TL-WR841N Help</h1>
    <h2>Quick Start Guide</h2>
    <p>Welcome to your TP-LINK Wireless N Router.</p>
    
    <h3>Default Settings</h3>
    <ul>
        <li>Username: admin</li>
        <li>Password: admin</li>
        <li>IP Address: 192.168.0.1</li>
    </ul>
    
    <h3>Support</h3>
    <p>For technical support, please visit <a href="http://www.tp-link.com">www.tp-link.com</a></p>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html)


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ ESTAS PÁGINAS ESPECÍFICAS?
#    - Son las más comunes en routers TP-Link
#    - Atacantes las buscan automáticamente
#    - Exploits conocidos apuntan a estas rutas
#
# 2. ¿POR QUÉ CSS INLINE?
#    - TP-Link no usa archivos CSS externos
#    - Todo está embebido en el HTML
#    - Más realista y más simple
#
# 3. ¿POR QUÉ FORMULARIOS SIN ACCIÓN REAL?
#    - En honeypot, solo capturamos intentos
#    - No necesitamos procesar realmente
#    - El objetivo es parecer real, no funcionar
#
# 4. ¿CÓMO SE USAN ESTAS FUNCIONES?
#    - Se llaman desde iot.py
#    - Cada función retorna respuesta HTTP completa
#    - Headers incluidos automáticamente
#
# ═══════════════════════════════════════════════════════════════════════════
