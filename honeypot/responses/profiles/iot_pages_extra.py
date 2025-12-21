"""
═══════════════════════════════════════════════════════════════════════════
IOT PAGES EXTRA - Páginas adicionales de configuración (Sprint 2)
═══════════════════════════════════════════════════════════════════════════
Páginas adicionales de configuración del router TP-Link TL-WR841N.

CONTENIDO:
✅ Menu frame (/userRpm/MenuRpm.htm)
✅ System reboot (/userRpm/SysRebootRpm.htm)
✅ System statistics (/userRpm/SystemStatisticRpm.htm)
✅ System log (/userRpm/SystemLogRpm.htm)
✅ Change password (/userRpm/PasswordRpm.htm)
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from .iot_helpers import build_tplink_response, get_device_info
from ..utils.dynamic_content import DynamicContentGenerator
import random


# ═══════════════════════════════════════════════════════════════════════════
# MENU FRAME - /userRpm/MenuRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_menu_frame():
    """Menú lateral del router (usado en frameset)"""
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Menu</title>
    <style>
        body {
            margin: 0;
            padding: 10px;
            font-family: Arial, sans-serif;
            font-size: 12px;
            background: #f0f0f0;
        }
        .menu-section {
            margin-bottom: 10px;
        }
        .menu-title {
            background: #00A0E9;
            color: white;
            padding: 5px 10px;
            font-weight: bold;
            cursor: pointer;
        }
        .menu-item {
            padding: 5px 20px;
            border-bottom: 1px solid #e0e0e0;
            background: white;
        }
        .menu-item:hover {
            background: #e8f4f8;
        }
        a {
            color: #333;
            text-decoration: none;
        }
    </style>
</head>
<body>
    <div class="menu-section">
        <div class="menu-title">Status</div>
        <div class="menu-item"><a href="/userRpm/StatusRpm.htm" target="mainFrame">Router Status</a></div>
    </div>
    <div class="menu-section">
        <div class="menu-title">Network</div>
        <div class="menu-item"><a href="/userRpm/Index.htm" target="mainFrame">WAN Settings</a></div>
    </div>
    <div class="menu-section">
        <div class="menu-title">Wireless</div>
        <div class="menu-item"><a href="/userRpm/WlanSecurityRpm.htm" target="mainFrame">Wireless Security</a></div>
    </div>
    <div class="menu-section">
        <div class="menu-title">System Tools</div>
        <div class="menu-item"><a href="/userRpm/PasswordRpm.htm" target="mainFrame">Password</a></div>
        <div class="menu-item"><a href="/userRpm/SystemLogRpm.htm" target="mainFrame">System Log</a></div>
        <div class="menu-item"><a href="/userRpm/SystemStatisticRpm.htm" target="mainFrame">Statistics</a></div>
        <div class="menu-item"><a href="/userRpm/SysRebootRpm.htm" target="mainFrame">Reboot</a></div>
    </div>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# SYSTEM REBOOT - /userRpm/SysRebootRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_reboot_page():
    """Página de reinicio del router"""
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>System Reboot</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        .warning {
            background: #fff3cd;
            border: 1px solid #ffc107;
            padding: 15px;
            margin: 20px 0;
            border-radius: 5px;
        }
        .reboot-button {
            background: #00A0E9;
            color: white;
            padding: 10px 30px;
            border: none;
            font-size: 14px;
            cursor: pointer;
            border-radius: 3px;
        }
        .reboot-button:hover {
            background: #0080c0;
        }
    </style>
</head>
<body>
    <h1>System Reboot</h1>
    <div class="warning">
        <strong>Warning:</strong> Rebooting the router will temporarily interrupt network connectivity.
        All current connections will be lost.
    </div>
    <p>Click the button below to reboot the router:</p>
    <form method="POST" action="/userRpm/SysRebootRpm.htm">
        <button type="submit" class="reboot-button">Reboot Router</button>
    </form>
    <p><small>The reboot process will take approximately 30 seconds.</small></p>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# SYSTEM STATISTICS - /userRpm/SystemStatisticRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_statistics_page():
    """Página de estadísticas del sistema"""
    # Generar estadísticas falsas pero realistas
    packets_sent = random.randint(100000, 999999)
    packets_received = random.randint(100000, 999999)
    bytes_sent = random.randint(1000000000, 9999999999)
    bytes_received = random.randint(1000000000, 9999999999)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>System Statistics</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}
        th, td {{
            padding: 10px;
            border: 1px solid #c0c0c0;
            text-align: left;
        }}
        th {{
            background: #f0f0f0;
            font-weight: bold;
        }}
        h2 {{
            color: #00A0E9;
            border-bottom: 2px solid #00A0E9;
            padding-bottom: 5px;
        }}
    </style>
</head>
<body>
    <h1>System Statistics</h1>
    
    <h2>WAN Statistics</h2>
    <table>
        <tr>
            <th>Item</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Packets Sent</td>
            <td>{packets_sent:,}</td>
        </tr>
        <tr>
            <td>Packets Received</td>
            <td>{packets_received:,}</td>
        </tr>
        <tr>
            <td>Bytes Sent</td>
            <td>{bytes_sent:,} bytes ({bytes_sent / 1024 / 1024:.2f} MB)</td>
        </tr>
        <tr>
            <td>Bytes Received</td>
            <td>{bytes_received:,} bytes ({bytes_received / 1024 / 1024:.2f} MB)</td>
        </tr>
    </table>
    
    <h2>LAN Statistics</h2>
    <table>
        <tr>
            <th>Item</th>
            <th>Value</th>
        </tr>
        <tr>
            <td>Active Connections</td>
            <td>{random.randint(1, 10)}</td>
        </tr>
        <tr>
            <td>DHCP Clients</td>
            <td>{random.randint(1, 5)}</td>
        </tr>
    </table>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# SYSTEM LOG - /userRpm/SystemLogRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_system_log():
    """Página de logs del sistema"""
    # Generar logs falsos pero realistas
    from datetime import datetime, timedelta
    
    logs = []
    base_time = datetime.now()
    
    log_messages = [
        ("INFO", "System started successfully"),
        ("INFO", "WAN connection established"),
        ("INFO", "DHCP server started"),
        ("INFO", "Wireless network enabled"),
        ("WARN", "Failed login attempt from 192.168.0.100"),
        ("INFO", "Firmware check completed"),
        ("INFO", "Time synchronized with NTP server"),
    ]
    
    for i, (level, message) in enumerate(log_messages):
        timestamp = (base_time - timedelta(hours=i*2)).strftime("%Y-%m-%d %H:%M:%S")
        logs.append(f"<tr><td>{timestamp}</td><td>{level}</td><td>{message}</td></tr>")
    
    logs_html = "\n".join(logs)
    
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>System Log</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            padding: 20px;
        }}
        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 12px;
        }}
        th, td {{
            padding: 8px;
            border: 1px solid #c0c0c0;
            text-align: left;
        }}
        th {{
            background: #f0f0f0;
            font-weight: bold;
        }}
        .log-info {{ color: #00A0E9; }}
        .log-warn {{ color: #ff9800; }}
        .log-error {{ color: #d00; }}
    </style>
</head>
<body>
    <h1>System Log</h1>
    <p>Displaying recent system events:</p>
    <table>
        <tr>
            <th>Timestamp</th>
            <th>Level</th>
            <th>Message</th>
        </tr>
        {logs_html}
    </table>
    <p><small>Log entries are stored for 7 days.</small></p>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# CHANGE PASSWORD - /userRpm/PasswordRpm.htm
# ═══════════════════════════════════════════════════════════════════════════

def get_password_page():
    """Página de cambio de contraseña"""
    html = '''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>Change Password</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            padding: 20px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: inline-block;
            width: 150px;
            font-weight: bold;
        }
        input[type="password"] {
            padding: 5px;
            width: 200px;
            border: 1px solid #c0c0c0;
        }
        .save-button {
            background: #00A0E9;
            color: white;
            padding: 8px 25px;
            border: none;
            cursor: pointer;
            border-radius: 3px;
            margin-left: 150px;
        }
        .save-button:hover {
            background: #0080c0;
        }
        .info {
            background: #e8f4f8;
            border: 1px solid #00A0E9;
            padding: 10px;
            margin: 20px 0;
            border-radius: 5px;
        }
    </style>
</head>
<body>
    <h1>Change Administrator Password</h1>
    <div class="info">
        <strong>Note:</strong> It is strongly recommended to change the default password to protect your router.
    </div>
    <form method="POST" action="/userRpm/PasswordRpm.htm">
        <div class="form-group">
            <label for="oldPassword">Old Password:</label>
            <input type="password" id="oldPassword" name="oldPassword" maxlength="15">
        </div>
        <div class="form-group">
            <label for="newPassword">New Password:</label>
            <input type="password" id="newPassword" name="newPassword" maxlength="15">
        </div>
        <div class="form-group">
            <label for="confirmPassword">Confirm Password:</label>
            <input type="password" id="confirmPassword" name="confirmPassword" maxlength="15">
        </div>
        <div class="form-group">
            <button type="submit" class="save-button">Save</button>
        </div>
    </form>
    <p><small>Password must be 1-15 characters long.</small></p>
</body>
</html>'''
    
    return build_tplink_response("200 OK", html, include_cookies=True)


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ ESTAS PÁGINAS ADICIONALES?
#    - Aumentan la credibilidad del honeypot
#    - Routers reales tienen estas funcionalidades
#    - Capturan más intentos de interacción
#
# 2. ¿LOS DATOS SON REALES?
#    - NO, todas las estadísticas son generadas aleatoriamente
#    - Los logs son falsos pero realistas
#    - El objetivo es PARECER real, no serlo
#
# 3. ¿QUÉ PASA SI ALGUIEN INTENTA CAMBIAR LA CONTRASEÑA?
#    - El formulario captura el intento
#    - No se cambia nada realmente
#    - Se loguea para análisis
#
# ═══════════════════════════════════════════════════════════════════════════
