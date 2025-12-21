"""
═══════════════════════════════════════════════════════════════════════════
EASTER EGGS - Rutas Ocultas de Alucard
═══════════════════════════════════════════════════════════════════════════
Contiene easter eggs y señales ocultas para causar paranoia.

EL OJO DE ALUCARD:
- Ruta secreta que muestra un ojo ASCII art
- Solo aparece si se solicita directamente (no está en sitemap)
- Sirve para dar un "susto" o crear paranoia en atacantes
- Logging especial cuando alguien lo encuentra
═══════════════════════════════════════════════════════════════════════════
"""

from ..utils.http_builder import HTTPResponseBuilder

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ EL OJO DE ALUCARD - ASCII ART                                           │
# ├─────────────────────────────────────────────────────────────────────────┤
# │ Un ojo vigilante que simboliza que Alucard está observando              │
# │ Causa paranoia: "¿Me están vigilando? ¿Esto es un honeypot?"            │
# └─────────────────────────────────────────────────────────────────────────┘

ALUCARD_EYE_ART = '''
    ⠀⠀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿⣿⣿⣷⣶⣤⣀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀
    ⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀
    ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⣀⣀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡟⠀⠀⣰⣿⣿⣿⣿⣆⠀⠀⢻⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⠀⠀⣼⣿⣿⣿⣿⣿⣿⣧⠀⠀⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⠿⠿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡀⠀⠹⣿⣿⣶⣶⣿⣿⠏⠀⢀⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣷⡀⠀⠈⠛⠿⠟⠛⠁⠀⢀⣾⣿⣿⣿⣿⣿⣿
    ⠹⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⠏
    ⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀
    ⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢿⣿⣿⣿⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀
    
    ╔═══════════════════════════════════════════════════════════╗
    ║                                                           ║
    ║              I ' M   W A T C H I N G   Y O U              ║
    ║                                                           ║
    ║                      - Alucard                            ║
    ║                                                           ║
    ╚═══════════════════════════════════════════════════════════╝
    
    You found something you weren't supposed to find.
    This server remembers you.
    
    Your IP, your User-Agent, your fingerprint...
    All logged. All tracked. All remembered.
    
    Sweet dreams.
'''

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ VARIANTE: Guiño de Alucard (Más Sutil)                                  │
# └─────────────────────────────────────────────────────────────────────────┘

ALUCARD_WINK = '''
    ⠀⠀⠀⠀⠀⠀⣀⣤⣶⣾⣿⣿⣿⣿⣷⣶⣤⣀⠀⠀⠀⠀⠀⠀
    ⠀⠀⠀⣠⣴⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣦⣄⠀⠀⠀
    ⠀⣠⣾⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣄⠀
    ⣼⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣧
    ⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠛⠉⠉⠛⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀⠀⣀⣀⠀⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⡟⠀⠀⣰⣿⣿⣿⣿⣆⠀⠀⢻⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⠀⠀⣼⣿⣿⣿⣿⣿⣿⣧⠀⠀⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿⣿⣿⠀⠀⣿⣿⣿⣿⣿⣿  ;)
    ⣿⣿⣿⣿⣿⣿⡀⠀⠹⣿⣿⣶⣶⣿⣿⠏⠀⢀⣿⣿⣿⣿⣿⣿
    ⣿⣿⣿⣿⣿⣿⣷⡀⠀⠈⠛⠿⠟⠛⠁⠀⢀⣾⣿⣿⣿⣿⣿⣿
    ⠹⣿⣿⣿⣿⣿⣿⣿⣦⣀⠀⠀⠀⠀⣀⣴⣿⣿⣿⣿⣿⣿⣿⠏
    ⠀⠙⢿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⡿⠋⠀
    ⠀⠀⠀⠙⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠟⠋⠀⠀⠀
    ⠀⠀⠀⠀⠀⠀⠉⠛⠻⠿⢿⣿⣿⣿⡿⠿⠟⠛⠉⠀⠀⠀⠀⠀
    
    *wink*
'''

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ GENERAR RESPUESTAS HTTP PARA EASTER EGGS                                │
# └─────────────────────────────────────────────────────────────────────────┘

def get_alucard_eye_response():
    """Respuesta del ojo de Alucard (versión completa - paranoia)"""
    return HTTPResponseBuilder.build_text(ALUCARD_EYE_ART, "200 OK")

def get_alucard_wink_response():
    """Respuesta del guiño de Alucard (versión sutil)"""
    return HTTPResponseBuilder.build_text(ALUCARD_WINK, "200 OK")

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ DICCIONARIO DE EASTER EGGS                                              │
# ├─────────────────────────────────────────────────────────────────────────┤
# │ IMPORTANTE: Estas rutas NO están en COMMON_PATHS                        │
# │ Solo aparecen si el atacante las pide directamente                      │
# │                                                                          │
# │ RUTAS PROPUESTAS:                                                        │
# │   /.alucard      → Ojo completo (paranoia máxima)                       │
# │   /.watching     → Ojo completo (alternativa)                           │
# │   /eye           → Ojo completo (más obvio)                             │
# │   /.wink         → Guiño sutil                                          │
# │   /hello         → Guiño sutil (más casual)                             │
# └─────────────────────────────────────────────────────────────────────────┘

EASTER_EGG_ENDPOINTS = {
    # Versión completa (paranoia)
    '/.alucard': get_alucard_eye_response,
    '/.watching': get_alucard_eye_response,
    '/eye': get_alucard_eye_response,
    
    # Versión sutil (guiño)
    '/.wink': get_alucard_wink_response,
    '/hello': get_alucard_wink_response,
}

# ┌─────────────────────────────────────────────────────────────────────────┐
# │ NOTA DE USO                                                              │
# ├─────────────────────────────────────────────────────────────────────────┤
# │ Para activar los easter eggs, importar en endpoint_manager.py:          │
# │                                                                          │
# │   from .profiles.easter_eggs import EASTER_EGG_ENDPOINTS                │
# │                                                                          │
# │ Y fusionar en ENDPOINTS:                                                 │
# │                                                                          │
# │   ENDPOINTS = {                                                          │
# │       **COMMON_ENDPOINTS,                                                │
# │       **EASTER_EGG_ENDPOINTS,  # ← Agregar aquí                         │
# │       **GENERIC_ENDPOINTS,                                               │
# │       ...                                                                │
# │   }                                                                      │
# │                                                                          │
# │ LOGGING: Cuando alguien acceda, usar AccessLogger.log_easter_egg_access()│
# └─────────────────────────────────────────────────────────────────────────┘
