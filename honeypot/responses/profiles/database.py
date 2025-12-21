"""
═══════════════════════════════════════════════════════════════════════════
PERFIL DATABASE - Herramientas de BBDD Expuestas
═══════════════════════════════════════════════════════════════════════════
Simula herramientas de administración de bases de datos expuestas.
Atrae ataques dirigidos a phpMyAdmin, pgAdmin, etc.
═══════════════════════════════════════════════════════════════════════════
"""

DATABASE_ENDPOINTS = {
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /phpmyadmin (phpMyAdmin)                                          │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Herramienta de administración de MySQL                          │
    # │ TRAMPA: Simula phpMyAdmin expuesto (muy buscado por atacantes)          │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/phpmyadmin': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>phpMyAdmin</h1><p>Welcome to phpMyAdmin</p></body></html>',
    
    # ┌─────────────────────────────────────────────────────────────────────────┐
    # │ RUTA: /pgadmin (pgAdmin)                                                │
    # ├─────────────────────────────────────────────────────────────────────────┤
    # │ QUÉ ES: Herramienta de administración de PostgreSQL                     │
    # │ TRAMPA: Simula pgAdmin expuesto                                         │
    # └─────────────────────────────────────────────────────────────────────────┘
    '/pgadmin': 'HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<html><body><h1>pgAdmin</h1><p>PostgreSQL Administration</p></body></html>',
}
