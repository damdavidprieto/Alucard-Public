# 🍯 Educational Honeypot

**⚠️ DISCLAIMER: Este honeypot es SOLO para fines educativos**

---

## 📋 Tabla de Contenidos

- [Advertencias Importantes](#-advertencias-importantes)
- [¿Qué es esto?](#-qué-es-esto)
- [Arquitectura](#-arquitectura)
- [Características](#-características)
- [Instalación](#-instalación)
- [Uso](#-uso)
- [Perfiles Disponibles](#-perfiles-disponibles)
- [Estructura del Proyecto](#-estructura-del-proyecto)
- [Limitaciones](#-limitaciones)
- [Licencia](#-licencia)

---

## ⚠️ Advertencias Importantes

### NO Usar Para

- ❌ Protección de sistemas en producción
- ❌ Defensa de redes corporativas
- ❌ Recopilación de inteligencia de amenazas real
- ❌ Cualquier uso sin aislamiento adecuado

### SÍ Usar Para

- ✅ Aprendizaje de conceptos de honeypots
- ✅ Experimentación en entornos aislados (VMs)
- ✅ Comprensión de técnicas de detección
- ✅ Práctica de desarrollo en Python

### Responsabilidad

El autor **NO se hace responsable** de:
- Daños causados por uso inadecuado
- Compromisos de seguridad derivados del uso
- Pérdida de datos o servicios
- Violaciones de privacidad o legalidad

---

## 🎯 ¿Qué es esto?

Este es un **honeypot educativo** desarrollado para aprender sobre:

1. **Detección de ataques**: Cómo identificar herramientas de hacking
2. **Simulación de servicios**: HTTP, SSH, FTP
3. **Logging y análisis**: Registro de intentos de intrusión
4. **Arquitectura de seguridad**: Diseño de sistemas defensivos

### Características Principales

- 🌐 **Servidor HTTP** con múltiples perfiles (WordPress, API, IoT, etc.)
- 🔐 **Servidor SSH** falso con autenticación simulada
- 📊 **Logging detallado** en formato JSON
- 🌍 **Geolocalización** de IPs atacantes
- 🎭 **Perfiles dinámicos** para simular diferentes tipos de servidores
- 🔍 **Detección de scanners** (SQLMap, Nmap, Nikto, etc.)

---

## 🏗️ Arquitectura

```
┌─────────────────────────────────────────────────────────────┐
│                     ATACANTE                                │
│                  (Kali Linux / Tools)                       │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       │ HTTP/SSH Requests
                       │
                       ▼
┌─────────────────────────────────────────────────────────────┐
│                  DOCKER CONTAINER                           │
│  ┌───────────────────────────────────────────────────────┐  │
│  │  main.py (Orquestador)                                │  │
│  │  ├─ HTTPService (Puerto 8080)                         │  │
│  │  └─ SSHService (Puerto 2222)                          │  │
│  └───────────────────────────────────────────────────────┘  │
│                       │                                     │
│         ┌─────────────┼─────────────┐                       │
│         │             │             │                       │
│         ▼             ▼             ▼                       │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐                  │
│  │ Endpoint │  │ Scanner  │  │ Attack   │                  │
│  │ Manager  │  │ Detector │  │ Detector │                  │
│  └──────────┘  └──────────┘  └──────────┘                  │
│         │             │             │                       │
│         └─────────────┴─────────────┘                       │
│                       │                                     │
│                       ▼                                     │
│              ┌─────────────────┐                            │
│              │  Logger (JSON)  │                            │
│              └─────────────────┘                            │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
              ┌───────────────┐
              │ honeypot.log  │
              │  (Persistente)│
              └───────────────┘
```

---

## ✨ Características

### 1. Perfiles Dinámicos

El honeypot puede simular diferentes tipos de servidores:

- **Generic**: Servidor Apache básico
- **WordPress**: Blog WordPress con plugins
- **API**: API REST con endpoints
- **Database**: Herramientas de administración de BBDD
- **IoT**: Dispositivos IoT (routers, cámaras)
- **DevOps**: Fugas de configuración (.git, .env, etc.)

### 2. Detección de Herramientas

Detecta automáticamente:
- SQLMap (SQL Injection)
- Nmap (Port Scanner)
- Nikto (Web Scanner)
- Gobuster/Dirbuster (Directory Brute Force)
- WPScan (WordPress Scanner)
- Burp Suite
- Metasploit
- Y más...

### 3. Respuestas Trampa

Devuelve respuestas falsas para hacer perder tiempo al atacante:
- Errores SQL falsos para SQLMap
- Respuestas WAF para scanners
- Archivos de configuración falsos
- Endpoints API ficticios

---

## 🚀 Instalación

### Requisitos

- Docker
- Python 3.8+ (para desarrollo)
- VirtualBox o VMware (para aislamiento)

### Opción 1: Docker (Recomendado)

```bash
# 1. Clonar repositorio
git clone https://github.com/damdavidprieto/Alucard-Public.git
cd Alucard-Public/honeypot

# 2. Construir imagen
docker build -t educational-honeypot .

# 3. Ejecutar
docker run -d \
  -p 8080:8080 \
  -p 2222:2222 \
  -v $(pwd)/honeypot.log:/app/honeypot.log \
  --name my-honeypot \
  educational-honeypot
```

### Opción 2: Python Local (Solo para desarrollo)

```bash
# 1. Instalar dependencias
pip install -r requirements.txt

# 2. Ejecutar
python main.py
```

**⚠️ IMPORTANTE**: Ejecutar SOLO en VM aislada, nunca en sistema principal.

---

## 📖 Uso

### Configuración Básica

Editar `config.py`:

```python
# Cambiar puertos
HTTP_PORT = 8080
SSH_PORT = 2222

# Cambiar perfil activo
HONEYPOT_PROFILE = 'wordpress'  # o 'all', 'api', 'iot', etc.
```

### Cambiar Perfil en Tiempo de Ejecución

```bash
# Perfil WordPress
HONEYPOT_PROFILE=wordpress python main.py

# Perfil IoT
HONEYPOT_PROFILE=iot python main.py

# Todos los perfiles
HONEYPOT_PROFILE=all python main.py
```

### Ver Logs

```bash
# En tiempo real
tail -f honeypot.log

# Analizar logs (requiere jq)
cat honeypot.log | jq '.'
```

---

## 🎭 Perfiles Disponibles

### `generic` - Servidor Apache Básico
Simula un servidor web genérico con:
- Página de inicio
- robots.txt
- favicon.ico
- Errores 404 personalizados

### `wordpress` - Blog WordPress
Simula un sitio WordPress con:
- `/wp-admin` - Panel de administración
- `/wp-login.php` - Login
- `/wp-content/plugins/` - Plugins
- `/xmlrpc.php` - XML-RPC

### `api` - API REST
Simula una API con:
- `/api/v1/users` - Usuarios
- `/api/v1/auth` - Autenticación
- `/api/v1/data` - Datos
- Respuestas JSON

### `database` - Herramientas BBDD
Simula:
- phpMyAdmin
- Adminer
- MongoDB Express

### `iot` - Dispositivos IoT
Simula:
- Routers TP-Link
- Cámaras Tapo C200
- Interfaces de gestión

### `devops` - Fugas de Configuración
Simula fugas comunes:
- `.git/config`
- `.env`
- `docker-compose.yml`
- `.aws/credentials`

---

## 📁 Estructura del Proyecto

```
honeypot/
├── main.py                 # Punto de entrada
├── config.py               # Configuración
├── Dockerfile              # Imagen Docker
├── requirements.txt        # Dependencias Python
├── profiles.json           # Configuración de perfiles
│
├── core/                   # Núcleo del sistema
│   ├── logger.py           # Sistema de logging
│   ├── geolocation.py      # Geolocalización de IPs
│   └── utils.py            # Utilidades
│
├── services/               # Servicios (HTTP, SSH, FTP)
│   ├── base.py             # Clase base
│   ├── http_service.py     # Servidor HTTP
│   └── ssh_service.py      # Servidor SSH
│
├── responses/              # Respuestas HTTP
│   ├── endpoint_manager.py # Gestor de endpoints
│   ├── detectors/          # Detectores de ataques
│   │   └── scanner_detector.py
│   └── profiles/           # Perfiles de honeypot
│       ├── generic.py
│       ├── wordpress.py
│       ├── api.py
│       └── ...
│
└── detection/              # Detección de ataques
    └── http_attacks.py     # Detección de ataques HTTP
```

---

## ⚠️ Limitaciones

Este honeypot es **educativo** y tiene limitaciones importantes:

### Técnicas

1. **Detección por User-Agent**: Fácil de evadir cambiando el User-Agent
2. **Sin análisis de comportamiento**: No detecta patrones complejos
3. **Respuestas estáticas**: Las trampas son predecibles
4. **Sin machine learning**: No aprende de ataques

### Operacionales

1. **No es production-ready**: Falta hardening
2. **Sin escalabilidad**: Diseñado para una instancia
3. **Logging básico**: No integra con SIEM
4. **Sin correlación**: No relaciona eventos

### De Seguridad

1. **Puede tener vulnerabilidades**: Es código educativo
2. **No proporciona protección real**: Es un señuelo
3. **Requiere aislamiento**: Debe estar en VM

---

## 🛡️ Requisitos de Seguridad

Si decides experimentar con este honeypot:

### Obligatorio

1. ✅ **VM Aislada**: Usa VirtualBox/VMware
2. ✅ **Red NAT**: No usar modo bridged
3. ✅ **Snapshots**: Antes de cada experimento
4. ✅ **Monitoreo**: Del sistema host

### Recomendado

1. 📊 **Logs externos**: Enviar a sistema separado
2. 🔒 **Firewall**: Limitar conexiones salientes
3. 📸 **Capturas de red**: Para análisis posterior
4. 🔄 **Rotación**: Destruir y recrear regularmente

---

## 📚 Recursos de Aprendizaje

### Documentación Relacionada

- [ARCHITECTURE.md](../docs/ARCHITECTURE.md) - Arquitectura de 3 capas
- [ATTACK_SCENARIOS.md](../docs/ATTACK_SCENARIOS.md) - Escenarios de ataque
- [MANUAL_TECNICO.md](../docs/MANUAL_TECNICO.md) - Guía técnica Python

### Referencias

Este proyecto fue inspirado por:
- [T-Pot](https://github.com/telekom-security/tpotce) - Plataforma de honeypots
- [Wazuh](https://wazuh.com/) - SIEM y detección de intrusiones
- Proyectos de [U7Dani](https://github.com/U7Dani) - Laboratorios Blue Team

---

## 📄 Licencia

Este proyecto está bajo Licencia MIT. Ver [LICENSE](../LICENSE) para más detalles.

**Importante**: 
- Puedes usar, modificar y distribuir el código
- Debes mantener el aviso de copyright
- Debes citar las fuentes originales

---

## 🤝 Contribuciones

Este es un proyecto educativo. Las contribuciones son bienvenidas si:
- Mejoran el valor educativo
- Añaden documentación
- Corrigen bugs
- Añaden nuevos perfiles educativos

**No se aceptan**:
- Código ofensivo
- Herramientas de ataque
- Exploits reales

---

## 💬 Contacto

- **GitHub**: [@damdavidprieto](https://github.com/damdavidprieto)
- **Proyecto**: Alucard - Ecosistema de Seguridad Defensiva
- **Issues**: Para reportar problemas o sugerencias

---

## 🙏 Agradecimientos

Desarrollado con asistencia de **Antigravity (Google Gemini)**.

Agradecimientos especiales a la comunidad de ciberseguridad por compartir conocimiento y hacer el aprendizaje accesible.

---

**⚡ Última actualización**: 2025-12-21  
**📈 Versión**: 1.0.0-educational  
**🎯 Estado**: Educativo - No usar en producción

---

*"El único error real es aquel del que no aprendemos nada."* - Henry Ford

🍯 **Educational Honeypot** - Aprendiendo seguridad defensiva
