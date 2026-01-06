# 🔒 Guía: Auditoría de Ciberseguridad en Red Doméstica

**Fecha:** 18 de diciembre de 2025  
**Objetivo:** Cómo realizar una auditoría profesional de tu red doméstica

---

## 📋 Opciones para Auditoría de Red Doméstica

### Opción 1: Hazlo Tú Mismo (DIY) ✅

**Ventajas:**
- Gratis
- Aprendes sobre tu red
- Control total

**Desventajas:**
- Requiere conocimientos técnicos
- Consume tiempo
- Puede que no detectes todo

### Opción 2: Contratar Profesional 💰

**Ventajas:**
- Análisis profesional completo
- Informe detallado
- Recomendaciones expertas

**Desventajas:**
- Costo (300€ - 1500€)
- Necesitas confiar en terceros
- Acceso a tu red

### Opción 3: Herramientas Automatizadas 🤖

**Ventajas:**
- Fácil de usar
- Rápido
- Económico

**Desventajas:**
- Menos detallado que profesional
- Puede generar falsos positivos

---

## 🛠️ Opción 1: Auditoría DIY Paso a Paso

### Fase 1: Inventario de Red

#### 1.1 Escanear Dispositivos en la Red

**Herramientas recomendadas:**

**Fing** (Gratis, fácil)
- Descarga: https://www.fing.com/
- Escanea todos los dispositivos conectados
- Identifica fabricantes
- Detecta puertos abiertos

**Advanced IP Scanner** (Gratis, Windows)
- Descarga: https://www.advanced-ip-scanner.com/
- Escaneo rápido de red local
- Acceso remoto integrado

**Angry IP Scanner** (Gratis, multiplataforma)
- Descarga: https://angryip.org/
- Open source
- Exporta resultados

**Comandos nativos:**
```powershell
# Ver dispositivos conectados
arp -a

# Escanear rango de IPs (requiere nmap)
nmap -sn 192.168.0.0/24
```

#### 1.2 Documentar Dispositivos

Crear lista de:
- Nombre del dispositivo
- Dirección IP
- Dirección MAC
- Fabricante
- Propósito (PC, móvil, IoT, etc.)
- ¿Es tuyo? (detectar intrusos)

---

### Fase 2: Auditoría del Router

#### 2.1 Acceder al Router

1. Abrir navegador
2. Ir a: `192.168.0.1` o `192.168.1.1`
3. Login con credenciales (usuario/contraseña)

**⚠️ Si aún tienes credenciales por defecto (admin/admin), CÁMBIALAS YA**

#### 2.2 Verificaciones Críticas

**✅ Contraseña WiFi:**
- Mínimo 16 caracteres
- WPA3 o WPA2-AES
- Nunca WEP o WPA (obsoletos)

**✅ Firmware actualizado:**
- Buscar actualizaciones en panel del router
- Aplicar última versión disponible

**✅ Firewall habilitado:**
- Verificar que esté activo
- Configurar reglas si es posible

**✅ UPnP deshabilitado:**
- UPnP es conveniente pero inseguro
- Deshabilitar si no lo necesitas

**✅ Administración remota deshabilitada:**
- No permitir acceso desde Internet
- Solo gestión desde red local

**✅ WPS deshabilitado:**
- WPS es vulnerable a ataques
- Desactivar completamente

**✅ DNS seguro:**
- Cambiar a Cloudflare (1.1.1.1, 1.0.0.1)
- O Google (8.8.8.8, 8.8.4.4)
- Evitar DNS del ISP

#### 2.3 Revisar Logs del Router

- Buscar intentos de acceso fallidos
- Conexiones sospechosas
- Dispositivos desconocidos

---

### Fase 3: Escaneo de Vulnerabilidades

#### 3.1 Escanear Puertos Abiertos

**Nmap (Avanzado)**
```bash
# Instalar nmap
# Escanear tu propia IP pública
nmap -sV -p- TU_IP_PUBLICA

# Escanear dispositivos locales
nmap -sV 192.168.0.1-254
```

