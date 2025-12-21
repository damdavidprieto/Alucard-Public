"""
═══════════════════════════════════════════════════════════════════════════
BASE UTILITIES - Funciones compartidas para todos los perfiles comunes
═══════════════════════════════════════════════════════════════════════════
Este módulo contiene utilidades base que son usadas por todos los generadores
de perfiles comunes (apache_default, corporate, device).

CONTENIDO:
✅ Generador de favicon (base64)
✅ Funciones helper para construir respuestas HTTP
✅ Utilidades de contenido dinámico compartido
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════
from ...utils.http_builder import HTTPResponseBuilder
from ...utils.dynamic_content import DynamicContentGenerator


# ═══════════════════════════════════════════════════════════════════════════
# FAVICON GENERATOR
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - Los navegadores SIEMPRE piden /favicon.ico
# - Un servidor real tiene un favicon válido
# - Devolver Content-Length: 0 es muy sospechoso
# - Solución: Generar un favicon simple pero válido en base64
# ═══════════════════════════════════════════════════════════════════════════

def get_favicon_base64():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR FAVICON SIMPLE EN BASE64                                        │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Retornar un favicon 16x16 píxeles codificado en base64             │
    │   2. Es un ícono genérico simple (cuadrado gris)                        │
    │   3. Suficiente para parecer legítimo                                   │
    │                                                                          │
    │ NOTA: Este es un favicon ICO real de 16x16 píxeles                      │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # FAVICON ICO: 16x16 píxeles, formato ICO estándar
    # Este es un cuadrado gris simple pero válido
    # Generado con herramientas estándar de conversión de imágenes
    favicon_data = (
        "AAABAAEAEBAQAAEABAAoAQAAFgAAACgAAAAQAAAAIAAAAAEABAAAAAAAgAAAAAAA"
        "AAAAAAAAEAAAAAAAAAAAAAAAgAAAgAAAAICAAIAAAACAAIAAgIAAAMDAwACAgIAA"
        "AP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8A"
        "AP//AAD//wAA//8AAP//AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
        "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAP//"
        "AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//AAD//wAA//8AAP//"
        "AAD//wAA//8AAP//AAA="
    )
    return favicon_data


def get_favicon_response():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUIR RESPUESTA HTTP COMPLETA PARA FAVICON                          │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener datos del favicon en base64                                │
    │   2. Decodificar base64 a bytes                                         │
    │   3. Construir respuesta HTTP con Content-Type: image/x-icon            │
    │   4. Incluir cache headers (24 horas)                                   │
    │                                                                          │
    │ RESULTADO: Respuesta HTTP válida con favicon real                       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    import base64
    
    # PASO 1: Obtener favicon en base64
    favicon_b64 = get_favicon_base64()
    
    # PASO 2: Decodificar a bytes
    # EXPLICACIÓN PYTHON:
    # - base64.b64decode() convierte string base64 a bytes
    # - .decode('latin1') convierte bytes a string (necesario para HTTP)
    favicon_bytes = base64.b64decode(favicon_b64).decode('latin1')
    
    # PASO 3: Construir respuesta HTTP
    # NOTA: cache_age=86400 = 24 horas (navegador cachea el favicon)
    return HTTPResponseBuilder.build_response(
        "200 OK",
        "image/x-icon",
        favicon_bytes,
        cache_age=86400  # Cache por 24 horas
    )


# ═══════════════════════════════════════════════════════════════════════════
# ROBOTS.TXT GENERATOR
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - robots.txt es estándar en todos los servidores web
# - Indica a los crawlers (Google, Bing) qué pueden indexar
# - Diferentes tipos de servidores tienen diferentes robots.txt
# ═══════════════════════════════════════════════════════════════════════════

def build_robots_txt(disallow_paths=None, allow_paths=None, crawl_delay=10, 
                     include_sitemap=True):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUIR ROBOTS.TXT CONFIGURABLE                                       │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - disallow_paths: Lista de rutas prohibidas (ej: ['/admin/', '/api/'])│
    │   - allow_paths: Lista de rutas permitidas (ej: ['/public/'])           │
    │   - crawl_delay: Segundos entre peticiones del crawler                  │
    │   - include_sitemap: Si incluir referencia a sitemap.xml                │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Empezar con "User-agent: *" (aplica a todos los crawlers)          │
    │   2. Añadir Crawl-delay                                                 │
    │   3. Añadir rutas Disallow (prohibidas)                                 │
    │   4. Añadir rutas Allow (permitidas)                                    │
    │   5. Opcionalmente añadir referencia a Sitemap                          │
    │                                                                          │
    │ TRAMPA: Las rutas "prohibidas" atraen a atacantes curiosos              │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # VALORES POR DEFECTO
    # EXPLICACIÓN PYTHON:
    # - "if disallow_paths is None:" = Si no se pasó el parámetro
    # - "disallow_paths = []" = Usar lista vacía por defecto
    if disallow_paths is None:
        disallow_paths = []
    if allow_paths is None:
        allow_paths = []
    
    # CONSTRUCCIÓN DEL CONTENIDO
    # PASO 1: Header básico
    content = f"User-agent: *\nCrawl-delay: {crawl_delay}\n"
    
    # PASO 2: Añadir rutas prohibidas
    # EXPLICACIÓN PYTHON:
    # - "for path in disallow_paths:" = Iterar sobre cada ruta
    # - "content += ..." = Añadir al string existente
    for path in disallow_paths:
        content += f"Disallow: {path}\n"
    
    # PASO 3: Añadir rutas permitidas
    for path in allow_paths:
        content += f"Allow: {path}\n"
    
    # PASO 4: Añadir sitemap si se solicita
    if include_sitemap:
        content += "\n# Sitemap\nSitemap: /sitemap.xml"
    
    # PASO 5: Construir respuesta HTTP
    return HTTPResponseBuilder.build_text(content)


# ═══════════════════════════════════════════════════════════════════════════
# SECURITY.TXT GENERATOR (RFC 9116)
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - security.txt es un estándar RFC 9116
# - Indica cómo reportar vulnerabilidades de seguridad
# - Empresas serias lo tienen en /.well-known/security.txt
# - Hace parecer el servidor más legítimo
# ═══════════════════════════════════════════════════════════════════════════

def build_security_txt(contact_email, domain="example.com", 
                       preferred_languages=None):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUIR SECURITY.TXT CONFIGURABLE (RFC 9116)                          │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - contact_email: Email de contacto para reportar vulnerabilidades     │
    │   - domain: Dominio del servidor                                        │
    │   - preferred_languages: Idiomas preferidos (ej: ['en', 'es'])          │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener fecha de expiración (6 meses en el futuro)                 │
    │   2. Construir contenido según RFC 9116                                 │
    │   3. Incluir Contact, Expires, Preferred-Languages, Canonical           │
    │                                                                          │
    │ EFECTO: Hace parecer el servidor profesional y legítimo                 │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # VALORES POR DEFECTO
    if preferred_languages is None:
        preferred_languages = ["en", "es"]
    
    # PASO 1: Obtener fecha de expiración dinámica
    # NOTA: DynamicContentGenerator.get_security_txt_expiry() genera
    #       una fecha 180 días en el futuro en formato ISO 8601
    expiry = DynamicContentGenerator.get_security_txt_expiry()
    
    # PASO 2: Construir contenido según RFC 9116
    # FORMATO ESTÁNDAR:
    # - Contact: Cómo contactar al equipo de seguridad
    # - Expires: Fecha de expiración del archivo
    # - Preferred-Languages: Idiomas preferidos para comunicación
    # - Canonical: URL canónica del archivo
    # - Acknowledgments: Página de reconocimientos (opcional)
    content = f"""Contact: mailto:{contact_email}
