"""
═══════════════════════════════════════════════════════════════════════════
PERFIL DEVOPS - Fugas de Configuración
═══════════════════════════════════════════════════════════════════════════
Simula archivos de configuración expuestos accidentalmente.
Atrae ataques que buscan .env, docker-compose.yml, etc.
═══════════════════════════════════════════════════════════════════════════
"""

DEVOPS_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /.env (Archivo de Variables de Entorno)                           │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Archivo .env expuesto (error común de desarrolladores)          │
    # │ TRAMPA: Contiene credenciales falsas de base de datos                   │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/.env': 'HTTP/1.1 200 OK\r\nContent-Type: text/plain\r\n\r\nDB_HOST=localhost\nDB_USER=root\nDB_PASS=secret123',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /docker-compose.yml (Configuración Docker)                        │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Archivo docker-compose expuesto                                 │
    # │ TRAMPA: Revela "arquitectura" falsa del sistema                         │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/docker-compose.yml': 'HTTP/1.1 200 OK\r\nContent-Type: text/yaml\r\n\r\nversion: "3"\nservices:\n  db:\n    image: mysql',
}
