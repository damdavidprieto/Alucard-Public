# 📘 Guía de Aprendizaje: Alucard Honeypot

Esta guía está diseñada para enseñarte Python y conceptos de programación de sistemas y redes utilizando el código de tu propio honeypot.

---

## Capítulo 1: El Director de Orquesta (`main.py`)

El archivo `main.py` es el punto de entrada. Es pequeño, pero introduce conceptos fundamentales.

### 1. Sistema de Módulos (`import`)
Python es modular. No escribimos todo en un archivo.
```python
from services import HTTPService, SSHService
```
*   **Concepto**: Esto busca una carpeta llamada `services`. Dentro de esa carpeta debe haber un archivo especial `__init__.py` que le dice a Python que esa carpeta es un "paquete".
*   **Por qué**: Nos permite separar lógica. El código web va en un lado, el SSH en otro, y `main.py` solo los coordina.

### 2. Concurrencia (`threading`)
```python
http_thread = threading.Thread(target=http_service.start, daemon=True)
http_thread.start()
```
*   **El Problema**: Un servidor, como un servidor web, se queda "escuchando" esperando a que alguien se conecte. Esta operación es **bloqueante**. Si pusieras `http_service.start()` directamente, el programa se detendría en esa línea para siempre y nunca arrancaría el servicio SSH.
*   **La Solución**: **Hilos (Threads)**. Imagina que tu programa principal es una carretera principal. Al crear un `Thread`, creas un carril paralelo. El servicio web corre en su propio carril, y el programa principal sigue adelante inmediatamente para arrancar el SSH en otro carril.
*   **Daemon Threads**: `daemon=True` indica que son hilos "sirvientes". Si el hilo principal (el programa `main.py`) se cierra, estos hilos mueren automáticamente. Si fuera `False`, el programa no se cerraría hasta que estos hilos terminen (y como son servidores, nunca terminan por sí mismos).

### 3. El Bucle Infinito (`while True`)
```python
while True:
    time.sleep(1)
```
*   **Por qué**: Como lanzamos el servidor Web y el SSH en hilos secundarios (daemons), el hilo principal se queda sin nada que hacer. Si no ponemos nada, llegaría al final del archivo y el programa se cerraría (matando a los daemons con él).
*   **`time.sleep(1)`**: Esto es crucial. Sin esto, el bucle `while True` giraría millones de veces por segundo, poniendo tu CPU al 100% haciendo absolutamente nada. `sleep(1)` le dice al procesador: "Despiértame en un segundo". Esto reduce el uso de CPU casi a 0%.

### 4. Manejo de Excepciones (`try...except`)
```python
except KeyboardInterrupt:
```
*   **Concepto**: Cuando pulsas `Ctrl+C` en la terminal, el sistema operativo envía una señal de interrupción. Python convierte esto en un error llamado `KeyboardInterrupt`.
*   **Manejo**: Al envolver el bucle en un bloque `try`, "atrapamos" ese error para cerrar el programa limpiamente (mostrando un mensaje de despedida) en lugar de que el programa explote con un error feo en pantalla.

---

## Siguiente Paso: `services/base.py`
Ahora que sabemos cómo arranca, el siguiente paso lógico es ver **qué es un servicio**.
El archivo `services/base.py` contiene la "plantilla maestra" (Clase Padre) de la que heredan todos nuestros servicios. Ahí aprenderemos sobre **Herencia** y **Sockets**.

---

## Capítulo 2: La Plantilla Maestra (`services/base.py`)

Si `main.py` es el jefe, `base.py` es el manual de instrucciones que deben seguir todos los empleados (servicios).

### 1. Clases y Objetos (`class`)
```python
class BaseService(ABC):
```
*   **Clase**: Es como un plano de arquitectura. No es la casa real, sino las instrucciones para construirla.
*   **Objeto**: Es la casa construida. `http_service` en `main.py` es un objeto construido usando el plano `HTTPService`.
*   **Herencia (`ABC`)**: Aquí usamos algo avanzado llamado "Clase Abstracta". Funciona como un contrato. Al decir que `BaseService` es abstracta, obligamos a cualquiera que la use (como `HTTPService`) a cumplir ciertas reglas, como tener una función `handle_client`.

### 2. El Constructor (`__init__`)
```python
def __init__(self, host: str, port: int, service_name: str):
    self.host = host
    self.port = port
```
*   Esta función se ejecuta automáticamente cuando creas el servicio.
*   **`self`**: Representa "a mí mismo". Cuando guardamos `self.port = port`, estamos guardando ese dato en la "memoria" de ese objeto específico. Así, el servicio HTTP recuerda que es el puerto 8080 y el SSH recuerda que es el 2222, usando el mismo código.

### 3. Sockets: Las Tuberías de Internet
```python
self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
self.server_socket.bind((self.host, self.port))
self.server_socket.listen(5)
```
Esto es pura programación de redes:
1.  **`socket()`**: Crea el teléfono.
2.  **`bind()`**: Asigna el número de teléfono (IP y Puerto). Si el puerto está ocupado por otro programa, aquí fallará.
3.  **`listen(5)`**: Empieza a esperar llamadas. El `5` es la "cola de espera"; si llaman 6 personas a la vez, el sexto recibe tono de ocupado.

