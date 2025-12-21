"""
Profiles package - Endpoints organizados por perfil de honeypot.

Cada archivo representa un perfil diferente:
- generic.py: Servidor básico
- wordpress.py: CMS WordPress
- api.py: Backend empresarial
- database.py: Herramientas de BBDD
- iot.py: Dispositivos IoT
- devops.py: Fugas de configuración

NOTA: Los endpoints comunes (/, /robots.txt, /favicon.ico, etc.) ahora están
integrados en cada perfil usando el sistema de common profiles (common/).
"""

from .generic import GENERIC_ENDPOINTS
from .wordpress import WORDPRESS_ENDPOINTS
from .api import API_ENDPOINTS
from .database import DATABASE_ENDPOINTS
from .iot import IOT_ENDPOINTS
from .iot_tapo import IOT_TAPO_ENDPOINTS
from .devops import DEVOPS_ENDPOINTS

__all__ = [
    'GENERIC_ENDPOINTS',
    'WORDPRESS_ENDPOINTS',
    'API_ENDPOINTS',
    'DATABASE_ENDPOINTS',
    'IOT_ENDPOINTS',
    'IOT_TAPO_ENDPOINTS',
    'DEVOPS_ENDPOINTS',
]
