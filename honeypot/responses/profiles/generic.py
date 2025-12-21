"""
═══════════════════════════════════════════════════════════════════════════
PERFIL GENERIC - Servidor Básico
═══════════════════════════════════════════════════════════════════════════
Simula un servidor web genérico con páginas de administración básicas.
Ideal para atraer ataques de fuerza bruta y escaneos generales.

MEJORAS IMPLEMENTADAS:
✅ Usa common profile Apache default (servidor genérico sin configurar)
✅ Página principal: Apache2 Ubuntu Default Page
✅ robots.txt, humans.txt, security.txt coherentes
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from .common import get_apache_default_common_endpoints
# ↑ Importar generador de endpoints comunes Apache default
# Perfil genérico = servidor básico sin configurar


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS ESPECÍFICOS DE GENERIC
# ═══════════════════════════════════════════════════════════════════════════
# NOTA: Estos son endpoints ÚNICOS de servidores genéricos
# Los endpoints comunes (/, /robots.txt, etc.) vienen del generador Apache default
# ═══════════════════════════════════════════════════════════════════════════

GENERIC_SPECIFIC_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /admin (Panel de Administración)                                  │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Página de login de administrador                                │
    # │ TRAMPA: Formulario falso para capturar credenciales intentadas          │
    # │ MEJORA FUTURA: Convertir a función dinámica con formulario completo     │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/admin': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Admin Login</h1><form><input name="user"><input type="password" name="pass"></form></body></html>',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /login (Login General)                                            │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Página de login genérica                                        │
    # │ TRAMPA: Captura intentos de autenticación                               │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/login': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Login</h1><form action="/auth" method="POST"><input name="username"><input type="password" name="password"></form></body></html>',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /auth (Endpoint de Autenticación)                                 │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Procesa intentos de login                                       │
    # │ TRAMPA: Siempre falla (para registrar credenciales intentadas)          │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/auth': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Login Failed</h1><p>Invalid credentials. Please try again.</p><a href="/login">Back</a></body></html>',
}


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS COMPLETOS DE GENERIC
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - Fusionamos endpoints comunes Apache default + endpoints específicos genéricos
# - Apache default es perfecto para un servidor genérico sin configurar
# - La página principal será "Apache2 Ubuntu Default Page: It works"
# ═══════════════════════════════════════════════════════════════════════════

GENERIC_ENDPOINTS = {
    # PASO 1: Desempaquetar endpoints comunes Apache default
    **get_apache_default_common_endpoints(),
    
    # PASO 2: Desempaquetar endpoints específicos genéricos
    **GENERIC_SPECIFIC_ENDPOINTS,
}


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿QUÉ CAMBIÓ EN ESTE ARCHIVO?
#    ANTES:
#    - Solo endpoints específicos (/admin, /login, /auth)
#    - Dependía de common.py genérico
#
#    AHORA:
#    - Usa generador Apache default para endpoints comunes
#    - Página principal: Apache2 Ubuntu Default Page
#    - Coherencia total con un servidor genérico
#
# 2. ¿QUÉ ENDPOINTS TIENE AHORA GENERIC_ENDPOINTS?
#    COMUNES (de apache_default):
#    - /                          → Apache2 Ubuntu Default Page
#    - /robots.txt                → Directivas genéricas
#    - /favicon.ico               → Favicon válido
#    - /sitemap.xml               → Sitemap básico
#    - /humans.txt                → System Administrator
#    - /.well-known/security.txt  → Política de seguridad genérica
#
#    ESPECÍFICOS (de generic):
#    - /admin                     → Panel de administración
#    - /login                     → Página de login
#    - /auth                      → Endpoint de autenticación
#
# 3. ¿CUÁNDO SE USA ESTE PERFIL?
#    - Cuando no se especifica un perfil concreto
#    - Para simular un servidor básico sin configurar
#    - Atrae ataques genéricos de fuerza bruta
#
# 4. MEJORAS FUTURAS:
#    - Convertir /admin, /login, /auth a funciones dinámicas
#    - Añadir más endpoints genéricos (/phpmyadmin, /backup/)
#    - Formularios HTML completos con CSS
#
# ═══════════════════════════════════════════════════════════════════════════