### 4. El Bucle de Atención (`accept`)
```python
while self.running:
    client_socket, address = self.server_socket.accept()
```
*   **`accept()`**: Esta es la línea mágica. El programa se detiene aquí y espera. NO hace nada hasta que alguien se conecta.
*   Cuando alguien entra, `accept` despierta y nos da dos cosas:
    1.  `client_socket`: Una nueva tubería exclusiva para hablar con ESE cliente específico.
    2.  `address`: La IP y puerto de quien nos llama (ej: `192.168.1.50`).

### 5. Multitarea por Cliente
```python
threading.Thread(target=self.handle_client, ...).start()
```
*   Si atendiéramos al cliente directamente ahí, nadie más podría conectarse hasta que termináramos con él.
*   Por eso, lanzamos **otro hilo más** para cada cliente que llega.
*   **Visualización**:
    *   Hilo Principal (`main.py`): Supervisa todo.
    *   Hilo Servicio HTTP (`BaseService.start`): Está en la puerta esperando clientes.
    *   Hilo Cliente 1 (`handle_client`): Atendiendo a Juan.
    *   Hilo Cliente 2 (`handle_client`): Atendiendo a María.

---

## Siguiente Paso: Implementación Real (`services/http_service.py`)
Ya tenemos la plantilla. Ahora veamos cómo se usa para crear un servicio real.
En `services/http_service.py` veremos cómo "rellenamos" los huecos de la plantilla para entender el protocolo HTTP (GET, POST, etc.) y cómo detectamos ataques.

---

## Capítulo 3: El Especialista (`services/http_service.py`)

Aquí es donde la programación orientada a objetos brilla. `HTTPService` no necesita saber cómo abrir un socket o aceptar conexiones, porque eso ya lo hace su padre (`BaseService`). Solo se preocupa de hablar "idioma Web" (HTTP).

### 1. La Herencia en Acción
```python
class HTTPService(BaseService):
```
*   Al poner `(BaseService)`, le decimos: "Tú eres un `BaseService`. Tienes todo lo que él tiene (funciones `start`, `stop`, variables `host`, `port`).

### 2. Cumpliendo el Contrato (`handle_client`)
Recuerda que `BaseService` tenía un método abstracto `handle_client`. Aquí **estamos obligados** a escribirlo.
```python
def handle_client(self, client_socket, address):
```
Esta función es lo que ejecuta el "trabajador" (hilo) que creamos en `base.py`.

### 3. Recibiendo Datos (`recv`)
```python
data = client_socket.recv(4096).decode('utf-8')
```
1.  `recv(4096)`: "Lee hasta 4096 bytes de la tubería".
2.  `decode('utf-8')`: Los ordenadores envían bytes (números). Esto los convierte en texto legible.

### 4. Detectando Ataques
```python
detected_attacks = HTTPAttackDetector.detect(data)
```
Aquí delegamos el trabajo sucio a otro experto (`HTTPAttackDetector`). Es como si el recepcionista llamara a seguridad si ve a alguien sospechoso.

### 5. Logging (El Chivato)
```python
HoneypotLogger.log_connection(...)
```
Registramos todo lo que pasó. Fíjate que usamos `HoneypotLogger`, que es una clase estática (no necesitamos crearla con `()`, la usamos directamente).

### 6. La Respuesta
```python
client_socket.send(response.encode('utf-8'))
```
Un servidor no solo escucha, debe responder. Enviamos texto (HTML) convertido de nuevo a bytes (`encode`).

---

**Resumen del Flujo de una Conexión:**
1.  `main.py` arrancó el servicio.
2.  `BaseService` (padre) abrió el socket y esperó.
3.  Un hacker se conectó.
4.  `BaseService` aceptó la llamada y creó un hilo.
5.  El hilo ejecutó `HTTPService.handle_client`.
6.  `HTTPService` leyó los datos, detectó el ataque y lo guardó en el log.

---

## Capítulo 4: El Menú (`responses/http_endpoints.py`)

Finalmente, ¿qué responde el servidor cuando alguien pide algo?
Para esto usamos un archivo separado. Esto es bueno porque separa la **lógica** (cómo procesar la petición) de los **datos** (qué contenido devolver).

### 1. Clases Estáticas (`@classmethod`)
```python
class HTTPEndpoints:
    @classmethod
    def get_response(cls, path):
```
*   Fíjate que no hay `__init__`. No necesitamos crear "objetos" de este menú.
*   Es como una pizarra en la pared. Solo hay una.
*   Al usar `@classmethod`, podemos llamar a la función directamente: `HTTPEndpoints.get_response(...)`.

### 2. Diccionarios (Mapas)
```python
ENDPOINTS = {
    '/': '...Welcome...',
    '/admin': '...Login...',
}
```
*   Un diccionario en Python es clave-valor. Es la estructura más rápida para búsquedas.
*   En lugar de hacer 20 `if/else` ("si pide admin haz esto, si pide login haz esto otro"), usamos el diccionario.

### 3. Búsqueda Segura (`.get()`)
```python
return cls.ENDPOINTS.get(path, cls.NOT_FOUND)
```
*   Esta línea es elegante.
*   Dice: "Busca `path` en el diccionario. Si lo encuentras, dámelo. Si NO lo encuentras, devuélveme `NOT_FOUND`".
*   Asi manejamos los errores 404 automáticamente sin escribir código complejo.

---

## ¡Felicidades! 🎓
Has completado el recorrido por la arquitectura del Honeypot.
1.  **Main**: Arranca motor.
2.  **Base**: Plantilla de conexión.
3.  **Service**: Lógica HTTP.
4.  **Endpoints**: Contenido visual.
5.  **Logger/Config**: Utilidades.

¡Ya estás listo para modificarlo!
