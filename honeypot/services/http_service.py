"""
HTTP honeypot service.
Handles HTTP requests and detects web attacks.
"""

import socket

# Importamos la plantilla maestra (BaseService)
from .base import BaseService
# Importamos el 'Chivato' (Logger) para guardar lo que pase
from core.logger import HoneypotLogger
# Importamos el detector de ataques (el guardia de seguridad)
from detection.http_attacks import HTTPAttackDetector
# Importamos las respuestas falsas (para engañar al atacante)
from responses.endpoint_manager import HTTPEndpoints
import config


# Clase HTTPService
# (BaseService) significa: "Hereda todo del manual BaseService".
# No tenemos que reescribir la lógica de sockets/threads, ya la tenemos gratis.
class HTTPService(BaseService):
    """Servicio Honeypot para simular un servidor Web (HTTP)"""
    
    def __init__(self, host: str = None, port: int = None):
        """Inicializamos el servicio web"""
        import os
        # Si no nos dan IP/Puerto, usamos los de config.py
        host = host or config.HTTP_HOST
        # En la nube (Cloud Run), el puerto nos lo da el entorno (os.environ).
        port = port or int(os.environ.get("PORT", config.HTTP_PORT))
        
        # SUPER: Llamamos al constructor del padre (BaseService).
        # Es como decir: "Papá, inicializa la parte aburrida de los sockets por mí".
        super().__init__(host, port, "HTTP Honeypot")
    
    # ESTO ES LO IMPORTANTE.
    # BaseService nos obligaba a implementar 'handle_client'. Aquí está.
    # Esta función se ejecuta en su propio hilo para cada cliente.
    def handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        Manejar la conexión de un visitante.
        Aquí es donde 'hablamos' HTTP.
        
        Args:
            client_socket: El teléfono privado con el visitante.
            address: Su (IP, Puerto).
        """
        try:
            # 1. RECIBIR DATOS (OÍR)
            # recv(BUFFER_SIZE): Escuchamos lo que nos dicen.
            # decode('utf-8'): Convertimos los sonidos (bytes) a palabras (texto).
            # errors='ignore': Si dicen algo raro que no entendemos, lo ignoramos para no explotar.
            data = client_socket.recv(config.BUFFER_SIZE).decode('utf-8', errors='ignore')
            
            if not data:
                return # Si no dicen nada, colgamos.
            
            # 2. ENTENDER LA PETICIÓN
            # Analizamos qué piden (ej: "GET /admin/login.php")
            # Y AHORA TAMBIÉN: Quiénes son (Headers) y Qué traen (Body)
            method, path, headers, body = self._parse_request(data)
            
            # 3. DETECTAR ATAQUES (ANALIZAR)
            # Le pasamos el texto al experto en seguridad.
            detected_attacks = HTTPAttackDetector.detect(data)
            
            # Extraemos el User-Agent (o ponemos 'Unknown' si no lo envían)
            user_agent = headers.get('User-Agent', 'Unknown')
            
            # 4. REGISTRAR TODO (CHIVARSE)
            # Guardamos todo en el log: quién, qué pidió, y qué ataques detectamos.
            HoneypotLogger.log_connection(
                service='HTTP',
                ip=address[0],
                port=address[1],
                data=data[:config.LOG_DATA_MAX_LENGTH], 
                extra={
                    'method': method,
                    'path': path,
                    'user_agent': user_agent,
                    'all_headers': headers, # ¡NUEVO! Todas las cabeceras
                    'payload_body': body[:1024], # ¡NUEVO! El cuerpo (limitado)
                    'attacks_detected': detected_attacks
                }
            )
            
            # 5. RESPONDER (HABLAR)
            # Buscamos qué respuesta falsa darle según lo que pidió.
            # LE PASAMOS EL USER-AGENT para que el camarero sepa si darle el "menú trampa".
            response = HTTPEndpoints.get_response(path, user_agent)
            # encode('utf-8'): Convertimos nuestro texto a bytes para enviarlo por el cable.
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"[!] Error en HTTP handler: {e}")
        finally:
            # 6. COLGAR (LIMPIEZA)
            try:
                client_socket.close()
            except:
                pass
    
    def _parse_request(self, data: str) -> tuple:
        """
        Analiza la petición HTTP completa.
        Extrae Método, Ruta, Cabeceras (Headers) y Cuerpo (Body).
        """
        headers = {}
        body = ""
        
        # Separar cabeceras y cuerpo
        parts = data.split('\r\n\r\n', 1)
        header_part = parts[0]
        body = parts[1] if len(parts) > 1 else ""
        
        lines = header_part.split('\r\n')
        
        # 1. Request Line
        if not lines:
            return 'UNKNOWN', '/', headers, body
            
        request_line = lines[0]
        req_parts = request_line.split(' ')
        method = req_parts[0] if len(req_parts) > 0 else 'UNKNOWN'
        path = req_parts[1] if len(req_parts) > 1 else '/'
        
        # 2. Extract Headers
        for line in lines[1:]:
            if not line: break
            if ':' in line:
                key, value = line.split(':', 1)
                headers[key.strip()] = value.strip()
                
        return method, path, headers, body
