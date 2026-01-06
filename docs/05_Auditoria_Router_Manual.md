# Guía de Auditoría de Seguridad del Router

**Fecha de actualización**: 2025-12-24  
**Propósito**: Checklist paso a paso para auditar manualmente la seguridad de tu router doméstico  
**Trazabilidad**: Documento parte del repositorio Alucard

---

## ⚠️ Antes de Empezar

> [!IMPORTANT]
> **Requisitos previos**:
> - Acceso físico al router
> - Credenciales de administrador del router
> - Navegador web actualizado
> - 30-45 minutos de tiempo

> [!WARNING]
> **Advertencias**:
> - Algunos cambios pueden interrumpir temporalmente la conexión
> - Documenta la configuración actual antes de hacer cambios
> - Ten a mano el número de soporte de tu ISP por si algo sale mal

---

## 1. Acceso al Router

### 1.1 Identificar la IP del Router

Ejecuta en PowerShell:
```powershell
ipconfig | findstr "Puerta de enlace"
```

**IP común del router**: Generalmente `192.168.1.1` o `192.168.0.1`

### 1.2 Acceder a la Interfaz Web

1. Abre tu navegador
2. Escribe la IP del router en la barra de direcciones
3. Acepta el certificado SSL (si aparece advertencia)

### 1.3 Credenciales

**Credenciales por defecto comunes** (¡DEBEN cambiarse!):
- Usuario: `admin` / Contraseña: `admin`
- Usuario: `admin` / Contraseña: `password`
- Usuario: `admin` / Contraseña: `1234`

**Documentar**:
- [ ] IP del router: _______________
- [ ] Marca/Modelo: _______________
- [ ] Versión de firmware: _______________

---

## 2. Seguridad de Acceso

### 2.1 Contraseña de Administrador

> [!CAUTION]
> **CRÍTICO**: La contraseña por defecto es la vulnerabilidad #1 en routers domésticos

**Checklist**:
- [ ] ¿La contraseña es la que venía por defecto? → **CAMBIAR INMEDIATAMENTE**
- [ ] ¿La contraseña tiene al menos 16 caracteres?
- [ ] ¿Incluye mayúsculas, minúsculas, números y símbolos?
- [ ] ¿Es única (no se usa en otros servicios)?

**Ubicación típica**: `Administración` → `Contraseña` o `System` → `Password`

**Documentar**:
- [ ] Contraseña cambiada: ✅ / ❌
- [ ] Fecha del cambio: _______________

### 2.2 Administración Remota

> [!WARNING]
> La administración remota permite acceder al router desde Internet. **Debe estar DESACTIVADA** a menos que tengas una necesidad específica.

**Checklist**:
- [ ] ¿Está habilitada la administración remota? → **DESACTIVAR**
- [ ] ¿Hay acceso SSH desde Internet? → **DESACTIVAR**
- [ ] ¿Hay acceso Telnet? → **DESACTIVAR** (Telnet es inseguro)

**Ubicación típica**: `Administración` → `Acceso Remoto` o `Remote Management`

**Documentar**:
- [ ] Administración remota: ACTIVA / **DESACTIVADA** ✅
- [ ] SSH remoto: ACTIVO / **DESACTIVADO** ✅
- [ ] Telnet: ACTIVO / **DESACTIVADO** ✅

---

## 3. Seguridad WiFi

### 3.1 Cifrado WiFi

> [!IMPORTANT]
> **WPA3** es el estándar más seguro. Si tu router no lo soporta, usa **WPA2-AES**.

**Checklist**:
- [ ] Tipo de cifrado actual: _______________
- [ ] ¿Es WPA3 o WPA2? → Si es WEP o WPA: **ACTUALIZAR**
- [ ] ¿Usa AES (no TKIP)?

**Ubicación típica**: `WiFi` → `Seguridad` o `Wireless` → `Security`

**Configuración recomendada**:
- **Mejor**: WPA3-Personal
- **Aceptable**: WPA2-Personal (AES)
- **NUNCA**: WEP, WPA, o "Abierto"

