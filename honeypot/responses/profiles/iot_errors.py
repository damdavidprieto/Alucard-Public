"""
═══════════════════════════════════════════════════════════════════════════
IOT ERRORS - Páginas de error con estilo TP-Link
═══════════════════════════════════════════════════════════════════════════
Genera páginas de error (404, 403, 500) con el estilo visual de TP-Link.

CARACTERÍSTICAS:
✅ Diseño coherente con interfaz TP-Link
✅ Colores y tipografía oficial
✅ Mensajes de error apropiados
✅ Enlaces de navegación útiles
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from .iot_helpers import build_tplink_response


# ═══════════════════════════════════════════════════════════════════════════
# PLANTILLA BASE DE ERROR
# ═══════════════════════════════════════════════════════════════════════════

def _build_error_page(error_code: str, error_title: str, error_message: str, 
                      show_home_link: bool = True) -> str:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUIR PÁGINA DE ERROR CON ESTILO TP-LINK                            │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - error_code: Código de error (ej: "404", "403", "500")              │
    │   - error_title: Título del error (ej: "Page Not Found")               │
    │   - error_message: Mensaje descriptivo                                  │
    │   - show_home_link: Si mostrar enlace a home                           │
    │                                                                          │
    │ RETORNA: HTML completo con estilo TP-Link                               │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # ENLACE HOME: Solo si se solicita
    home_link = '''
        <p style="margin-top: 30px;">
            <a href="/userRpm/Index.htm" style="color: #00A0E9; text-decoration: none;">
                ← Return to Router Home
            </a>
        </p>
    ''' if show_home_link else ''
    
    # HTML: Página de error con estilo TP-Link
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8">
    <title>{error_code} {error_title}</title>
    <style type="text/css">
        body {{
            margin: 0;
            padding: 0;
            font-family: Arial, sans-serif;
            background: linear-gradient(to bottom, #e8f4f8 0%, #d4e9f2 100%);
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }}
        
        .error-container {{
            background: white;
            border: 1px solid #c0c0c0;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            max-width: 600px;
            margin: 20px;
        }}
        
        .error-header {{
            background: #00A0E9;
            color: white;
            padding: 20px;
            text-align: center;
        }}
        
        .error-code {{
            font-size: 72px;
            font-weight: bold;
            margin: 0;
            line-height: 1;
        }}
        
        .error-title {{
            font-size: 24px;
            margin: 10px 0 0 0;
        }}
        
        .error-body {{
            padding: 40px;
            text-align: center;
        }}
        
        .error-message {{
            color: #666;
            font-size: 16px;
            line-height: 1.6;
            margin: 0 0 20px 0;
        }}
        
        .error-details {{
            background: #f8f8f8;
            border: 1px solid #e0e0e0;
            padding: 15px;
            margin: 20px 0;
            font-size: 14px;
            color: #888;
            text-align: left;
        }}
        
        a {{
            color: #00A0E9;
            text-decoration: none;
            font-weight: bold;
        }}
        
        a:hover {{
            text-decoration: underline;
        }}
        
        .footer {{
            background: #f0f0f0;
            padding: 15px;
            text-align: center;
            font-size: 11px;
            color: #999;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="error-container">
        <div class="error-header">
            <div class="error-code">{error_code}</div>
            <div class="error-title">{error_title}</div>
        </div>
        <div class="error-body">
            <p class="error-message">{error_message}</p>
            {home_link}
        </div>
        <div class="footer">
            TP-LINK TL-WR841N Wireless N Router
        </div>
    </div>
</body>
</html>'''
    
    return html


# ═══════════════════════════════════════════════════════════════════════════
# ERROR 404 - NOT FOUND
# ═══════════════════════════════════════════════════════════════════════════

def get_404_error():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE ERROR 404 NOT FOUND                                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ USO: Cuando se solicita una ruta que no existe                          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    html = _build_error_page(
        error_code="404",
        error_title="Page Not Found",
        error_message="The requested page does not exist on this router. Please check the URL and try again."
    )
    
    return build_tplink_response("404 Not Found", html)


# ═══════════════════════════════════════════════════════════════════════════
# ERROR 403 - FORBIDDEN
# ═══════════════════════════════════════════════════════════════════════════

def get_403_error():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE ERROR 403 FORBIDDEN                                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ USO: Cuando se intenta acceder a recurso sin permisos                   │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    html = _build_error_page(
        error_code="403",
        error_title="Access Forbidden",
        error_message="You don't have permission to access this resource. Please log in with valid administrator credentials."
    )
    
    return build_tplink_response("403 Forbidden", html)


# ═══════════════════════════════════════════════════════════════════════════
# ERROR 500 - INTERNAL SERVER ERROR
# ═══════════════════════════════════════════════════════════════════════════

def get_500_error():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA DE ERROR 500 INTERNAL SERVER ERROR                       │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ USO: Cuando hay un error interno del router                             │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    html = _build_error_page(
        error_code="500",
        error_title="Internal Server Error",
        error_message="The router encountered an internal error and was unable to complete your request. Please try rebooting the router.",
        show_home_link=False  # No mostrar link si el router tiene problemas
    )
    
    return build_tplink_response("500 Internal Server Error", html)


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ PÁGINAS DE ERROR PERSONALIZADAS?
#    - Routers reales tienen páginas de error con su estilo
#    - Aumenta credibilidad
#    - Mantiene coherencia visual
#    - Mejor experiencia para el atacante
#
# 2. ¿CUÁNDO SE USAN ESTAS PÁGINAS?
#    - 404: Ruta no encontrada
#    - 403: Acceso denegado (sin permisos)
#    - 500: Error interno del servidor
#
# 3. ¿CÓMO SE INTEGRAN?
#    En endpoint_manager.py:
#    from .profiles.iot_errors import get_404_error
#    
#    if path not in endpoints:
#        return get_404_error()
#
# ═══════════════════════════════════════════════════════════════════════════
