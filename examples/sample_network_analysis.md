# Análisis de Seguridad de Red - Ejemplo

**Fecha**: 2025-XX-XX XX:XX:XX  
**Sistema**: DESKTOP-EJEMPLO  
**Usuario**: usuario  

---

## Resumen

Análisis pasivo y defensivo. Sin escaneos activos.

> **Nota**: Este es un archivo de ejemplo con datos ficticios para demostrar el formato de salida del script `analyze_network.ps1`.

---

## 1. Dispositivos en Red

**Total**: 3 (ejemplo)

- **192.168.1.1** - MAC: XX:XX:XX:XX:XX:01 - Tipo: dinámico (Router)
- **192.168.1.100** - MAC: XX:XX:XX:XX:XX:02 - Tipo: dinámico (Este equipo)
- **192.168.1.150** - MAC: XX:XX:XX:XX:XX:03 - Tipo: dinámico (Otro dispositivo)

### Análisis
- Router detectado en gateway
- 2 dispositivos adicionales en la red
- Todas las MACs son de ejemplo

---

## 2. Adaptadores Activos

### Ethernet
- Estado: Up
- MAC: XX:XX:XX:XX:XX:02
- IP: 192.168.1.100
- Gateway: 192.168.1.1

---

## 3. Conexiones TCP Activas

**Total**: 5 (ejemplo)

### Conexiones Locales
```
Local: 192.168.1.100:50000 → Remote: 192.168.1.1:443 (HTTPS)
Local: 192.168.1.100:50001 → Remote: 8.8.8.8:53 (DNS)
```

### Análisis
- Conexiones normales a servicios estándar
- Sin conexiones sospechosas detectadas

---

## 4. Puertos en Escucha

**Total**: 3 (ejemplo)

```
TCP 0.0.0.0:135 (RPC)
TCP 0.0.0.0:445 (SMB)
TCP 127.0.0.1:5357 (WSDAPI)
```

### Análisis
- Puertos estándar de Windows
- SMB solo en red local
- Sin puertos no autorizados

---

## 5. Configuración de Firewall

**Estado**: Activo ✅

- Perfil de Dominio: Activo
- Perfil Privado: Activo
- Perfil Público: Activo

---

## 6. Configuración DNS

**Servidores DNS**:
- Primario: 8.8.8.8 (Google DNS)
- Secundario: 8.8.4.4 (Google DNS)

---

## 7. Alertas de Seguridad

### ✅ Sin Alertas Críticas

**Verificaciones realizadas**:
- ✅ Firewall activo
- ✅ DNS configurado correctamente
- ✅ Sin puertos sospechosos
- ✅ Conexiones normales

---

## Conclusión

**Estado de Seguridad**: ✅ BUENO

El análisis no detectó problemas de seguridad evidentes. La configuración de red parece normal y segura.

---

*Este es un archivo de ejemplo. Los datos son ficticios y solo demuestran el formato de salida.*
