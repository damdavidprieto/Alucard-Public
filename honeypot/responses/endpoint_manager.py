"""
═══════════════════════════════════════════════════════════════════════════
ENDPOINT MANAGER - Gestor Centralizado de Endpoints HTTP
═══════════════════════════════════════════════════════════════════════════
Este es el nuevo archivo principal que reemplaza a http_endpoints.py.
Importa todos los perfiles y gestiona las respuestas HTTP del honeypot.

ARQUITECTURA:
- Importa endpoints de profiles/ (common, generic, wordpress, etc.)
- Usa ScannerDetector para detectar herramientas de hacking
- Gestiona el filtrado por perfil activo
- Devuelve respuestas HTTP apropiadas
═══════════════════════════════════════════════════════════════════════════
"""

# ═══════════════════════════════════════════════════════════════════════════
# IMPORTS
# ═══════════════════════════════════════════════════════════════════════════

# Importar todos los perfiles de endpoints
from .profiles import (
    GENERIC_ENDPOINTS,
    WORDPRESS_ENDPOINTS,
    API_ENDPOINTS,
    DATABASE_ENDPOINTS,
    IOT_ENDPOINTS,
    IOT_TAPO_ENDPOINTS,
    DEVOPS_ENDPOINTS,
)

# NOTA: COMMON_ENDPOINTS ya no existe como entidad separada
# Los endpoints comunes (/, /robots.txt, etc.) ahora están integrados
# en cada perfil usando el sistema de common profiles (common/)

# Importar detector de scanners
from .detectors import ScannerDetector


# ═══════════════════════════════════════════════════════════════════════════
# CLASE PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════

