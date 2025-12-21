"""
RTSP honeypot service.
Simulates a Real Time Streaming Protocol server (for IP Cameras).
"""

import socket
import logging
from .base import BaseService
from core.logger import HoneypotLogger
import config

class RTSPService(BaseService):
    """Servicio Honeypot para simular una Cámara IP (RTSP)"""
    
    def __init__(self, host: str = None, port: int = 554):
        """Inicializamos el servicio RTSP"""
        # IMPORTANTE: Port 554 es el estándar RTSP
        # Si falla por permisos (requiere admin), el usuario deberá cambiarlo o ejecutar como admin.
        super().__init__(host or config.HTTP_HOST, port, "RTSP Camera")
        
    def handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        Manejar handshake RTSP.
        El objetivo es pedir autenticación siempre.
        """
        try:
            # 1. RECIBIR
            data = client_socket.recv(config.BUFFER_SIZE).decode('utf-8', errors='ignore')
            
            if not data:
                return

            # Extraer método (OPTIONS, DESCRIBE, SETUP, PLAY)
            first_line = data.split('\r\n')[0]
            method = first_line.split(' ')[0] if ' ' in first_line else 'UNKNOWN'
            
            # 2. LOGGING
            HoneypotLogger.log_connection(
                service='RTSP',
                ip=address[0],
                port=address[1],
                data=data[:config.LOG_DATA_MAX_LENGTH],
                extra={'method': method, 'payload': data}
            )
            
            # 3. RESPONDEMOS SIMULANDO TAPO C200
            # Secuencia típica:
            # Cliente: OPTIONS rtsp://...
            # Servidor: 200 OK (Public: ...)
            # Cliente: DESCRIBE rtsp://...
            # Servidor: 401 Unauthorized (Digest realm="TP-Link...")
            
            cseq = "1"
            # Intentar extraer CSeq del cliente para responder con el mismo
            for line in data.split('\r\n'):
                if line.startswith('CSeq:'):
                    cseq = line.split(':')[1].strip()
                    break

            if method == 'OPTIONS':
                # Respuesta a OPTIONS: "Hola, hablo RTSP"
                response = (
                    f"RTSP/1.0 200 OK\r\n"
                    f"CSeq: {cseq}\r\n"
                    f"Public: OPTIONS, DESCRIBE, SETUP, TEARDOWN, PLAY, PAUSE, GET_PARAMETER, SET_PARAMETER\r\n"
                    f"\r\n"
                )
            else:
                # A CUALQUIER OTRA COSA (DESCRIBE, SETUP...): "Identifícate"
                # Simulamos la auth de TP-Link
                response = (
                    f"RTSP/1.0 401 Unauthorized\r\n"
                    f"CSeq: {cseq}\r\n"
                    f"WWW-Authenticate: Digest realm=\"IP Camera(A2497)\", nonce=\"5f9a6e12\", algorithm=\"MD5\"\r\n"
                    f"WWW-Authenticate: Basic realm=\"IP Camera(A2497)\"\r\n"
                    f"\r\n"
                )
            
            client_socket.send(response.encode('utf-8'))
            
        except Exception as e:
            print(f"[!] Error en RTSP handler: {e}")
        finally:
            try:
                client_socket.close()
            except:
                pass
