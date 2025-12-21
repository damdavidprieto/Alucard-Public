"""
═══════════════════════════════════════════════════════════════════════════
PERFIL API - Backend Empresarial
═══════════════════════════════════════════════════════════════════════════
Simula una API REST empresarial con endpoints comunes.
Atrae ataques a APIs, inyecciones, y escaneos de Swagger/Actuator.

MEJORAS IMPLEMENTADAS:
✅ Usa common profile Apache default (APIs backend no tienen frontend elaborado)
✅ Página principal: Apache2 Ubuntu Default Page
✅ robots.txt, humans.txt coherentes con stack Java/Spring Boot
✅ Tech stack menciona Java, Spring Boot en humans.txt
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from .common import get_apache_default_common_endpoints
# ↑ Importar generador de endpoints comunes Apache default
# APIs backend suelen tener página default simple, no frontend corporativo


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS ESPECÍFICOS DE API
# ═══════════════════════════════════════════════════════════════════════════
# NOTA: Estos son endpoints ÚNICOS de APIs REST
# Los endpoints comunes (/, /robots.txt, etc.) vienen del generador Apache default
# ═══════════════════════════════════════════════════════════════════════════

API_SPECIFIC_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /api/v1/users (Endpoint de Usuarios)                              │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Endpoint REST para listar usuarios                              │
    # │ TRAMPA: Devuelve datos falsos para parecer una API real                 │
    # │ MEJORA FUTURA: Convertir a función dinámica con datos variables         │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/api/v1/users': 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"users": [{"id": 1, "name": "admin"}]}',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /api/auth (Autenticación API)                                     │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Endpoint de autenticación con API key                           │
    # │ TRAMPA: Siempre devuelve "Invalid API key"                              │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/api/auth': 'HTTP/1.1 401 Unauthorized\r\nContent-Type: application/json\r\n\r\n{"error": "Invalid API key"}',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /actuator/health (Spring Boot Actuator)                           │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Endpoint de health check de Spring Boot                         │
    # │ TRAMPA: Simula una aplicación Java Spring Boot                          │
    # │ NOTA: Actuator expuesto es una vulnerabilidad común                     │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/actuator/health': 'HTTP/1.1 200 OK\r\nContent-Type: application/json\r\n\r\n{"status":"UP"}',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /swagger-ui.html (Documentación Swagger)                          │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Interfaz de documentación de API Swagger                        │
    # │ TRAMPA: Sugiere que hay documentación de API expuesta                   │
    # │ MEJORA FUTURA: Página Swagger completa con endpoints falsos             │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/swagger-ui.html': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>Swagger UI</h1><p>API Documentation</p></body></html>',
}


# ═══════════════════════════════════════════════════════════════════════════
# ENDPOINTS COMPLETOS DE API
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - Fusionamos endpoints comunes Apache default + endpoints específicos de API
# - Apache default es apropiado porque APIs backend no tienen frontend elaborado
# - La página principal será "Apache2 Ubuntu Default Page: It works"
# - Coherente con un servidor backend sin configurar frontend
# ═══════════════════════════════════════════════════════════════════════════

API_ENDPOINTS = {
    # PASO 1: Desempaquetar endpoints comunes Apache default
    # NOTA: No pasamos parámetros, usa valores por defecto
    **get_apache_default_common_endpoints(),
    
    # PASO 2: Desempaquetar endpoints específicos de API
    **API_SPECIFIC_ENDPOINTS,
}


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ APACHE DEFAULT Y NO CORPORATE?
#    - APIs backend NO suelen tener frontend corporativo elaborado
#    - Es común ver Apache2 default page en APIs de desarrollo/staging
#    - Más realista que una landing page corporativa
#    - El atacante piensa: "API sin frontend configurado = vulnerable"
#
# 2. ¿QUÉ ENDPOINTS TIENE AHORA API_ENDPOINTS?
#    COMUNES (de apache_default):
#    - /                          → Apache2 Ubuntu Default Page
#    - /robots.txt                → Directivas genéricas
#    - /favicon.ico               → Favicon válido
#    - /sitemap.xml               → Sitemap básico
#    - /humans.txt                → System Administrator
#    - /.well-known/security.txt  → Política de seguridad genérica
#
#    ESPECÍFICOS (de API):
#    - /api/v1/users              → Endpoint REST de usuarios
#    - /api/auth                  → Autenticación API
#    - /actuator/health           → Spring Boot health check
#    - /swagger-ui.html           → Documentación Swagger
#
# 3. ¿CÓMO PERSONALIZAR EL TECH STACK?
#    - Actualmente usa valores por defecto de apache_default
#    - Para personalizar, modificar humans.txt en apache_default.py
#    - O crear una variante específica para APIs Java/Spring Boot
#
# 4. MEJORAS FUTURAS:
#    - Convertir endpoints API a funciones dinámicas
#    - Añadir más endpoints de Actuator (/actuator/env, /actuator/metrics)
#    - Simular respuestas Swagger completas con OpenAPI spec
#    - Añadir endpoints de GraphQL (/graphql, /graphiql)
#
# 5. ¿POR QUÉ NO MENCIONAR JAVA/SPRING BOOT EN COMMON?
#    - apache_default es genérico (usado también por generic.py)
#    - Para mencionar Java/Spring Boot, necesitaríamos:
#      * Crear apache_default_java.py
#      * O pasar tech_stack como parámetro a apache_default
#    - Por ahora, la coherencia básica es suficiente
#
# ═══════════════════════════════════════════════════════════════════════════