**Documentar**:
- [ ] Cifrado WiFi: _______________
- [ ] Actualizado a WPA2/WPA3: ✅ / ❌

### 3.2 Contraseña WiFi

**Checklist**:
- [ ] ¿La contraseña WiFi es diferente a la de administrador?
- [ ] ¿Tiene al menos 20 caracteres?
- [ ] ¿Es aleatoria (no palabras del diccionario)?

**Documentar**:
- [ ] Contraseña WiFi cambiada: ✅ / ❌

### 3.3 SSID (Nombre de Red)

**Checklist**:
- [ ] ¿El SSID revela información personal? (ej: "WiFi_Juan_Piso3") → **CAMBIAR**
- [ ] ¿El SSID revela el modelo del router? (ej: "NETGEAR_5G") → **CAMBIAR**

**Recomendación**: Usa un nombre genérico que no revele información.

**Documentar**:
- [ ] SSID actual: _______________
- [ ] SSID cambiado: ✅ / ❌

### 3.4 WPS (WiFi Protected Setup)

> [!CAUTION]
> **WPS es una vulnerabilidad conocida**. Permite ataques de fuerza bruta en minutos.

**Checklist**:
- [ ] ¿Está habilitado WPS? → **DESACTIVAR**
- [ ] ¿Hay un botón físico WPS en el router? → Desactivar en software

**Ubicación típica**: `WiFi` → `WPS` o `Wireless` → `WPS`

**Documentar**:
- [ ] WPS: ACTIVO / **DESACTIVADO** ✅

### 3.5 Red de Invitados

**Checklist**:
- [ ] ¿Tienes red de invitados configurada?
- [ ] ¿Está aislada de tu red principal?
- [ ] ¿Tiene contraseña diferente?

**Recomendación**: Usa red de invitados para dispositivos IoT y visitantes.

**Documentar**:
- [ ] Red de invitados: ACTIVA / DESACTIVADA
- [ ] Aislamiento activado: ✅ / ❌

---

## 4. Firewall y Seguridad de Red

### 4.1 Firewall del Router

**Checklist**:
- [ ] ¿El firewall está activado? → **DEBE ESTAR ACTIVO**
- [ ] ¿Está en modo "Alto" o "Máximo"?
- [ ] ¿Bloquea pings desde Internet (Stealth Mode)?

**Ubicación típica**: `Firewall` → `Configuración` o `Security` → `Firewall`

**Documentar**:
- [ ] Firewall: **ACTIVO** ✅ / DESACTIVADO
- [ ] Nivel: _______________

### 4.2 Port Forwarding (Redirección de Puertos)

> [!WARNING]
> Cada puerto abierto es una puerta de entrada potencial para atacantes.

**Checklist**:
- [ ] ¿Hay reglas de port forwarding configuradas?
- [ ] ¿Son todas necesarias?
- [ ] ¿Sabes qué servicio usa cada puerto?

**Revisar cada regla**:

| Puerto | Protocolo | IP Interna | Servicio | ¿Necesario? |
|--------|-----------|------------|----------|-------------|
| ______ | TCP/UDP   | __________ | ________ | ✅ / ❌     |
| ______ | TCP/UDP   | __________ | ________ | ✅ / ❌     |

**Acción**: Elimina todas las reglas innecesarias.

**Documentar**:
- [ ] Reglas revisadas: ✅ / ❌
- [ ] Reglas eliminadas: _______________

### 4.3 UPnP (Universal Plug and Play)

> [!CAUTION]
> **UPnP es una vulnerabilidad de seguridad**. Permite que aplicaciones abran puertos automáticamente sin tu conocimiento.

**Checklist**:
- [ ] ¿Está habilitado UPnP? → **DESACTIVAR** (a menos que sea absolutamente necesario)

**Ubicación típica**: `Avanzado` → `UPnP` o `NAT` → `UPnP`

> [!TIP]
> **Detección Avanzada**: Ejecuta `scripts\analyze_network.ps1`. Si ves tráfico Multicast a `239.255.255.250` (SSDP), es muy probable que UPnP siga activo en tu red.

**Documentar**:
- [ ] UPnP: ACTIVO / **DESACTIVADO** ✅