class HTTPEndpoints:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GESTOR CENTRALIZADO DE ENDPOINTS HTTP                                   │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ QUÉ HACE: Gestiona todas las respuestas HTTP del honeypot               │
    │                                                                          │
    │ RESPONSABILIDADES:                                                       │
    │   1. Fusionar todos los perfiles en un solo diccionario                 │
    │   2. Detectar herramientas de hacking (SQLMap, Nmap, etc.)              │
    │   3. Filtrar endpoints según el perfil activo                           │
    │   4. Normalizar rutas (quitar parámetros)                               │
    │   5. Buscar y devolver la respuesta apropiada                           │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ DICCIONARIO MAESTRO DE ENDPOINTS                                        │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Fusiona TODOS los perfiles en un solo diccionario                       │
    # │ Usa el operador ** para "desempaquetar" cada diccionario                │
    # │                                                                          │
    # │ EJEMPLO: {**dict1, **dict2} = {key1: val1, key2: val2, ...}             │
    # └─────────────────────────────────────────────────────────────────────────┘
    ENDPOINTS = {
        **GENERIC_ENDPOINTS,     # Servidor básico (incluye common apache_default)
        **WORDPRESS_ENDPOINTS,   # WordPress (incluye common corporate)
        **API_ENDPOINTS,         # API REST (incluye common apache_default)
        **DATABASE_ENDPOINTS,    # Herramientas de BBDD
        **IOT_ENDPOINTS,         # Dispositivos IoT (Route TP-Link)
        **IOT_TAPO_ENDPOINTS,    # Cámaras Tapo C200
        **DEVOPS_ENDPOINTS,      # Fugas de configuración
    }
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RESPUESTA POR DEFECTO (404 Not Found)                                   │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Se devuelve cuando no encontramos la ruta solicitada                    │
    # └─────────────────────────────────────────────────────────────────────────┘
    NOT_FOUND = 'HTTP/1.1 404 Not Found\r\nContent-Type: text/html\r\n\r\n<html><body><h1>404 Not Found</h1><p>The requested URL was not found on this server.</p></body></html>'
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODO PRINCIPAL: get_response()
    # ═══════════════════════════════════════════════════════════════════════════
    
    @classmethod
    def get_response(cls, path: str, user_agent: str = None) -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────────┐
        │ MÉTODO PRINCIPAL: El Camarero del Honeypot                              │
        ├─────────────────────────────────────────────────────────────────────────┤
        │ QUÉ HACE: Decide qué respuesta HTTP enviar al atacante                  │
        │ PASOS:                                                                   │
        │   1. Verifica si la ruta está permitida por el perfil activo            │
        │   2. Detecta herramientas de hacking (SQLMap, Nmap, etc.)               │
        │   3. Normaliza la ruta (quita parámetros)                               │
        │   4. Busca la respuesta correspondiente                                 │
        │   5. Si no encuentra nada, devuelve 404                                 │
        └─────────────────────────────────────────────────────────────────────────┘
        """
        import config
        profile = getattr(config, 'HONEYPOT_PROFILE', 'all')
        
        # ┌─────────────────────────────────────────────────────────────────────┐
        # │ PASO 0: Filtrado por Perfil                                         │
        # ├─────────────────────────────────────────────────────────────────────┤
        # │ Verifica si esta ruta está permitida en el perfil actual            │
        # │ Ejemplo: Si perfil='wordpress', solo muestra rutas de WordPress     │
        # └─────────────────────────────────────────────────────────────────────┘
        if not cls._is_path_allowed(path, profile):
             return cls.NOT_FOUND

        # ┌─────────────────────────────────────────────────────────────────────┐
        # │ PASO 1: Detección de Herramientas de Hacking                        │
        # ├─────────────────────────────────────────────────────────────────────┤
        # │ Delega la detección a ScannerDetector                               │
        # │ Si detecta algo, devuelve respuesta trampa inmediatamente           │
        # └─────────────────────────────────────────────────────────────────────┘
        scanner_response = ScannerDetector.detect(user_agent)
        if scanner_response:
            return scanner_response

        # ┌─────────────────────────────────────────────────────────────────────┐
        # │ PASO 2: Normalización de la Ruta                                    │
        # ├─────────────────────────────────────────────────────────────────────┤
        # │ Limpia la ruta quitando parámetros de query y fragmentos            │
        # │ Ejemplo: /admin?id=123#top → /admin                                 │
        # └─────────────────────────────────────────────────────────────────────┘
        clean_path = cls._normalize_path(path)

        # ┌─────────────────────────────────────────────────────────────────────┐
        # │ PASO 3: Búsqueda de Respuesta                                       │
        # ├─────────────────────────────────────────────────────────────────────┤
        # │ Busca la respuesta en el diccionario ENDPOINTS                      │
        # │ Primero intenta coincidencia exacta, luego pattern matching         │
        # └─────────────────────────────────────────────────────────────────────┘
        response = cls._find_matching_endpoint(clean_path)
        
        # ┌─────────────────────────────────────────────────────────────────────┐
        # │ PASO 4: Respuesta Final                                             │
        # ├─────────────────────────────────────────────────────────────────────┤
        # │ Si encontramos algo, lo devolvemos. Si no, 404 Not Found            │
        # └─────────────────────────────────────────────────────────────────────┘
        return response if response else cls.NOT_FOUND
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES (Fragmentación del código)
    # ═══════════════════════════════════════════════════════════════════════════
    
    @staticmethod
    def _normalize_path(path: str) -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────────┐
        │ NORMALIZADOR DE RUTAS                                                   │
        ├─────────────────────────────────────────────────────────────────────────┤
        │ QUÉ HACE: Limpia la ruta para facilitar la búsqueda                     │
        │ LIMPIEZA:                                                                │
        │   - Quita parámetros de query (?id=123&debug=true)                      │
        │   - Quita fragmentos (#section)                                         │
        │                                                                          │
        │ EJEMPLO: /admin?id=123#top → /admin                                     │
        └─────────────────────────────────────────────────────────────────────────┘
        """
        # Quitar parámetros de query (todo después del ?)
        clean_path = path.split('?')[0]
        
        # Quitar fragmentos (todo después del #)
        clean_path = clean_path.split('#')[0]
        
        return clean_path
    
    @classmethod
    def _find_matching_endpoint(cls, clean_path: str) -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────────┐
        │ BUSCADOR DE ENDPOINTS                                                   │
        ├─────────────────────────────────────────────────────────────────────────┤
        │ QUÉ HACE: Busca la respuesta HTTP correspondiente a la ruta             │
        │ ESTRATEGIA:                                                              │
        │   1. Coincidencia EXACTA: /admin → /admin                               │
        │   2. Pattern Matching: /api/v1/users/123 → /api/v1/users               │
        │                                                                          │
        │ RETORNA: Respuesta HTTP si encuentra, None si no encuentra              │
        └─────────────────────────────────────────────────────────────────────────┘
        """
        # ESTRATEGIA 1: Coincidencia Exacta
        # Ejemplo: Si pide "/admin", buscamos exactamente "/admin"
        if clean_path in cls.ENDPOINTS:
            return cls.ENDPOINTS[clean_path]
        
        # ESTRATEGIA 2: Pattern Matching (para APIs con IDs)
        # Ejemplo: /api/v1/users/123 coincide con /api/v1/users
        # Útil para APIs RESTful donde hay IDs dinámicos
        for endpoint_pattern, response in cls.ENDPOINTS.items():
            # Si la ruta solicitada empieza con el patrón del endpoint
            if clean_path.startswith(endpoint_pattern + '/'):
                return response
        
        # No encontramos nada
        return None
    
    # ═══════════════════════════════════════════════════════════════════════════
    # MÉTODOS AUXILIARES (Compatibilidad)
    # ═══════════════════════════════════════════════════════════════════════════
    
    @classmethod
    def add_endpoint(cls, path: str, response: str) -> None:
        """
        ┌─────────────────────────────────────────────────────────────────────────┐
        │ AGREGAR ENDPOINT DINÁMICAMENTE                                          │
        ├─────────────────────────────────────────────────────────────────────────┤
        │ Permite agregar endpoints en tiempo de ejecución                        │
        │ Útil para testing o personalización dinámica                            │
        └─────────────────────────────────────────────────────────────────────────┘
        """
        cls.ENDPOINTS[path] = response
    
    @classmethod
    def get_all_paths(cls) -> list:
        """
        ┌─────────────────────────────────────────────────────────────────────────┐
        │ LISTAR TODOS LOS ENDPOINTS ACTIVOS                                      │
        ├─────────────────────────────────────────────────────────────────────────┤
        │ Devuelve lista de rutas disponibles según el perfil activo              │
        │ Útil para debugging y logging                                           │
        └─────────────────────────────────────────────────────────────────────────┘
        """
        import config
        profile = getattr(config, 'HONEYPOT_PROFILE', 'all')
        return [p for p in cls.ENDPOINTS.keys() if cls._is_path_allowed(p, profile)]

    @staticmethod
    def _is_path_allowed(path: str, profile: str) -> bool:
        """
        ┌─────────────────────────────────────────────────────────────────────────┐
        │ FILTRO DE PERFILES                                                      │
        ├─────────────────────────────────────────────────────────────────────────┤
        │ Define qué rutas están activas para cada perfil de honeypot             │
        │                                                                          │
        │ LÓGICA:                                                                  │
        │   1. Si perfil='all' → Permitir TODO                                    │
        │   2. Si es ruta común → Siempre permitir                                │
        │   3. Si coincide con keywords del perfil → Permitir                     │
        │   4. Si no coincide → Bloquear (404)                                    │
        └─────────────────────────────────────────────────────────────────────────┘
        """
        
        # PERFIL 'ALL' (Cazamos todo)
        if profile == 'all':
            return True

        # NOTA: Ya no verificamos COMMON_PATHS porque los endpoints comunes
        # ahora están integrados en cada perfil. Cada perfil incluye sus propios
        # endpoints comunes (/, /robots.txt, /favicon.ico, etc.)

        # 1. Cargar perfiles desde profiles.json
        import json
        import os
        
        # Ruta al archivo JSON (subimos un nivel desde responses/)
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        json_path = os.path.join(base_dir, 'profiles.json')
        
        try:
            with open(json_path, 'r') as f:
                profiles = json.load(f)
        except Exception as e:
            # Fallback seguro si falla el JSON
            print(f"[!] Error loading profiles.json: {e}")
            return True  # Fail Open (mostrar todo si hay error)

        # 3. Verificar si la ruta pertenece al perfil activo
        # Buscamos si ALGUNA de las palabras clave del perfil está en la ruta
        keywords = profiles.get(profile, [])
        for keyword in keywords:
            if keyword in path:
                return True
                
        # 4. Si no encaja, ocultar (return False)
        return False
