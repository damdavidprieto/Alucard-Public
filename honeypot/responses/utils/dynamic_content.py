"""
═══════════════════════════════════════════════════════════════════════════
DYNAMIC CONTENT GENERATOR - Generador de Contenido Dinámico
═══════════════════════════════════════════════════════════════════════════
Genera contenido variable para hacer las respuestas más realistas.

MEJORA CRÍTICA #2: Respuestas Dinámicas
- Timestamps que cambian en cada petición
- Uptimes simulados del servidor
- Session IDs únicos
- Fechas de actualización variables
═══════════════════════════════════════════════════════════════════════════
"""

import datetime
import random
import uuid


class DynamicContentGenerator:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ GENERADOR DE CONTENIDO DINÁMICO                                         │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ QUÉ HACE: Genera datos variables para respuestas HTTP                   │
    │                                                                          │
    │ DATOS QUE GENERA:                                                        │
    │   - Uptime del servidor (días simulados)                                │
    │   - Fechas de última actualización                                      │
    │   - Fechas de expiración (security.txt)                                 │
    │   - Session IDs únicos                                                  │
    │   - Timestamps actuales                                                 │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ ESTADO PERSISTENTE                                                      │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ Simula que el servidor lleva tiempo ejecutándose                        │
    # │ Se inicializa una vez cuando se importa el módulo                       │
    # └─────────────────────────────────────────────────────────────────────────┘
    _server_start_time = datetime.datetime.now() - datetime.timedelta(days=random.randint(30, 180))
    
    @classmethod
    def get_uptime_days(cls) -> int:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ CALCULAR UPTIME DEL SERVIDOR                                        │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Simula cuántos días lleva el servidor ejecutándose                  │
        │ Añade variación aleatoria para parecer más real                     │
        │                                                                      │
        │ EJEMPLO: "Server uptime: 127 days"                                  │
        └─────────────────────────────────────────────────────────────────────┘
        """
        delta = datetime.datetime.now() - cls._server_start_time
        base_days = delta.days
        
        # Añadir variación pequeña (±5 días) para que no sea exacto
        variation = random.randint(-5, 5)
        
        return max(1, base_days + variation)
    
    @staticmethod
    def get_current_timestamp() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ TIMESTAMP ACTUAL                                                     │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Formato legible: "2025-12-13 08:00:17"                              │
        └─────────────────────────────────────────────────────────────────────┘
        """
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    @staticmethod
    def get_last_update_date() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ FECHA DE ÚLTIMA ACTUALIZACIÓN                                       │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Simula que el sitio se actualizó hace 2-30 días                     │
        │ Formato: "2024/11/15"                                               │
        │                                                                      │
        │ USO: Para humans.txt, about pages, etc.                             │
        └─────────────────────────────────────────────────────────────────────┘
        """
        days_ago = random.randint(2, 30)
        date = datetime.datetime.now() - datetime.timedelta(days=days_ago)
        return date.strftime("%Y/%m/%d")
    
    @staticmethod
    def get_security_txt_expiry() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ FECHA DE EXPIRACIÓN PARA SECURITY.TXT                               │
        ├─────────────────────────────────────────────────────────────────────┤
        │ RFC 9116 recomienda expiración en 6-12 meses                        │
        │ Formato: "2025-06-13T08:00:17.000Z" (ISO 8601)                      │
        └─────────────────────────────────────────────────────────────────────┘
        """
        # Expira en 6 meses (180 días)
        expiry = datetime.datetime.now() + datetime.timedelta(days=180)
        return expiry.strftime("%Y-%m-%dT%H:%M:%S.000Z")
    
    @staticmethod
    def generate_session_id() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ GENERAR SESSION ID ÚNICO                                            │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Genera un ID corto y único para cada sesión/petición                │
        │ Formato: "a1b2c3d4" (8 caracteres)                                  │
        │                                                                      │
        │ USO: Tracking, honeytokens, identificación de sesiones              │
        └─────────────────────────────────────────────────────────────────────┘
        """
        return str(uuid.uuid4())[:8]
    
    @staticmethod
    def generate_request_id() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ GENERAR REQUEST ID ÚNICO                                            │
        ├─────────────────────────────────────────────────────────────────────┤
        │ ID más largo para tracking de peticiones individuales               │
        │ Formato: "req_a1b2c3d4-e5f6-g7h8-i9j0-k1l2m3n4o5p6"                │
        └─────────────────────────────────────────────────────────────────────┘
        """
        return f"req_{uuid.uuid4()}"
    
    @staticmethod
    def get_random_load_average() -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ LOAD AVERAGE SIMULADO                                               │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Simula carga del servidor (estilo Unix)                             │
        │ Formato: "0.15, 0.23, 0.18" (1min, 5min, 15min)                     │
        └─────────────────────────────────────────────────────────────────────┘
        """
        load_1min = round(random.uniform(0.05, 0.50), 2)
        load_5min = round(random.uniform(0.10, 0.60), 2)
        load_15min = round(random.uniform(0.08, 0.45), 2)
        
        return f"{load_1min}, {load_5min}, {load_15min}"