### 4.4 DMZ (Zona Desmilitarizada)

> [!CAUTION]
> **DMZ expone completamente un dispositivo a Internet**. Solo para casos muy específicos.

**Checklist**:
- [ ] ¿Hay un dispositivo en DMZ? → **DESACTIVAR** (a menos que sepas exactamente por qué lo necesitas)

**Documentar**:
- [ ] DMZ: ACTIVA / **DESACTIVADA** ✅

---

## 5. DNS y Configuración de Red

### 5.1 Servidores DNS

**Checklist**:
- [ ] ¿Qué servidores DNS está usando el router?
- [ ] ¿Son de tu ISP o personalizados?

**Opciones seguras**:
- **Cloudflare**: `1.1.1.1` / `1.0.0.1`
- **Google**: `8.8.8.8` / `8.8.4.4`
- **Quad9**: `9.9.9.9` / `149.112.112.112`

**Ubicación típica**: `Internet` → `DNS` o `WAN` → `DNS`

**Documentar**:
- [ ] DNS Primario: _______________
- [ ] DNS Secundario: _______________
- [ ] DNS cambiado: ✅ / ❌

### 5.2 IPv6

**Checklist**:
- [ ] ¿Está habilitado IPv6?
- [ ] ¿Tiene firewall IPv6 activo?
- [ ] ¿Necesitas IPv6?

**Recomendación**: Si no usas IPv6, desactívalo para reducir superficie de ataque.

**Documentar**:
- [ ] IPv6: ACTIVO / DESACTIVADO
- [ ] Firewall IPv6: ACTIVO / DESACTIVADO

---

## 6. Firmware y Actualizaciones

### 6.1 Versión de Firmware

> [!IMPORTANT]
> **Firmware desactualizado = vulnerabilidades conocidas sin parchar**

**Checklist**:
- [ ] Versión actual de firmware: _______________
- [ ] Fecha de la versión: _______________
- [ ] ¿Hay actualizaciones disponibles? → **ACTUALIZAR**

**Ubicación típica**: `Administración` → `Actualización de Firmware` o `System` → `Firmware Upgrade`

**Documentar**:
- [ ] Firmware actualizado: ✅ / ❌
- [ ] Nueva versión: _______________
- [ ] Fecha de actualización: _______________

### 6.2 Actualizaciones Automáticas

**Checklist**:
- [ ] ¿Están habilitadas las actualizaciones automáticas?

**Recomendación**: Activa si está disponible, pero revisa las notas de versión.

**Documentar**:
- [ ] Auto-actualización: ACTIVA / DESACTIVADA

---

## 7. Logs y Monitoreo

### 7.1 Logs del Router

**Checklist**:
- [ ] ¿El router guarda logs?
- [ ] ¿Puedes ver intentos de acceso fallidos?
- [ ] ¿Hay actividad sospechosa?

**Ubicación típica**: `Administración` → `Logs` o `System Log`

**Buscar**:
- Intentos de login fallidos
- Conexiones desde IPs desconocidas
- Cambios de configuración no autorizados

**Documentar**:
- [ ] Logs revisados: ✅ / ❌
- [ ] Actividad sospechosa: SÍ / NO
- [ ] Detalles: _______________

### 7.2 Dispositivos Conectados

**Checklist**:
- [ ] ¿Reconoces todos los dispositivos conectados?
- [ ] ¿Hay dispositivos desconocidos?

**Ubicación típica**: `Estado` → `Dispositivos Conectados` o `Device List`

**Acción**: Anota MAC addresses de dispositivos desconocidos y bloquéalos.

**Documentar**:
- [ ] Total de dispositivos: _______________
- [ ] Dispositivos desconocidos: _______________
- [ ] MACs bloqueadas: _______________

---

## 8. Configuraciones Avanzadas

### 8.1 Filtrado MAC

**Checklist**:
- [ ] ¿Está habilitado el filtrado MAC?
- [ ] ¿Está en modo "whitelist" (solo permitir)?

**Recomendación**: Útil pero no es seguridad absoluta (MACs se pueden falsificar).

