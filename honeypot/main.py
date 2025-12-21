"""
═══════════════════════════════════════════════════════════════════════════
⚠️  EDUCATIONAL HONEYPOT - DISCLAIMER
═══════════════════════════════════════════════════════════════════════════

Este honeypot fue desarrollado con fines ESTRICTAMENTE EDUCATIVOS.

ADVERTENCIAS:
- NO usar en producción
- NO usar sin aislamiento (VM)
- Solo para aprendizaje
- Puede contener vulnerabilidades intencionales

Ver honeypot/README.md para más detalles.
═══════════════════════════════════════════════════════════════════════════
"""

"""
Alucard Honeypot - Main Entry Point
Educational honeypot with modular architecture.
"""

# Importamos herramientas:
# 'time': para controlar tiempos y hacer esperas.
# 'threading': para poder hacer varias cosas a la vez (multitarea).
import time
import threading

# Importamos nuestros servicios falsos (Honeypot) desde la carpeta 'services'.
# HTTPService: Se hará pasar por un servidor web.
# SSHService: Se hará pasar por una terminal remota.
from services import HTTPService, SSHService

def start_honeypot():
    """Función principal que arranca todo el sistema."""
    
    print("=" * 60)
    print("🐝 Alucard Educational Honeypot")
    print("=" * 60)
    print("[!] EDUCATIONAL USE ONLY - See README for disclaimers")
    print("=" * 60)
    
    services = []

    print("[*] Arrancando servicios...")
    
    # 1. HTTP Service
    http_service = HTTPService()
    http_thread = threading.Thread(target=http_service.start, daemon=True)
    http_thread.start()
    services.append(http_service)
    
    # 2. SSH Service
    try:
        ssh_service = SSHService()
        ssh_thread = threading.Thread(target=ssh_service.start, daemon=True)
        ssh_thread.start()
        services.append(ssh_service)
    except Exception as e:
        print(f"[!] SSH Service Error: {e}")

    print("[*] ¡Servicios iniciados!")
    print("[*] HTTP: Puerto 8080")
    print("[*] SSH: Puerto 2222")
    print("[*] Logs: honeypot.log")
    print("=" * 60)
    print("[*] Presiona Ctrl+C para detener")
    
    try:
        while True:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n[*] Apagando honeypot ordenadamente...")
        for s in services:
            if hasattr(s, 'stop'):
                s.stop()
        print("[*] ¡Honeypot detenido!")

if __name__ == "__main__":
    start_honeypot()
