"""
═══════════════════════════════════════════════════════════════════════════
COMMON PROFILES PACKAGE - Exportaciones principales
═══════════════════════════════════════════════════════════════════════════
Este archivo __init__.py hace que el directorio 'common' sea un paquete Python
y exporta las funciones principales de cada generador de perfil común.

ESTRUCTURA DEL PAQUETE:
common/
├── __init__.py              ← Este archivo (exportaciones)
├── base.py                  ← Utilidades compartidas
├── apache_default.py        ← Generador para servidores genéricos
├── corporate.py             ← Generador para sitios corporativos
└── device.py                ← Generador para dispositivos IoT

USO DESDE OTROS MÓDULOS:
    from .common import (
        get_apache_default_common_endpoints,
        get_corporate_common_endpoints,
        get_device_common_endpoints
    )

EXPLICACIÓN PYTHON:
- __init__.py convierte un directorio en un paquete importable
- Sin este archivo, Python no reconocería 'common' como paquete
- Las importaciones aquí facilitan el acceso desde otros módulos
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTAR GENERADORES DE PERFILES COMUNES
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN:
# - "from .apache_default import ..." = Importar desde apache_default.py
# - El punto "." significa "en el mismo directorio"
# - Importamos las funciones principales que otros módulos necesitarán
# ═══════════════════════════════════════════════════════════════════════════

from .apache_default import get_apache_default_common_endpoints
# ↑ Generador para servidores genéricos (Apache2 Ubuntu Default Page)
# USO: Perfiles generic.py, api.py

from .corporate import get_corporate_common_endpoints
# ↑ Generador para sitios corporativos (landing page empresarial)
# USO: Perfiles wordpress.py, aplicaciones de negocio

from .device import get_device_common_endpoints
# ↑ Generador para dispositivos IoT (login page estilo router)
# USO: Perfiles iot.py, cámaras, routers


# ═══════════════════════════════════════════════════════════════════════════
# LISTA __all__ - EXPORTACIONES PÚBLICAS
# ═══════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN PYTHON:
# - __all__ define qué se exporta cuando alguien hace "from common import *"
# - Es una lista de strings con los nombres de las funciones/clases públicas
# - Buena práctica: Definir explícitamente qué es público
# ═══════════════════════════════════════════════════════════════════════════

__all__ = [
    'get_apache_default_common_endpoints',  # Apache2 default page
    'get_corporate_common_endpoints',       # Corporate landing page
    'get_device_common_endpoints',          # IoT device login page
]


# ═══════════════════════════════════════════════════════════════════════════
# NOTAS TÉCNICAS
# ═══════════════════════════════════════════════════════════════════════════
#
# 1. ¿POR QUÉ NECESITAMOS __init__.py?
#    - Python 3.3+ permite paquetes sin __init__.py (namespace packages)
#    - PERO es mejor práctica incluirlo para:
#      * Controlar qué se exporta
#      * Inicializar el paquete si es necesario
#      * Documentar el paquete
#
# 2. ¿CÓMO SE USA ESTE PAQUETE?
#    - Desde wordpress.py:
#      from .common import get_corporate_common_endpoints
#      ENDPOINTS = {**get_corporate_common_endpoints(...), ...}
#
#    - Desde api.py:
#      from .common import get_apache_default_common_endpoints
#      ENDPOINTS = {**get_apache_default_common_endpoints(), ...}
#
#    - Desde iot.py:
#      from .common import get_device_common_endpoints
#      ENDPOINTS = {**get_device_common_endpoints(...), ...}
#
# 3. ¿QUÉ PASA SI NO IMPORTAMOS base.py AQUÍ?
#    - base.py contiene utilidades internas (favicon, robots.txt builders)
#    - NO necesita ser importado aquí porque:
#      * Los generadores (apache_default, corporate, device) ya lo importan
#      * Los perfiles (wordpress, api, iot) no lo usan directamente
#    - Solo exportamos las funciones de alto nivel
#
# 4. ¿POR QUÉ USAR IMPORTACIONES RELATIVAS (.apache_default)?
#    - Importaciones relativas (con punto) son más robustas
#    - Funcionan aunque el paquete se mueva o renombre
#    - Evitan conflictos de nombres
#
# ═══════════════════════════════════════════════════════════════════════════
