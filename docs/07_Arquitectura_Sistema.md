# 🏗️ Arquitectura del Sistema - 3 Capas

## Diagrama General

```
┌───────────────────────────────────────────────────────────────────────┐
│                                                                       │
│  CAPA 1: WINDOWS HOST (Tu Sistema Principal)                        │
│  ═══════════════════════════════════════════════════════════════     │
│                                                                       │
│  📁 c:\test\                                                          │
│     ├── honeypot.py          (código fuente)                         │
│     ├── Dockerfile            (configuración contenedor)             │
│     ├── honeypot.log          (📝 LOGS PERSISTENTES)                 │
│     └── analyze_logs.py       (análisis de datos)                    │
│                                                                       │
│  🐳 Docker Desktop                                                    │
│     └── WSL2 (Windows Subsystem for Linux)                           │
│         └── Linux Kernel                                             │
│                                                                       │
│  💻 VirtualBox                                                        │
│     └── Hypervisor                                                   │
│                                                                       │
└───────────────────────────────────────────────────────────────────────┘
                                    │
                    ┌───────────────┴───────────────┐
                    │                               │
                    ▼                               ▼
┌─────────────────────────────────┐   ┌─────────────────────────────────┐
│                                 │   │                                 │
│  CAPA 2: DOCKER CONTAINER       │   │  CAPA 3: KALI LINUX VM         │
│  ═══════════════════════════     │   │  ═══════════════════════════   │
│                                 │   │                                 │
│  Sistema Operativo:             │   │  Sistema Operativo:             │
│  🐧 Linux (Debian Slim)         │   │  🐉 Kali Linux 2024            │
│                                 │   │     (Debian-based)              │
│  Servicios del Honeypot:        │   │                                 │
│  ┌─────────────────────────┐   │   │  Herramientas de Ataque:        │
│  │ 🌐 HTTP (Puerto 8080)   │   │   │  ┌─────────────────────────┐   │
│  │  • /admin               │   │   │  │ 🔍 nmap (escaneo)       │   │
│  │  • /login               │   │   │  │ 💥 metasploit           │   │
│  │  • /api/*               │   │   │  │ 🕷️ sqlmap               │   │
│  │  • /wp-admin            │   │   │  │ 🔨 hydra (fuerza bruta) │   │
│  └─────────────────────────┘   │   │  │ 📡 wireshark            │   │
│                                 │   │  │ 🎯 burp suite           │   │
│  ┌─────────────────────────┐   │   │  │ 🔓 nikto                │   │
│  │ 🔐 SSH (Puerto 2222)    │   │   │  └─────────────────────────┘   │
│  │  • Fake shell           │   │   │                                 │
│  │  • Credential logging   │   │   │  Herramientas de Análisis:      │
│  └─────────────────────────┘   │   │  ┌─────────────────────────┐   │
│                                 │   │  │ 📊 tcpdump              │   │
│  ┌─────────────────────────┐   │   │  │ 🔬 netcat               │   │
│  │ 📂 FTP (Puerto 2121)    │   │   │  │ 🐍 Python scripts       │   │
│  │  • Fake directories     │   │   │  └─────────────────────────┘   │
│  │  • Login tracking       │   │   │                                 │
│  └─────────────────────────┘   │   │  Red:                           │
│                                 │   │  • IP: 10.0.2.15 (NAT)         │
│  Características:               │   │  • Gateway: 10.0.2.2 (Host)    │
│  ✅ Logging JSON                │   │  • Internet: ✅                 │
│  ✅ Geolocalización             │   │  • Acceso a Honeypot: ✅        │
│  ✅ Detección de patrones       │   │                                 │
│  ✅ Fingerprinting              │   │  Propósito:                     │
│  ✅ Alertas en tiempo real      │   │  • Ejecutar ataques controlados │
│                                 │   │  • Probar honeypot              │
│  Red:                           │   │  • Analizar tráfico             │
│  • Puertos expuestos al host    │   │  • Aprender pentesting          │
│  • Volumen montado para logs    │   │                                 │
│                                 │   │                                 │
└─────────────────────────────────┘   └─────────────────────────────────┘
```

## Flujo de Datos

```
┌─────────────┐
│ Kali Linux  │
│ (Atacante)  │
└──────┬──────┘
       │
       │ 1. Ataque (nmap, curl, ssh, etc.)
       │
       ▼
┌─────────────────────┐
│ Windows Host        │
│ (10.0.2.2)          │
│                     │
│ Puerto 8080 ───────┼──┐
│ Puerto 2222 ───────┼──┤ 2. Reenvío de puertos
│ Puerto 2121 ───────┼──┘    Docker expone puertos
└─────────────────────┘
       │
       │ 3. Tráfico llega al contenedor
       │
       ▼
┌─────────────────────┐
│ Docker Container    │
│                     │
│ honeypot.py         │
│  ├─ Recibe petición │
│  ├─ Procesa         │
│  ├─ Geolocaliza IP  │
│  ├─ Detecta patrón  │
│  └─ Registra log    │
└─────────────────────┘
       │
       │ 4. Escribe log
       │
       ▼
┌─────────────────────┐
│ Volumen montado     │
│ c:\test\honeypot.log│
│                     │
│ ✅ Persistente      │
│ ✅ Accesible desde  │
│    Windows          │
└─────────────────────┘
       │
       │ 5. Análisis
       │
       ▼
┌─────────────────────┐
│ analyze_logs.py     │
│  ├─ Lee logs        │
│  ├─ Genera stats    │
│  ├─ Identifica IPs  │
│  └─ Crea reportes   │
└─────────────────────┘
```

