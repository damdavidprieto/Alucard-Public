# Auditoría de Seguridad de Red - Documentación

**Fecha de creación**: 2025-12-19  
**Propósito**: Sistema de auditoría de seguridad de red defensiva integrado con Alucard  
**Repositorio**: Alucard (GitHub)

---

## Descripción General

Este sistema proporciona herramientas para auditar la seguridad de tu red doméstica y router de forma **defensiva y pasiva**, sin realizar escaneos activos que puedan ser detectados o utilizados de forma ofensiva.

### Características Principales

✅ **Análisis Pasivo** - No envía paquetes a la red, solo lee información existente  
✅ **Defensivo** - Sin herramientas de escaneo o ataque  
✅ **Trazabilidad Completa** - Todos los análisis guardados en Alucard  
✅ **Guías Manuales** - Checklist paso a paso para auditar el router  
✅ **Alertas Inteligentes** - Detecta configuraciones inseguras  

---

## Archivos Creados

### Scripts

#### `scripts/analyze_network.ps1`
Script principal de análisis de red que realiza:
- Descubrimiento de dispositivos (ARP cache)
- Análisis de adaptadores de red
- Conexiones TCP activas
- Puertos en escucha (superficie de ataque)
- Estado del firewall de Windows
- Configuración DNS
- Generación de alertas de seguridad

**Uso**:
```powershell
cd c:\test\Alucard
.\scripts\analyze_network.ps1
```

### Documentación

#### `docs/ROUTER_SECURITY_AUDIT.md`
Guía completa de auditoría manual del router que incluye:
- Checklist de seguridad de acceso
- Verificación de cifrado WiFi
- Revisión de firewall y port forwarding
- Actualización de firmware
- Configuración DNS
- Puntuación de seguridad

**Uso**: Seguir el checklist paso a paso para revisar manualmente la configuración del router.

### Logs y Reportes

#### `logs/network/`
Directorio de logs de red con estructura:
```
logs/network/
├── devices_YYYY-MM-DD.json          # Dispositivos detectados
├── connections_YYYY-MM-DD.json      # Conexiones activas
└── reports/
    └── network_analysis_YYYY-MM-DD_HH-mm-ss.md  # Reportes generados
```

---

## Resultados del Primer Análisis

**Fecha**: 2025-12-19 16:51:45  
**Sistema**: DESKTOP-3C4RQ7N

### Hallazgos Principales

#### Dispositivos en Red
- **Total**: 15 dispositivos detectados
- **Router**: 192.168.0.1 (Gateway)
- **Dispositivos activos**: 3 (IPs dinámicas)
- **Multicast/Broadcast**: 12 (direcciones estáticas)

#### Conexiones Activas
- **Total**: 82 conexiones TCP establecidas
- **Top IPs remotas**:
  - 127.0.0.1 (localhost): 36 conexiones
  - 34.120.68.241 (Google Cloud): 12 conexiones
  - 142.251.5.81 (Google): 8 conexiones

#### Superficie de Ataque
- **Puertos en escucha**: 38 puertos
- **Puertos públicos críticos**: 
  - Puerto 135 (RPC) - svchost
  - Puerto 445 (SMB) - System
  - Puerto 27036 (Steam)
  - Puertos dinámicos: 49664-49685

#### Firewall de Windows
- ✅ **Domain**: Activo
- ✅ **Private**: Activo  
- ✅ **Public**: Activo (Block inbound, Allow outbound)

#### DNS
- **Servidor**: 192.168.0.1 (Router local)

### Alertas Generadas

🟡 **ADVERTENCIA**: Puertos escuchando en todas las interfaces (0.0.0.0):
- 135, 5040, 27036, 49664, 49665, 49666, 49669, 49674, 49685

**Recomendación**: Revisar si estos servicios necesitan estar accesibles desde toda la red.

---

## Próximos Pasos

### 1. Auditoría Manual del Router

Sigue la guía completa en `docs/ROUTER_SECURITY_AUDIT.md` para revisar:

- [ ] Contraseña de administrador del router
- [ ] Administración remota (debe estar desactivada)
- [ ] Cifrado WiFi (WPA2/WPA3)
- [ ] WPS (debe estar desactivado)
- [ ] UPnP (debe estar desactivado)
- [ ] Firmware actualizado
- [ ] Port forwarding (revisar reglas)
- [ ] Firewall del router

### 2. Investigar Dispositivos Desconocidos

Revisa la lista de dispositivos en `logs/network/devices_2025-12-19.json` e identifica:
- Dispositivos que no reconoces
- MACs sospechosas
- Conexiones inesperadas

### 3. Cerrar Puertos Innecesarios

Revisa los puertos en escucha y cierra los que no necesites:
- Puerto 27036 (Steam) - ¿Necesitas compartir juegos en red?
- Puertos RPC/SMB - ¿Necesitas compartir archivos?

### 4. Ejecutar Análisis Periódicos

Programa el script para ejecutarse regularmente:
```powershell
# Ejecutar análisis semanal
.\scripts\analyze_network.ps1
```

### 5. Documentar Cambios

Documenta todos los cambios de seguridad en este repositorio para mantener trazabilidad.

---

## Seguridad del Sistema

### Enfoque Defensivo

Este sistema está diseñado con seguridad en mente:

✅ **Sin escaneos activos** - No envía paquetes de red  
✅ **Sin herramientas ofensivas** - No incluye escáneres de puertos o vulnerabilidades  
✅ **Solo lectura** - Lee información del sistema sin modificar nada  
✅ **Trazabilidad** - Todos los análisis guardados en Git  

### Limitaciones

❌ **No puede acceder al router directamente** - Requiere revisión manual  
❌ **No detecta vulnerabilidades** - Solo muestra configuración actual  
❌ **No realiza pruebas de penetración** - Es un sistema defensivo  

---

## Trazabilidad

Todos los análisis y cambios están documentados en el repositorio Alucard:

- **Scripts**: `scripts/analyze_network.ps1`
- **Documentación**: `docs/ROUTER_SECURITY_AUDIT.md`
- **Logs**: `logs/network/`
- **Reportes**: `logs/network/reports/`

Cada ejecución genera:
1. Reporte en Markdown con timestamp
2. JSON de dispositivos detectados
3. JSON de conexiones activas

---

## Soporte

Para preguntas o problemas:
1. Revisa la documentación en `docs/`
2. Consulta los logs en `logs/network/`
3. Revisa el código en `scripts/analyze_network.ps1`

---

*Sistema de Auditoría de Red - Alucard*  
*Modo: Defensivo - Sin escaneos activos*  
*Última actualización: 2025-12-19*