**ShieldsUP!** (Online, fácil)
- Web: https://www.grc.com/shieldsup
- Escanea tu IP pública
- Detecta puertos expuestos
- Gratis

#### 3.2 Verificar Exposición a Internet

**Shodan** (Motor de búsqueda de dispositivos)
- Web: https://www.shodan.io/
- Buscar tu IP pública
- Ver qué información está expuesta
- Cuenta gratis con límites

**Censys** (Alternativa a Shodan)
- Web: https://search.censys.io/
- Similar a Shodan
- Gratis con registro

---

### Fase 4: Análisis de Tráfico de Red

#### 4.1 Wireshark (Avanzado)

**Descarga:** https://www.wireshark.org/

**Qué buscar:**
- Tráfico no cifrado (HTTP en lugar de HTTPS)
- Conexiones a IPs sospechosas
- Picos de tráfico inusuales
- Protocolos desconocidos

**⚠️ Requiere conocimientos técnicos**

#### 4.2 GlassWire (Más fácil)

**Descarga:** https://www.glasswire.com/

**Características:**
- Monitor de tráfico en tiempo real
- Alertas de nuevas conexiones
- Historial de actividad
- Versión gratis disponible

---

### Fase 5: Seguridad de Dispositivos IoT

#### 5.1 Identificar Dispositivos IoT

- Cámaras IP
- Smart TVs
- Asistentes de voz (Alexa, Google Home)
- Termostatos inteligentes
- Bombillas inteligentes
- Enchufes inteligentes

#### 5.2 Hardening de IoT

**✅ Cambiar contraseñas por defecto**
**✅ Actualizar firmware**
**✅ Deshabilitar funciones innecesarias**
**✅ Aislar en VLAN separada** (si tu router lo permite)
**✅ Revisar permisos de apps móviles**

---

### Fase 6: Pruebas de Penetración Básicas

#### 6.1 Probar Fuerza de Contraseña WiFi

**Aircrack-ng** (Solo para tu propia red)
```bash
# SOLO PARA TU PROPIA RED - ES ILEGAL HACERLO EN REDES AJENAS
aircrack-ng -w wordlist.txt capture.cap
```

**⚠️ ADVERTENCIA:** Solo prueba en TU red. Probar en redes ajenas es ILEGAL.

#### 6.2 Verificar Aislamiento de Clientes

- Conectar dos dispositivos a WiFi
- Intentar hacer ping entre ellos
- Si funciona, no hay aislamiento (puede ser problema en redes públicas)

---

## 🤖 Opción 3: Herramientas Automatizadas

### Router Security Scan (Gratis)

**F-Secure Router Checker**
- Web: https://www.f-secure.com/en/home/free-tools/router-checker
- Escaneo automático del router
- Detecta DNS hijacking
- Gratis

### Bitdefender Home Scanner (Gratis)

**Descarga:** https://www.bitdefender.com/solutions/home-scanner.html

**Características:**
- Escanea red doméstica
- Detecta vulnerabilidades
- Identifica dispositivos
- Gratis

### Avast Wi-Fi Inspector (Gratis)

**Incluido en Avast Antivirus**

**Características:**
- Escaneo de red
- Detección de vulnerabilidades
- Alertas de seguridad

---

## 💰 Opción 2: Contratar Profesional

### Cuándo Contratar un Profesional

- Tienes datos muy sensibles
- Red empresarial en casa
- Sospechas de compromiso
- Quieres certificación oficial
- Necesitas cumplir normativas

### Qué Esperar

**Servicios incluidos:**
- Escaneo completo de red
- Pruebas de penetración
- Análisis de vulnerabilidades
- Informe detallado
- Recomendaciones priorizadas
- Plan de remediación

**Costo aproximado:**
- Básico: 300€ - 600€
- Completo: 600€ - 1500€
- Empresarial: 1500€+

### Dónde Encontrar Profesionales