Expires: {expiry}
Preferred-Languages: {', '.join(preferred_languages)}
Canonical: https://{domain}/.well-known/security.txt
Acknowledgments: https://{domain}/security/hall-of-fame"""
    
    # PASO 3: Construir respuesta HTTP
    return HTTPResponseBuilder.build_text(content)


# ═══════════════════════════════════════════════════════════════════════════
# SITEMAP.XML GENERATOR
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - sitemap.xml lista todas las páginas del sitio
# - Usado por Google/Bing para indexar el sitio
# - Podemos incluir páginas FALSAS como trampa
# ═══════════════════════════════════════════════════════════════════════════

def build_sitemap_xml(urls_with_priority=None):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUIR SITEMAP.XML CONFIGURABLE                                      │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - urls_with_priority: Lista de tuplas (url, priority)                 │
    │     Ejemplo: [('/', 1.0), ('/about', 0.8), ('/contact', 0.5)]           │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Empezar con header XML estándar                                    │
    │   2. Para cada URL, crear entrada <url> con <loc> y <priority>          │
    │   3. Cerrar con </urlset>                                               │
    │                                                                          │
    │ TRAMPA: Incluir URLs que NO existen para detectar crawlers              │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # VALORES POR DEFECTO
    if urls_with_priority is None:
        # Por defecto, solo la página principal
        urls_with_priority = [('/', 1.0)]
    
    # PASO 1: Header XML estándar
    xml_content = '<?xml version="1.0" encoding="UTF-8"?>\n'
    xml_content += '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
    
    # PASO 2: Añadir cada URL
    # EXPLICACIÓN PYTHON:
    # - "for url, priority in urls_with_priority:" = Desempaquetar tupla
    # - url = primer elemento, priority = segundo elemento
    for url, priority in urls_with_priority:
        xml_content += f'''  <url>
    <loc>{url}</loc>
    <priority>{priority}</priority>
  </url>
'''
    
    # PASO 3: Cerrar XML
    xml_content += '</urlset>'
    
    # PASO 4: Construir respuesta HTTP
    return HTTPResponseBuilder.build_response(
        "200 OK",
        "application/xml; charset=UTF-8",
        xml_content
    )


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ FUNCIONES CONFIGURABLES?
#    - Cada tipo de servidor tiene diferentes robots.txt, security.txt, etc.
#    - En lugar de duplicar código, usamos funciones con parámetros
#    - Ejemplo: Apache default vs Corporate vs IoT device
#
# 2. ¿CÓMO SE USAN ESTAS FUNCIONES?
#    - Los generadores de perfiles (apache_default.py, corporate.py, etc.)
#      llaman a estas funciones con parámetros específicos
#    - Ejemplo: build_robots_txt(disallow_paths=['/admin/', '/api/'])
#
# 3. ¿POR QUÉ BASE64 PARA FAVICON?
#    - Los archivos binarios (imágenes) no se pueden poner directamente en código
#    - Base64 convierte bytes a texto ASCII
#    - Podemos incluir el favicon directamente en el código fuente
#
# 4. ¿QUÉ ES RFC 9116?
#    - RFC = Request For Comments (estándar de internet)
#    - RFC 9116 define el formato de security.txt
#    - Seguir el estándar hace parecer el servidor más legítimo
#
# ═══════════════════════════════════════════════════════════════════════════
