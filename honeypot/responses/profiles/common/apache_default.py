"""
═══════════════════════════════════════════════════════════════════════════
APACHE DEFAULT COMMON PROFILE - Servidor genérico sin configurar
═══════════════════════════════════════════════════════════════════════════
Este generador crea endpoints comunes temáticos para simular un servidor
Apache2 recién instalado con la página por defecto de Ubuntu.

USO:
- Servidores genéricos
- APIs backend sin frontend
- Instalaciones mínimas

APARIENCIA:
- Página principal: "Apache2 Ubuntu Default Page: It works"
- robots.txt: Directivas genéricas
- humans.txt: System Administrator
- Favicon: Genérico

EFECTO PSICOLÓGICO:
El atacante piensa: "Servidor sin configurar = vulnerable = objetivo fácil"
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
# GENERADOR DE PÁGINA PRINCIPAL - APACHE2 DEFAULT
# ═══════════════════════════════════════════════════════════════════════════

def get_apache_default_home():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR PÁGINA PRINCIPAL ESTILO APACHE2 UBUNTU DEFAULT                  │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener uptime del servidor (dinámico)                             │
    │   2. Construir HTML idéntico a Apache2 Ubuntu Default Page              │
    │   3. Incluir CSS inline para estilo oficial                             │
    │   4. Mencionar rutas de configuración reales de Apache                  │
    │                                                                          │
    │ REALISMO: Esta es la página REAL que ven miles de servidores            │
    │ TRAMPA: El atacante piensa que el servidor está sin configurar          │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # DATO DINÁMICO: Uptime del servidor
    uptime = DynamicContentGenerator.get_uptime_days()
    
    # HTML: Réplica de la página oficial de Apache2 Ubuntu
    # NOTA: Este es el HTML REAL que Apache2 muestra por defecto
    body = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="UTF-8">
    <title>Apache2 Ubuntu Default Page: It works</title>
    <style type="text/css" media="screen">
        * {{
            margin: 0px 0px 0px 0px;
            padding: 0px 0px 0px 0px;
        }}

        body, html {{
            padding: 3px 3px 3px 3px;
            background-color: #D8DBE2;
            font-family: Verdana, sans-serif;
            font-size: 11pt;
            text-align: center;
        }}

        div.main_page {{
            position: relative;
            display: table;
            width: 800px;
            margin-bottom: 3px;
            margin-left: auto;
            margin-right: auto;
            padding: 0px 0px 0px 0px;
            border-width: 2px;
            border-color: #212738;
            border-style: solid;
            background-color: #FFFFFF;
            text-align: center;
        }}

        div.page_header {{
            height: 99px;
            width: 100%;
            background-color: #F5F6F7;
        }}

        div.page_header span {{
            margin: 15px 0px 0px 50px;
            font-size: 180%;
            font-weight: bold;
        }}

        div.page_header img {{
            margin: 3px 0px 0px 40px;
            border: 0px 0px 0px;
        }}

        div.table_of_contents {{
            clear: left;
            min-width: 200px;
            margin: 3px 3px 3px 3px;
            background-color: #FFFFFF;
            text-align: left;
        }}

        div.table_of_contents_item {{
            clear: left;
            width: 100%;
            margin: 4px 0px 0px 0px;
            background-color: #FFFFFF;
            color: #000000;
            text-align: left;
        }}

        div.table_of_contents_item a {{
            margin: 6px 0px 0px 6px;
        }}

        div.content_section {{
            margin: 3px 3px 3px 3px;
            background-color: #FFFFFF;
            text-align: left;
        }}

        div.content_section_text {{
            padding: 4px 8px 4px 8px;
            color: #000000;
            font-size: 100%;
        }}

        div.content_section_text pre {{
            margin: 8px 0px 8px 0px;
            padding: 8px 8px 8px 8px;
            border-width: 1px;
            border-style: dotted;
            border-color: #000000;
            background-color: #F5F6F7;
            font-style: italic;
        }}

        div.content_section_text p {{
            margin-bottom: 6px;
        }}

        div.content_section_text ul, div.content_section_text li {{
            padding: 4px 8px 4px 16px;
        }}

        div.section_header {{
            padding: 3px 6px 3px 6px;
            background-color: #8E9CB2;
            color: #FFFFFF;
            font-weight: bold;
            font-size: 112%;
            text-align: center;
        }}

        div.section_header_red {{
            background-color: #CD214F;
        }}

        div.section_header_grey {{
            background-color: #9F9386;
        }}

        .floating_element {{
            position: relative;
            float: left;
        }}

        div.table_of_contents_item a,
        div.content_section_text a {{
            text-decoration: none;
            font-weight: bold;
        }}

        div.table_of_contents_item a:link,
        div.table_of_contents_item a:visited,
        div.table_of_contents_item a:active {{
            color: #000000;
        }}

        div.table_of_contents_item a:hover {{
            background-color: #000000;
            color: #FFFFFF;
        }}

        div.content_section_text a:link,
        div.content_section_text a:visited,
        div.content_section_text a:active {{
            background-color: #DCDFE6;
            color: #000000;
        }}

        div.content_section_text a:hover {{
            background-color: #000000;
            color: #DCDFE6;
        }}

        div.validator {{
        }}
    </style>
</head>
<body>
    <div class="main_page">
        <div class="page_header floating_element">
            <span class="floating_element">Apache2 Ubuntu Default Page</span>
        </div>
        <div class="content_section floating_element">
            <div class="section_header section_header_red">
                <div id="about"></div>
                It works!
            </div>
            <div class="content_section_text">
                <p>
                    This is the default welcome page used to test the correct 
                    operation of the Apache2 server after installation on Ubuntu systems.
                    If you can read this page, it means that the Apache HTTP server installed at
                    this site is working properly. You should <b>replace this file</b> (located at
                    <tt>/var/www/html/index.html</tt>) before continuing to operate your HTTP server.
                </p>

                <p>
                    If you are a normal user of this web site and don't know what this page is
                    about, this probably means that the site is currently unavailable due to
                    maintenance. If the problem persists, please contact the site's administrator.
                </p>

            </div>
            <div class="section_header">
                <div id="changes"></div>
                Configuration Overview
            </div>
            <div class="content_section_text">
                <p>
                    Ubuntu's Apache2 default configuration is different from the
                    upstream default configuration, and split into several files optimized for
                    interaction with Ubuntu tools. The configuration system is
                    <b>fully documented in
                    /usr/share/doc/apache2/README.Debian.gz</b>. Refer to this for the full
                    documentation. Documentation for the web server itself can be
                    found by accessing the <a href="/manual">manual</a> if the <tt>apache2-doc</tt>
                    package was installed on this server.
                </p>
                <p>
                    The configuration layout for an Apache2 web server installation on Ubuntu systems is as follows:
                </p>
                <pre>
/etc/apache2/
|-- apache2.conf
|       `--  ports.conf
|-- mods-enabled
|       |-- *.load
|       `-- *.conf
|-- conf-enabled
|       `-- *.conf
|-- sites-enabled
|       `-- *.conf
                </pre>
                <p>
                    <ul>
                        <li>
                            <tt>apache2.conf</tt> is the main configuration
                            file. It puts the pieces together by including all remaining configuration
                            files when starting up the web server.
                        </li>

                        <li>
                            <tt>ports.conf</tt> is always included from the
                            main configuration file. It is used to determine the listening ports for
                            incoming connections, and this file can be customized anytime.
                        </li>

                        <li>
                            Configuration files in the <tt>mods-enabled/</tt>,
                            <tt>conf-enabled/</tt> and <tt>sites-enabled/</tt> directories contain
                            particular configuration snippets which manage modules, global configuration
                            fragments, or virtual host configurations, respectively.
                        </li>
                    </ul>
                </p>
            </div>

            <div class="section_header">
                <div id="docroot"></div>
                Document Roots
            </div>

            <div class="content_section_text">
                <p>
                    By default, Ubuntu does not allow access through the web browser to
                    <em>any</em> file apart of those located in <tt>/var/www</tt>,
                    <a href="http://httpd.apache.org/docs/2.4/mod/mod_userdir.html" rel="nofollow">public_html</a>
                    directories (when enabled) and <tt>/usr/share</tt> (for web
                    applications). If your site is using a web document root
                    located elsewhere (such as in <tt>/srv</tt>) you may need to whitelist your
                    document root directory in <tt>/etc/apache2/apache2.conf</tt>.
                </p>
                <p>
                    The default Ubuntu document root is <tt>/var/www/html</tt>. You
                    can make your own virtual hosts under /var/www. This is different
                    to previous releases which provides better security out of the box.
                </p>
            </div>

            <div class="section_header">
                <div id="bugs"></div>
                Reporting Problems
            </div>
            <div class="content_section_text">
                <p>
                    Please use the <tt>ubuntu-bug</tt> tool to report bugs in the
                    Apache2 package with Ubuntu. However, check <a
                    href="https://bugs.launchpad.net/ubuntu/+source/apache2"
                    rel="nofollow">existing bug reports</a> before reporting a new bug.
                </p>
                <p>
                    Please report bugs specific to modules (such as PHP and others)
                    to respective packages, not to the web server itself.
                </p>
            </div>

        </div>
    </div>
    <div class="validator">
        <p>
            <small>Server uptime: {uptime} days</small>
        </p>
    </div>
</body>
</html>'''
    
    # CONSTRUCCIÓN: Respuesta HTTP con headers Apache
    return HTTPResponseBuilder.build_html("Apache2 Ubuntu Default Page", body)


# ═══════════════════════════════════════════════════════════════════════════
# GENERADOR DE HUMANS.TXT - APACHE DEFAULT
# ═══════════════════════════════════════════════════════════════════════════

def get_apache_default_humans():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR HUMANS.TXT PARA SERVIDOR GENÉRICO                               │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Obtener fecha de última actualización (dinámica)                   │
    │   2. Construir humans.txt genérico (System Administrator)               │
    │   3. Mencionar stack básico: Apache, Ubuntu                             │
    │                                                                          │
    │ EFECTO: Parece un servidor básico sin personalización                   │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    # DATO DINÁMICO: Fecha de última actualización
    last_update = DynamicContentGenerator.get_last_update_date()
    
    # CONTENIDO: Información genérica de administrador
    content = f'''/* TEAM */
Developer: System Administrator
Contact: admin [at] localhost
Location: Cloud

/* SITE */
Last update: {last_update}
Standards: HTML5, CSS3
Components: Apache/2.4.41
Software: Ubuntu 20.04 LTS'''
    
    return HTTPResponseBuilder.build_text(content)


# ═══════════════════════════════════════════════════════════════════════════
# FUNCIÓN PRINCIPAL: OBTENER TODOS LOS ENDPOINTS COMUNES
# ═══════════════════════════════════════════════════════════════════════════

def get_apache_default_common_endpoints():
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERAR DICCIONARIO COMPLETO DE ENDPOINTS COMUNES - APACHE DEFAULT      │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ PSEUDOCÓDIGO:                                                            │
    │   1. Crear diccionario con todas las rutas comunes                      │
    │   2. Asignar funciones generadoras a cada ruta                          │
    │   3. Usar funciones de base.py para robots.txt, security.txt, etc.      │
    │   4. Retornar diccionario completo                                      │
    │                                                                          │
    │ RETORNO: Diccionario {ruta: función_generadora}                         │
    │                                                                          │
    │ USO:                                                                     │
    │   from .common.apache_default import get_apache_default_common_endpoints│
    │   ENDPOINTS = {**get_apache_default_common_endpoints(), ...}            │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    return {
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: / (Página Principal)                                      │
        # │ FUNCIÓN: get_apache_default_home                                │
        # │ APARIENCIA: Apache2 Ubuntu Default Page oficial                 │
        # └─────────────────────────────────────────────────────────────────┘
        '/': get_apache_default_home,
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /robots.txt                                               │
        # │ FUNCIÓN: Lambda que llama build_robots_txt con parámetros       │
        # │ CONFIGURACIÓN: Disallow genérico (/admin/, /backup/)            │
        # └─────────────────────────────────────────────────────────────────┘
        '/robots.txt': lambda: build_robots_txt(
            disallow_paths=['/admin/', '/backup/', '/config/', '/private/'],
            allow_paths=['/public/'],
            crawl_delay=10,
            include_sitemap=True
        ),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /favicon.ico                                              │
        # │ FUNCIÓN: get_favicon_response (desde base.py)                   │
        # │ CONTENIDO: Favicon genérico válido en base64                    │
        # └─────────────────────────────────────────────────────────────────┘
        '/favicon.ico': get_favicon_response,
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /sitemap.xml                                              │
        # │ FUNCIÓN: Lambda que llama build_sitemap_xml                     │
        # │ TRAMPA: Incluye /about y /contact que NO existen (404)          │
        # └─────────────────────────────────────────────────────────────────┘
        '/sitemap.xml': lambda: build_sitemap_xml(
            urls_with_priority=[
                ('/', 1.0),
                ('/about', 0.8),      # TRAMPA: No existe
                ('/contact', 0.5)     # TRAMPA: No existe
            ]
        ),
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /humans.txt                                               │
        # │ FUNCIÓN: get_apache_default_humans                              │
        # │ CONTENIDO: Info genérica de System Administrator                │
        # └─────────────────────────────────────────────────────────────────┘
        '/humans.txt': get_apache_default_humans,
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ RUTA: /.well-known/security.txt                                 │
        # │ FUNCIÓN: Lambda que llama build_security_txt                    │
        # │ CONFIGURACIÓN: Email genérico, dominio localhost                │
        # └─────────────────────────────────────────────────────────────────┘
        '/.well-known/security.txt': lambda: build_security_txt(
            contact_email="security@localhost",
            domain="localhost",
            preferred_languages=["en"]
        ),
    }


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ APACHE2 DEFAULT PAGE?
#    - Es la página MÁS COMÚN en internet
#    - Miles de servidores la tienen (recién instalados, en desarrollo, etc.)
#    - Atacantes la ven constantemente en escaneos masivos
#    - No levanta sospechas
#
# 2. ¿POR QUÉ USAR LAMBDAS?
#    - Sintaxis: lambda: función_con_parámetros()
#    - Permite llamar funciones con parámetros específicos
#    - Ejemplo: lambda: build_robots_txt(disallow_paths=['/admin/'])
#    - Se ejecuta cuando se accede a la ruta, no al definir el diccionario
#
# 3. ¿CÓMO SE USA ESTE GENERADOR?
#    - En generic.py o api.py:
#      from .common.apache_default import get_apache_default_common_endpoints
#      ENDPOINTS = {**get_apache_default_common_endpoints(), ...}
#    - El operador ** "desempaqueta" el diccionario
#
# 4. ¿QUÉ PERFILES USAN ESTE COMMON?
#    - generic.py: Servidor genérico
#    - api.py: API backend (sin frontend elaborado)
#    - Cualquier perfil que quiera parecer "servidor básico"
#
# ═══════════════════════════════════════════════════════════════════════════
