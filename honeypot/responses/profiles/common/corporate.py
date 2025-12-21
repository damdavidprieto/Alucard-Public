"""
═══════════════════════════════════════════════════════════════════════════
CORPORATE COMMON PROFILE - Sitio web empresarial/corporativo
═══════════════════════════════════════════════════════════════════════════
Este generador crea endpoints comunes temáticos para simular un sitio web
de empresa/negocio profesional.

USO:
- WordPress corporativo
- APIs empresariales con frontend
- Aplicaciones de negocio

APARIENCIA:
- Página principal: Landing page corporativa con branding
- robots.txt: SEO-optimizado
- humans.txt: Equipo de desarrollo profesional
- Favicon: Logo corporativo

EFECTO PSICOLÓGICO:
El atacante piensa: "Empresa real = datos valiosos = objetivo interesante"
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
    build_security_txt,
    build_sitemap_xml
)


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE PÁGINA PRINCIPAL - CORPORATE
# ═══════════════════════════════════════════════════════════════════════════

def get_corporate_home(brand_name, tagline, tech_stack):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA PRINCIPAL CORPORATIVA                                    │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - brand_name: Nombre de la empresa (ej: "TechSolutions Inc.")         │
    │   - tagline: Eslogan (ej: "Innovation in Technology")                   │
    │   - tech_stack: Lista de tecnologías (ej: ["Apache", "PHP", "MySQL"])   │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener uptime y session ID (dinámicos)                            │
    │   2. Construir HTML corporativo moderno con CSS                         │
    │   3. Incluir branding, navegación, footer                               │
    │   4. Mencionar tech stack en footer                                     │
    │                                                                          │
    │ REALISMO: Parece un sitio corporativo real con diseño profesional       │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # DATOS DINÁMICOS
    uptime = DynamicContentGenerator.get_uptime_days()
    session = DynamicContentGenerator.generate_session_id()
    
    # TECH STACK: Convertir lista a string
    # EXPLICACIÓN PYTHON:
    # - ', '.join(tech_stack) = Une elementos con ", "
    # - Ejemplo: ["Apache", "PHP"] → "Apache, PHP"
    tech_stack_str = ', '.join(tech_stack) if tech_stack else "Apache"
    
    # HTML: Página corporativa moderna con CSS
    body = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <meta name="description" content="{brand_name} - {tagline}">
    <meta name="keywords" content="business, technology, solutions, consulting">
    <title>{brand_name} - {tagline}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            line-height: 1.6;
            color: #333;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
        }}
        
        .container {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }}
        
        header {{
            background: rgba(255, 255, 255, 0.95);
            padding: 20px 0;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }}
        
        .header-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}
        
        .logo {{
            font-size: 28px;
            font-weight: bold;
            color: #667eea;
            text-decoration: none;
        }}
        
        nav {{
            display: flex;
            gap: 30px;
        }}
        
        nav a {{
            color: #333;
            text-decoration: none;
            font-weight: 500;
            transition: color 0.3s;
        }}
        
        nav a:hover {{
            color: #667eea;
        }}
        
        .hero {{
            background: white;
            border-radius: 10px;
            padding: 60px 40px;
            text-align: center;
            box-shadow: 0 10px 40px rgba(0,0,0,0.1);
            margin-bottom: 40px;
        }}
        
        h1 {{
            font-size: 48px;
            color: #667eea;
            margin-bottom: 20px;
        }}
        
        .tagline {{
            font-size: 24px;
            color: #666;
            margin-bottom: 30px;
        }}
        
        .description {{
            font-size: 18px;
            color: #555;
            max-width: 800px;
            margin: 0 auto 40px;
        }}
        
        .cta-button {{
            display: inline-block;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 15px 40px;
            border-radius: 50px;
            text-decoration: none;
            font-weight: bold;
            font-size: 18px;
            transition: transform 0.3s, box-shadow 0.3s;
        }}
        
        .cta-button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 10px 20px rgba(102, 126, 234, 0.4);
        }}
        
        .features {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
            gap: 30px;
            margin-bottom: 40px;
        }}
        
        .feature-card {{
            background: white;
            padding: 30px;
            border-radius: 10px;
            box-shadow: 0 5px 20px rgba(0,0,0,0.1);
            transition: transform 0.3s;
        }}
        
        .feature-card:hover {{
            transform: translateY(-5px);
        }}
        
        .feature-card h3 {{
            color: #667eea;
            margin-bottom: 15px;
            font-size: 24px;
        }}
        
        .feature-card p {{
            color: #666;
            font-size: 16px;
        }}
        
        footer {{
            background: rgba(255, 255, 255, 0.95);
            padding: 30px 0;
            margin-top: 60px;
            box-shadow: 0 -2px 10px rgba(0,0,0,0.1);
        }}
        
        .footer-content {{
            max-width: 1200px;
            margin: 0 auto;
            padding: 0 20px;
            text-align: center;
        }}
        
        .footer-content p {{
            color: #666;
            margin-bottom: 10px;
        }}
        
        .footer-meta {{
            font-size: 12px;
            color: #999;
            margin-top: 15px;
        }}
    </style>
</head>
<body>
    <header>
        <div class="header-content">
            <a href="/" class="logo">{brand_name}</a>
            <nav>
                <a href="/about">About</a>
                <a href="/services">Services</a>
                <a href="/contact">Contact</a>
            </nav>
        </div>
    </header>
    
    <div class="container">
        <div class="hero">
            <h1>Welcome to {brand_name}</h1>
            <p class="tagline">{tagline}</p>
            <p class="description">
                We provide cutting-edge technology solutions to help businesses 
                thrive in the digital age. Our team of experts is dedicated to 
                delivering innovative and reliable services tailored to your needs.
            </p>
            <a href="/contact" class="cta-button">Get Started</a>
        </div>
        
        <div class="features">
            <div class="feature-card">
                <h3>🚀 Innovation</h3>
                <p>Leveraging the latest technologies to drive your business forward.</p>
            </div>
            <div class="feature-card">
                <h3>🔒 Security</h3>
                <p>Enterprise-grade security to protect your valuable data.</p>
            </div>
            <div class="feature-card">
                <h3>⚡ Performance</h3>
                <p>Optimized solutions for maximum speed and efficiency.</p>
            </div>
        </div>
    </div>
    
    <footer>
        <div class="footer-content">
            <p>&copy; 2024 {brand_name}. All rights reserved.</p>
            <p>Powered by {tech_stack_str}</p>
            <div class="footer-meta">
                <small>Server Uptime: {uptime} days | Session: {session}</small>
            </div>
        </div>
    </footer>
</body>
</html>'''
    
    return HTTPResponseBuilder.build_html(f"{brand_name} - {tagline}", body)


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE HUMANS.TXT - CORPORATE
# ═══════════════════════════════════════════════════════════════════════════

def get_corporate_humans(brand_name, domain, tech_stack):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR HUMANS.TXT PARA SITIO CORPORATIVO                               │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS:                                                              │
    │   - brand_name: Nombre de la empresa                                    │
    │   - domain: Dominio del sitio                                           │
    │   - tech_stack: Lista de tecnologías                                    │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener fecha de última actualización (dinámica)                   │
    │   2. Construir humans.txt profesional con equipo de desarrollo          │
    │   3. Mencionar tech stack completo                                      │
    │                                                                          │
    │ EFECTO: Parece una empresa con equipo de desarrollo real                │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    last_update = DynamicContentGenerator.get_last_update_date()
    tech_stack_str = ', '.join(tech_stack) if tech_stack else "Apache, PHP"
    
    content = f'''/* TEAM */
Company: {brand_name}
Developer: Web Development Team
Contact: dev [at] {domain}
Location: Cloud Infrastructure

/* SITE */
Last update: {last_update}
Standards: HTML5, CSS3, JavaScript ES6
Components: {tech_stack_str}
Framework: Modern Web Stack

/* THANKS */
To our amazing team and clients who make this possible.'''
    
    return HTTPResponseBuilder.build_text(content)


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL: OBTENER TODOS LOS ENDPOINTS COMUNES - CORPORATE
# ═══════════════════════════════════════════════════════════════════════════

def get_corporate_common_endpoints(brand_name="TechSolutions Inc.", 
                                   domain="techsolutions.local",
                                   tagline="Innovation in Technology",
                                   tech_stack=None):
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR DICCIONARIO COMPLETO DE ENDPOINTS COMUNES - CORPORATE           │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PARÁMETROS CONFIGURABLES:                                                │
    │   - brand_name: Nombre de la empresa (default: "TechSolutions Inc.")    │
    │   - domain: Dominio del sitio (default: "techsolutions.local")          │
    │   - tagline: Eslogan (default: "Innovation in Technology")              │
    │   - tech_stack: Lista de tecnologías (default: Apache, PHP, MySQL)      │
    │                                                                          │
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Establecer valores por defecto si no se proporcionan               │
    │   2. Crear diccionario con todas las rutas comunes                      │
    │   3. Configurar cada endpoint con los parámetros proporcionados         │
    │   4. Retornar diccionario completo                                      │
    │                                                                          │
    │ RETORNO: Diccionario {ruta: función_generadora}                         │
    │                                                                          │
    │ USO:                                                                     │
    │   from .common.corporate import get_corporate_common_endpoints          │
    │   ENDPOINTS = {                                                          │
    │       **get_corporate_common_endpoints(                                 │
    │           brand_name="MyCompany",                                       │
    │           domain="mycompany.com",                                       │
    │           tech_stack=["Apache", "PHP", "WordPress"]                     │
    │       ),                                                                 │
    │       '/wp-admin/': ...,  # Endpoints específicos del perfil            │
    │   }                                                                      │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # VALORES POR DEFECTO
    if tech_stack is None:
        tech_stack = ["Apache/2.4.41", "PHP/7.4", "MySQL/8.0"]
    
    return {
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: / (Página Principal)                                      │
        # │ FUNCIÓN: Lambda que llama get_corporate_home con parámetros     │
        # │ APARIENCIA: Landing page corporativa moderna                    │
        # └─────────────────────────────────────────────────────────────────┘
        '/': lambda: get_corporate_home(brand_name, tagline, tech_stack),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /robots.txt                                               │
        # │ CONFIGURACIÓN: SEO-optimizado para empresa                      │
        # │ TRAMPA: Disallow /admin/, /api/, /backup/                       │
        # └─────────────────────────────────────────────────────────────────┘
        '/robots.txt': lambda: build_robots_txt(
            disallow_paths=['/admin/', '/api/', '/backup/', '/wp-admin/', '/private/'],
            allow_paths=['/public/', '/assets/', '/images/'],
            crawl_delay=5,  # Crawl más rápido (empresa quiere SEO)
            include_sitemap=True
        ),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /favicon.ico                                              │
        # │ CONTENIDO: Favicon corporativo (mismo que apache_default)       │
        # └─────────────────────────────────────────────────────────────────┘
        '/favicon.ico': get_favicon_response,
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /sitemap.xml                                              │
        # │ CONFIGURACIÓN: Sitemap corporativo con páginas típicas          │
        # │ TRAMPA: Algunas páginas pueden no existir                       │
        # └─────────────────────────────────────────────────────────────────┘
        '/sitemap.xml': lambda: build_sitemap_xml(
            urls_with_priority=[
                ('/', 1.0),
                ('/about', 0.9),
                ('/services', 0.9),
                ('/contact', 0.8),
                ('/blog', 0.7),
                ('/products', 0.8)
            ]
        ),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /humans.txt                                               │
        # │ FUNCIÓN: Lambda que llama get_corporate_humans                  │
        # │ CONTENIDO: Info del equipo de desarrollo corporativo            │
        # └─────────────────────────────────────────────────────────────────┘
        '/humans.txt': lambda: get_corporate_humans(brand_name, domain, tech_stack),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /.well-known/security.txt                                 │
        # │ CONFIGURACIÓN: Política de seguridad profesional                │
        # │ EFECTO: Hace parecer empresa seria con proceso de seguridad     │
        # └─────────────────────────────────────────────────────────────────┘
        '/.well-known/security.txt': lambda: build_security_txt(
            contact_email=f"security@{domain}",
            domain=domain,
            preferred_languages=["en", "es"]
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ CORPORATE PROFILE?
#    - Muchos sitios WordPress son corporativos
#    - APIs empresariales suelen tener landing pages
#    - Parece objetivo de valor (datos de clientes, transacciones)
#    - Más atractivo para atacantes que un servidor genérico
#
# 2. ¿POR QUÉ PARÁMETROS CONFIGURABLES?
#    - Cada perfil puede personalizar el branding
#    - WordPress puede usar nombre de empresa diferente que API
#    - Permite coherencia total entre common y perfil específico
#
# 3. ¿CÓMO SE USA ESTE GENERADOR?
#    - En wordpress.py:
#      from .common.corporate import get_corporate_common_endpoints
#      WORDPRESS_ENDPOINTS = {
#          **get_corporate_common_endpoints(
#              brand_name="TechCorp Solutions",
#              domain="techcorp.local",
#              tech_stack=["Apache/2.4.41", "PHP/7.4", "MySQL/8.0", "WordPress/6.4"]
#          ),
#          '/wp-admin/': get_wp_admin,
#          '/wp-login.php': get_wp_login,
#      }
#
# 4. ¿QUÉ PERFILES USAN ESTE COMMON?
#    - wordpress.py: CMS corporativo
#    - Cualquier API con frontend corporativo
#    - Aplicaciones de negocio
#
# 5. ¿POR QUÉ USAR LAMBDAS?
#    - Necesitamos pasar parámetros a las funciones
#    - Lambda captura las variables del scope (brand_name, domain, etc.)
#    - Se ejecuta cuando se accede a la ruta, no al definir el diccionario
#
# ═══════════════════════════════════════════════════════════════════════════