## Comparación de Sistemas Operativos

| Aspecto | Windows Host | Docker (Linux) | Kali VM (Linux) |
|---------|--------------|----------------|-----------------|
| **SO Base** | Windows 10/11 | Debian Slim | Kali Linux (Debian) |
| **Kernel** | NT Kernel | Linux 5.x+ | Linux 6.x+ |
| **Propósito** | Gestión y almacenamiento | Ejecutar honeypot | Pentesting |
| **Aislamiento** | Host principal | Contenedor aislado | VM completamente aislada |
| **Recursos** | Todos disponibles | Limitados por Docker | Limitados (4GB RAM, 2 CPU) |
| **Red** | Física | Virtual (bridge) | Virtual (NAT/Host-only) |
| **Persistencia** | Permanente | Efímero (excepto volúmenes) | Permanente (con snapshots) |
| **Seguridad** | Exposición media | Alta (aislado) | Alta (aislado) |

## Ventajas de Cada Capa

### Windows Host (Capa 1)
✅ **Ventajas**:
- Interfaz familiar
- Fácil gestión de archivos
- Logs accesibles directamente
- Herramientas de análisis Windows

❌ **Desventajas**:
- No es el entorno nativo para honeypots
- Menos herramientas de seguridad

### Docker Container (Capa 2)
✅ **Ventajas**:
- Ligero y rápido
- Fácil de destruir y recrear
- Aislamiento del sistema host
- Portable (funciona en cualquier OS)
- Logs persistentes con volúmenes

❌ **Desventajas**:
- Comparte kernel con host (menos aislamiento que VM)
- Requiere reconstruir imagen para cambios de código

### Kali Linux VM (Capa 3)
✅ **Ventajas**:
- Herramientas de pentesting pre-instaladas
- Completamente aislada
- Snapshots para restaurar
- Entorno Linux completo
- Ideal para aprendizaje

❌ **Desventajas**:
- Consume más recursos que Docker
- Más lenta que contenedor
- Requiere más configuración inicial

## Escenarios de Uso por Capa

### Capa 1 (Windows)
```powershell
# Gestionar contenedor
docker build -t simple-honeypot .
docker run -d -p 8080:8080 --name my-honeypot ...

# Analizar logs
Get-Content honeypot.log
python analyze_logs.py --summary

# Visualizar datos
# Abrir dashboard.html en navegador
```

### Capa 2 (Docker)
```bash
# Dentro del contenedor (si necesitas debuggear)
docker exec -it my-honeypot /bin/bash

# Ver procesos
ps aux

# Ver logs internos
cat /app/honeypot.log
```

### Capa 3 (Kali)
```bash
# Escanear honeypot
nmap -sV -p 8080,2222,2121 10.0.2.2

# Atacar web
nikto -h http://10.0.2.2:8080
sqlmap -u "http://10.0.2.2:8080/login"

# Fuerza bruta SSH
hydra -l admin -P wordlist.txt ssh://10.0.2.2:2222

# Capturar tráfico
sudo tcpdump -i eth0 host 10.0.2.2
```

## Comunicación Entre Capas

### Windows ↔ Docker
- **Puertos**: Docker expone puertos al host
- **Volúmenes**: Archivos compartidos (logs)
- **Red**: Bridge network

### Windows ↔ Kali VM
- **Red NAT**: Kali accede a Windows vía 10.0.2.2
- **Carpetas compartidas**: Opcional (VirtualBox Guest Additions)
- **Clipboard**: Bidireccional (si está habilitado)

### Kali VM ↔ Docker
- **Indirecto**: Kali → Windows → Docker
- **Tráfico**: Pasa por el host Windows
- **Puertos**: Kali ataca 10.0.2.2:8080 → Windows → Docker

## Seguridad de la Arquitectura

```
Nivel de Exposición:
┌─────────────────────────────────────┐
│ Internet                            │ ← Más expuesto
│  ↓ (si expones puertos)             │
│ Windows Host                        │
│  ↓ (puertos internos)               │
│ Docker Container (Honeypot)         │ ← Aislado
│                                     │
│ Kali VM                             │ ← Completamente aislado
└─────────────────────────────────────┘
```

### Recomendaciones de Seguridad

1. **NO expongas el honeypot a Internet** sin medidas adicionales
2. **Usa NAT** para Kali (no bridged en red pública)
3. **Mantén logs fuera del contenedor** (ya implementado ✅)
4. **Haz snapshots** de Kali antes de ejecutar malware
5. **Monitorea recursos** del host

## Próximos Pasos

1. ✅ Arquitectura documentada
2. ✅ Guía de Kali creada
3. ⏳ Decidir nivel de sofisticación del honeypot
4. ⏳ Implementar mejoras al honeypot
5. ⏳ Configurar Kali VM
6. ⏳ Ejecutar escenarios de ataque
7. ⏳ Analizar resultados

---

**¿Listo para mejorar el honeypot?** 🚀