**Plataformas:**
- Upwork (freelancers)
- Fiverr (servicios puntuales)
- LinkedIn (profesionales certificados)

**Certificaciones a buscar:**
- CEH (Certified Ethical Hacker)
- OSCP (Offensive Security Certified Professional)
- CISSP (Certified Information Systems Security Professional)

---

## 📊 Checklist de Auditoría Completa

### Router
- [ ] Contraseña de admin cambiada
- [ ] Firmware actualizado
- [ ] WiFi con WPA3/WPA2-AES
- [ ] Contraseña WiFi fuerte (16+ caracteres)
- [ ] UPnP deshabilitado
- [ ] WPS deshabilitado
- [ ] Administración remota deshabilitada
- [ ] DNS seguro configurado
- [ ] Firewall habilitado
- [ ] Logs revisados

### Red
- [ ] Inventario de dispositivos completo
- [ ] Todos los dispositivos identificados
- [ ] No hay dispositivos desconocidos
- [ ] Escaneo de puertos realizado
- [ ] No hay puertos innecesarios abiertos
- [ ] IP pública verificada en Shodan
- [ ] Tráfico de red analizado

### Dispositivos
- [ ] Todos con antivirus actualizado
- [ ] Sistemas operativos actualizados
- [ ] Contraseñas únicas y fuertes
- [ ] 2FA habilitado donde sea posible
- [ ] Backups configurados

### IoT
- [ ] Contraseñas por defecto cambiadas
- [ ] Firmware actualizado
- [ ] Funciones innecesarias deshabilitadas
- [ ] Permisos de apps revisados

---

## 🎯 Plan de Acción Recomendado

### Para Usuario Básico

1. **Usar Fing** para escanear dispositivos
2. **Acceder al router** y verificar configuración básica
3. **Usar F-Secure Router Checker** online
4. **Cambiar contraseñas** débiles
5. **Actualizar firmware** del router

**Tiempo:** 2-3 horas  
**Costo:** Gratis

### Para Usuario Avanzado

1. Todo lo anterior +
2. **Instalar nmap** y escanear red completa
3. **Usar Wireshark** para analizar tráfico
4. **Verificar en Shodan** exposición pública
5. **Configurar VLAN** para IoT (si es posible)
6. **Implementar Pi-hole** para DNS filtering

**Tiempo:** 1-2 días  
**Costo:** Gratis (o ~50€ para Raspberry Pi si quieres Pi-hole)

### Para Máxima Seguridad

1. Todo lo anterior +
2. **Contratar auditoría profesional**
3. **Implementar IDS/IPS** (como Metatron que ya tienes)
4. **Segmentar red** con VLANs
5. **VPN para acceso remoto**
6. **Monitoreo continuo**

**Tiempo:** 1 semana  
**Costo:** 500€ - 2000€

---

## 🛡️ Tu Situación Actual

Basándome en lo que hemos hecho hoy:

### ✅ Ya Tienes
- Bitdefender activo (antivirus profesional)
- Firewall configurado restrictivamente
- Puertos críticos bloqueados
- Metatron (IDS casero)
- Sistema hardened

### 🔍 Deberías Hacer
1. **Escanear red con Fing** (10 minutos)
2. **Revisar configuración del router** (30 minutos)
3. **Verificar en Shodan** tu IP pública (5 minutos)
4. **Actualizar firmware del router** (15 minutos)

**Esto te daría una auditoría básica pero efectiva.**

---

## 📚 Recursos Adicionales

### Guías Online
- NIST Cybersecurity Framework
- OWASP IoT Security
- CIS Controls

### Comunidades
- r/homelab (Reddit)
- r/netsec (Reddit)
- Foros de seguridad informática

### Cursos Gratis
- Cybrary (cursos de seguridad)
- TryHackMe (práctica de pentesting)
- HackTheBox (retos de seguridad)

---

**Creado:** 18/12/2025 12:16 PM  
**Próxima revisión recomendada:** Cada 3-6 meses