**Documentar**:
- [ ] Filtrado MAC: ACTIVO / DESACTIVADO
- [ ] Modo: WHITELIST / BLACKLIST

### 8.2 Aislamiento de Clientes WiFi

**Checklist**:
- [ ] ¿Está habilitado el aislamiento de clientes?

**Recomendación**: Activa en red de invitados, opcional en red principal.

**Documentar**:
- [ ] Aislamiento: ACTIVO / DESACTIVADO

### 8.3 Horario de WiFi

**Checklist**:
- [ ] ¿Puedes programar horarios para WiFi?
- [ ] ¿Desactivas WiFi cuando no lo usas (ej: de noche)?

**Documentar**:
- [ ] Horario configurado: ✅ / ❌

---

## 9. Backup de Configuración

> [!TIP]
> **Siempre guarda un backup** antes y después de hacer cambios importantes.

**Checklist**:
- [ ] ¿Puedes exportar la configuración del router?
- [ ] ¿Has guardado un backup?

**Ubicación típica**: `Administración` → `Backup/Restore` o `System` → `Backup Settings`

**Documentar**:
- [ ] Backup guardado: ✅ / ❌
- [ ] Ubicación: `c:\test\Alucard\logs\network\router_backup_YYYY-MM-DD.cfg`

---

## 10. Resumen de Auditoría

### Puntuación de Seguridad

Cuenta cuántos ✅ tienes en las secciones críticas:

| Categoría | Puntos | Máximo |
|-----------|--------|--------|
| Contraseñas (2.1, 3.2) | __ / 2 | 2 |
| Acceso Remoto (2.2) | __ / 3 | 3 |
| WiFi (3.1, 3.4) | __ / 2 | 2 |
| Firewall (4.1) | __ / 1 | 1 |
| UPnP/DMZ (4.3, 4.4) | __ / 2 | 2 |
| Firmware (6.1) | __ / 1 | 1 |
| **TOTAL** | **__ / 11** | **11** |

**Interpretación**:
- **11/11**: 🟢 Excelente seguridad
- **8-10/11**: 🟡 Buena seguridad, mejoras menores
- **5-7/11**: 🟠 Seguridad moderada, mejoras necesarias
- **0-4/11**: 🔴 Seguridad deficiente, acción inmediata requerida

### Hallazgos Críticos

Documenta aquí los problemas más graves encontrados:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Acciones Tomadas

Documenta los cambios realizados:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

### Acciones Pendientes

Documenta lo que falta por hacer:

1. _______________________________________________
2. _______________________________________________
3. _______________________________________________

---

## 11. Próxima Auditoría

> [!NOTE]
> **Frecuencia recomendada**: Cada 3-6 meses o después de:
> - Actualización de firmware
> - Cambio de ISP
> - Incidente de seguridad
> - Cambio de contraseñas

**Próxima auditoría programada**: _______________

---

## 12. Verificación Cruzada (Navegadores)

A veces, lo que parece un router comprometido (redirecciones, anuncios raros) es en realidad malware en tu navegador.

**Acción Recomendada**:
- Ejecuta `scripts\analyze_browsers.ps1` para buscar extensiones maliciosas que manipulen tu tráfico.
- Revisa si tus DNS en el router coinciden con los detectados en tu PC (`ipconfig /all`).

---

## Recursos Adicionales

- **Buscar vulnerabilidades del modelo**: [https://www.cvedetails.com/](https://www.cvedetails.com/)
- **Comprobar si tu router está comprometido**: [https://www.shodan.io/](https://www.shodan.io/)
- **Guías por fabricante**:
  - TP-Link: [https://www.tp-link.com/support/](https://www.tp-link.com/support/)
  - Netgear: [https://www.netgear.com/support/](https://www.netgear.com/support/)
  - Asus: [https://www.asus.com/support/](https://www.asus.com/support/)

---

**Auditoría completada por**: _______________  
**Fecha**: _______________  
**Firma**: _______________

---

*Documento parte del repositorio Alucard - Sistema de Seguridad Defensiva*  
*Última actualización: 2025-12-19*
