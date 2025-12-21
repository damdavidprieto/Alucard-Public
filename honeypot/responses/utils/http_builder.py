"""
═══════════════════════════════════════════════════════════════════════════
HTTP RESPONSE BUILDER - Constructor de Respuestas HTTP Realistas
═══════════════════════════════════════════════════════════════════════════
Construye respuestas HTTP completas con headers realistas que imitan
servidores web reales (Apache, Nginx, etc.).

MEJORA CRÍTICA #1: Headers HTTP Completos
- Añade Server, Date, ETag, X-Powered-By, Cache-Control
- Calcula Content-Length correcto
- Genera ETags únicos por contenido
═══════════════════════════════════════════════════════════════════════════
"""

import datetime
import hashlib


class HTTPResponseBuilder:
    """
    ┌─────────────────────────────────────────────────────────────────────────┐
    │ CONSTRUCTOR DE RESPUESTAS HTTP REALISTAS                                │
    ├─────────────────────────────────────────────────────────────────────────┤
    │ QUÉ HACE: Construye respuestas HTTP con headers completos               │
    │                                                                          │
    │ HEADERS QUE AGREGA:                                                      │
    │   - Server: Apache/2.4.41 (Ubuntu)                                      │
    │   - Date: Timestamp actual en formato RFC 7231                          │
    │   - Content-Type: Según el tipo de contenido                            │
    │   - Content-Length: Tamaño exacto del body                              │
    │   - ETag: Hash MD5 del contenido (para caching)                         │
    │   - X-Powered-By: PHP/7.4.3 (fingerprint falso)                         │
    │   - Connection: keep-alive                                              │
    │   - Cache-Control: max-age=3600                                         │
    └─────────────────────────────────────────────────────────────────────────┘
    """
    
    # Configuración del servidor (puede parametrizarse)
    SERVER_NAME = "Apache/2.4.41 (Ubuntu)"
    PHP_VERSION = "PHP/7.4.3"
    DEFAULT_CACHE_AGE = 3600  # 1 hora
    
    @classmethod
    def build_response(cls, status_code: str, content_type: str, body: str, 
                      extra_headers: list = None, cache_age: int = None) -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ CONSTRUIR RESPUESTA HTTP COMPLETA                                   │
        ├─────────────────────────────────────────────────────────────────────┤
        │ PARÁMETROS:                                                          │
        │   status_code: "200 OK", "404 Not Found", etc.                      │
        │   content_type: "text/html", "application/json", etc.               │
        │   body: Contenido de la respuesta                                   │
        │   extra_headers: Lista de headers adicionales (opcional)            │
        │   cache_age: Segundos de cache (opcional, default 3600)             │
        │                                                                      │
        │ RETORNA: String con respuesta HTTP completa                         │
        └─────────────────────────────────────────────────────────────────────┘
        """
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ PASO 1: Generar timestamp actual (RFC 7231 format)              │
        # ├─────────────────────────────────────────────────────────────────┤
        # │ Formato: "Thu, 13 Dec 2025 07:58:21 GMT"                        │
        # └─────────────────────────────────────────────────────────────────┘
        timestamp = datetime.datetime.utcnow().strftime("%a, %d %b %Y %H:%M:%S GMT")
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ PASO 2: Generar ETag (hash MD5 del contenido)                   │
        # ├─────────────────────────────────────────────────────────────────┤
        # │ ETag permite caching en navegadores                             │
        # │ Ejemplo: "a1b2c3d4e5f6g7h8"                                     │
        # └─────────────────────────────────────────────────────────────────┘
        etag = hashlib.md5(body.encode('utf-8')).hexdigest()[:16]
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ PASO 3: Calcular Content-Length exacto                          │
        # ├─────────────────────────────────────────────────────────────────┤
        # │ Importante: Usar bytes, no caracteres (UTF-8)                   │
        # └─────────────────────────────────────────────────────────────────┘
        content_length = len(body.encode('utf-8'))
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ PASO 4: Construir headers base                                  │
        # └─────────────────────────────────────────────────────────────────┘
        headers = [
            f"HTTP/1.1 {status_code}",
            f"Server: {cls.SERVER_NAME}",
            f"Date: {timestamp}",
            f"Content-Type: {content_type}",
            f"Content-Length: {content_length}",
            f'ETag: "{etag}"',
            f"X-Powered-By: {cls.PHP_VERSION}",
            "Connection: keep-alive",
            f"Cache-Control: max-age={cache_age or cls.DEFAULT_CACHE_AGE}",
        ]
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ PASO 5: Agregar headers adicionales (si los hay)                │
        # └─────────────────────────────────────────────────────────────────┘
        if extra_headers:
            headers.extend(extra_headers)
        
        # ┌─────────────────────────────────────────────────────────────────┐
        # │ PASO 6: Ensamblar respuesta completa                            │
        # ├─────────────────────────────────────────────────────────────────┤
        # │ Formato HTTP: Headers + \r\n\r\n + Body                         │
        # └─────────────────────────────────────────────────────────────────┘
        response = "\r\n".join(headers) + "\r\n\r\n" + body
        
        return response
    
    @classmethod
    def build_html(cls, title: str, body_html: str, status_code: str = "200 OK") -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ ATAJO: Construir respuesta HTML                                     │
        ├─────────────────────────────────────────────────────────────────────┤
        │ Envuelve el HTML en estructura completa y añade headers             │
        └─────────────────────────────────────────────────────────────────────┘
        """
        html = f"""<html>
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
</head>
<body>
{body_html}
</body>
</html>"""
        
        return cls.build_response(status_code, "text/html; charset=UTF-8", html)
    
    @classmethod
    def build_json(cls, data: dict, status_code: str = "200 OK") -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ ATAJO: Construir respuesta JSON                                     │
        └─────────────────────────────────────────────────────────────────────┘
        """
        import json
        json_body = json.dumps(data, indent=2)
        return cls.build_response(status_code, "application/json", json_body)
    
    @classmethod
    def build_text(cls, text: str, status_code: str = "200 OK") -> str:
        """
        ┌─────────────────────────────────────────────────────────────────────┐
        │ ATAJO: Construir respuesta de texto plano                           │
        └─────────────────────────────────────────────────────────────────────┘
        """
        return cls.build_response(status_code, "text/plain; charset=UTF-8", text)
