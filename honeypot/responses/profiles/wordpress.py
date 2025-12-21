"""
═══════════════════════════════════════════════════════════════════════════
PERFIL WORDPRESS - CMS Vulnerable
═══════════════════════════════════════════════════════════════════════════
Simula una instalación de WordPress para atraer ataques específicos de WP.
Incluye endpoints comunes que los atacantes buscan en sitios WordPress.

MEJORAS IMPLEMENTADAS:
✅ Usa common profile corporativo para coherencia
✅ Página principal corporativa (no genérica)
✅ robots.txt, humans.txt, security.txt coherentes con WordPress
✅ Branding empresarial consistente
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from .common import get_corporate_common_endpoints
# ↑ Importar generador de endpoints comunes corporativos
# Esto proporciona: /, /robots.txt, /favicon.ico, /sitemap.xml, 
#                   /humans.txt, /.well-known/security.txt


# ═══════════════════════════════════════════════════════════════════════════
# CONFIGURACIÓN DEL BRANDING CORPORATIVO
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - WordPress suele ser usado por empresas/negocios
# - Definimos el branding que se usará en todos los endpoints comunes
# - Esto asegura coherencia entre la página principal y los endpoints de WP
# ═══════════════════════════════════════════════════════════════════════════

WORDPRESS_BRAND_NAME = "TechSolutions Inc."
WORDPRESS_DOMAIN = "techsolutions.local"
WORDPRESS_TAGLINE = "Innovation in Technology"
WORDPRESS_TECH_STACK = [
    "Apache/2.4.41",
    "PHP/7.4",
    "MySQL/8.0",
    "WordPress/6.4"
]


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS ESPECÍFICOS DE WORDPRESS
# ═══════════════════════════════════════════════════════════════════════════
# NOTA: Estos son endpoints ÚNICOS de WordPress
# Los endpoints comunes (/, /robots.txt, etc.) vienen del generador corporativo
# ═══════════════════════════════════════════════════════════════════════════

WORDPRESS_SPECIFIC_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /wp-admin (Panel de Administración de WordPress)                  │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Panel de administración de WordPress                            │
    # │ TRAMPA: Atrae ataques de fuerza bruta específicos de WP                 │
    # │ MEJORA FUTURA: Convertir a función dinámica con formulario real         │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/wp-admin': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>WordPress Admin</h1><!-- Fake WP Login --></body></html>',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /wp-login.php (Login de WordPress)                                │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Página de login estándar de WordPress                           │
    # │ TRAMPA: Formulario falso para capturar credenciales                     │
    # │ MEJORA FUTURA: Formulario completo con CSS estilo WordPress             │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/wp-login.php': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>WordPress Login</h1><form name="loginform" action="wp-login.php" method="post"></form></body></html>',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /xmlrpc.php (XML-RPC de WordPress)                                │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Endpoint XML-RPC (usado para ataques DDoS en WP)                │
    # │ TRAMPA: Responde "Method Not Allowed" para parecer real                 │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/xmlrpc.php': 'HTTP/1.1 405 Method Not Allowed\r\nContent-Type: text/plain\r\n\r\nXML-RPC server accepts POST requests only.',
}


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS COMPLETOS DE WORDPRESS
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - Fusionamos endpoints comunes corporativos + endpoints específicos de WP
# - Operador ** "desempaqueta" el diccionario
# - Resultado: Un diccionario completo con TODAS las rutas
#
# EJEMPLO DE FUSIÓN:
#   common = {'/': home, '/robots.txt': robots}
#   specific = {'/wp-admin': wp_admin}
#   result = {**common, **specific}
#   → {'/': home, '/robots.txt': robots, '/wp-admin': wp_admin}
# ═══════════════════════════════════════════════════════════════════════════

WORDPRESS_ENDPOINTS = {
    # PASO 1: Desempaquetar endpoints comunes corporativos
    # NOTA: Estos endpoints usan el branding definido arriba
    **get_corporate_common_endpoints(
        brand_name=WORDPRESS_BRAND_NAME,
        domain=WORDPRESS_DOMAIN,
        tagline=WORDPRESS_TAGLINE,
        tech_stack=WORDPRESS_TECH_STACK
    ),
    
    # PASO 2: Desempaquetar endpoints específicos de WordPress
    # NOTA: Si hay conflicto de rutas, estos SOBRESCRIBEN los comunes
    **WORDPRESS_SPECIFIC_ENDPOINTS,
}


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿QUÉ CAMBIÓ EN ESTE ARCHIVO?
#    ANTES:
#    - Solo endpoints específicos de WordPress
#    - Sin página principal, robots.txt, etc.
#    - Dependía de common.py genérico (no coherente)
#
#    AHORA:
#    - Usa generador corporativo para endpoints comunes
#    - Página principal corporativa coherente con WordPress
#    - Branding consistente en todos los endpoints
#    - Tech stack menciona WordPress en humans.txt
#
# 2. ¿CÓMO FUNCIONA LA FUSIÓN DE DICCIONARIOS?
#    - Operador **: Desempaqueta un diccionario
#    - {**dict1, **dict2}: Fusiona dict1 y dict2
#    - Si hay claves duplicadas, dict2 sobrescribe dict1
#    - Ejemplo:
#      {**{'a': 1, 'b': 2}, **{'b': 3, 'c': 4}}
#      → {'a': 1, 'b': 3, 'c': 4}
#
# 3. ¿POR QUÉ DEFINIR CONSTANTES DE BRANDING?
#    - Facilita cambiar el branding en un solo lugar
#    - Documentación clara de la configuración
#    - Fácil de personalizar para diferentes escenarios
#
# 4. ¿QUÉ ENDPOINTS TIENE AHORA WORDPRESS_ENDPOINTS?
#    COMUNES (de corporate):
#    - /                          → Landing page corporativa
#    - /robots.txt                → SEO-optimizado
#    - /favicon.ico               → Favicon válido
#    - /sitemap.xml               → Sitemap con páginas corporativas
#    - /humans.txt                → Info del equipo + WordPress en tech stack
#    - /.well-known/security.txt  → Política de seguridad profesional
#
#    ESPECÍFICOS (de WordPress):
#    - /wp-admin                  → Panel de administración
#    - /wp-login.php              → Página de login
#    - /xmlrpc.php                → XML-RPC endpoint
#
# 5. ¿CÓMO SE IMPORTA ESTE PERFIL?
#    - En profiles/__init__.py:
#      from .wordpress import WORDPRESS_ENDPOINTS
#    - En endpoint_manager.py:
#      from .profiles import WORDPRESS_ENDPOINTS
#
# 6. MEJORAS FUTURAS:
#    - Convertir /wp-admin y /wp-login.php a funciones dinámicas
#    - Añadir más endpoints de WordPress (/wp-content/, /wp-includes/)
#    - Simular plugins vulnerables conocidos
#
# ═══════════════════════════════════════════════════════════════════════════
