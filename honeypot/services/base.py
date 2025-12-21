"""
Base service class for all honeypot services.
Provides common interface and socket management.
"""

import socket
import threading
from abc import ABC, abstractmethod


# Definimos una 'Clase Abstracta' (ABC).
# Esto no es un servicio real, es una PLANTILLA.
# Obliga a quien la use (como HTTPService) a seguir ciertas reglas.
class BaseService(ABC):
    """Clase base (plantilla) para todos los servicios del honeypot"""
    
    def __init__(self, host: str, port: int, service_name: str):
        """
        Constructor: Se ejecuta al crear el servicio.
        Aquí guardamos la configuración inicial.
        """
        # "self" es la memoria del objeto. Guardamos estos datos para usarlos luego.
        self.host = host              # La IP donde escucharemos (ej: 0.0.0.0)
        self.port = port              # El puerto (ej: 8080)
        self.service_name = service_name # Nombre para los logs (ej: "HTTP Honeypot")
        self.server_socket = None     # Aquí guardaremos el "teléfono" (socket) cuando lo creemos
        self.running = False          # Semáforo para saber si debemos seguir funcionando
    
    def start(self) -> None:
        """Función para ARRANCAR el servicio y ponerse a escuchar"""
        
        # 1. CREAR EL SOCKET (El Teléfono)
        # AF_INET = Usar direcciones IP (Internet)
        # SOCK_STREAM = Usar protocolo TCP (fiable, como una llamada telefónica)
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Esta línea es un truco técnico: "Si cierro el programa, libera el puerto INMEDIATAMENTE".
        # Evita el error "Address already in use" si reinicias rápido.
        self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        try:
            # 2. BIND (Asignar número)
            # Decimos "Este teléfono responde en esta IP y este Puerto".
            self.server_socket.bind((self.host, self.port))
            
            # 3. LISTEN (Esperar llamadas)
            # Empezamos a escuchar. El '5' es la cola de espera máxima.
            self.server_socket.listen(5)
            self.running = True
            
            print(f"[*] {self.service_name} escuchando en {self.host}:{self.port}")
            
            # 4. BUCLE DE ATENCIÓN
            # Mientras el servicio esté marcado como 'running', seguimos aceptando llamadas.
            while self.running:
                try:
                    # ACCEPT (Descolgar el teléfono)
                    # ¡CUIDADO! Esta línea CONGELA el programa aquí hasta que entra alguien.
                    # client_socket: Una conexión privada EXCLUSIVA con ese cliente.
                    # address: La IP:Puerto de quien llama.
                    client_socket, address = self.server_socket.accept()
                    
                    # 5. DELEGAR (Multitarea)
                    # Si atendiéramos al cliente aquí, bloquearíamos la puerta.
                    # En lugar de eso, contratamos a un trabajador (hilo) para que lo atienda.
                    threading.Thread(
                        target=self.handle_client,      # Ve a ejecutar esta función
                        args=(client_socket, address),  # Con estos datos
                        daemon=True                     # Muere si el jefe muere
                    ).start()
                    
                except Exception as e:
                    if self.running:
                        print(f"[!] {self.service_name} error al aceptar conexión: {e}")
                    
        except Exception as e:
            print(f"[!] {self.service_name} error crítico: {e}")
        finally:
            # Si algo falla gravemente, nos aseguramos de cerrar todo.
            self.stop()
    
    def stop(self) -> None:
        """Función para APAGAR el servicio"""
        self.running = False
        if self.server_socket:
            try:
                # Colgamos el teléfono principal.
                self.server_socket.close()
            except:
                pass
    
    # Esto es un método ABSTRACTO.
    # Significa: "Yo (la plantilla) no sé cómo hacer esto, pero tú (HTTPService/SSHService) ESTÁS OBLIGADO a implementarlo".
    @abstractmethod
    def handle_client(self, client_socket: socket.socket, address: tuple) -> None:
        """
        Manejar la conexión con un cliente específico.
        Cada servicio (Web, SSH) tiene que decidir cómo hace esto.
        """
        pass
