# 🔍 Guía de Análisis Forense de Navegadores

## 📖 Índice

1. [¿Qué es este análisis?](#qué-es-este-análisis)
2. [¿Cuándo usarlo?](#cuándo-usarlo)
3. [Cómo ejecutar el script](#cómo-ejecutar-el-script)
4. [Interpretación de resultados](#interpretación-de-resultados)
5. [Indicadores de compromiso explicados](#indicadores-de-compromiso-explicados)
6. [Acciones recomendadas](#acciones-recomendadas)
7. [Limitaciones](#limitaciones)
8. [Preguntas frecuentes](#preguntas-frecuentes)

---

## ¿Qué es este análisis?

El script `analyze_browsers.ps1` es una herramienta de **análisis forense pasivo** que examina tus navegadores web en busca de indicadores de compromiso (IoCs) o actividad maliciosa.

### Características principales

✅ **Sin permisos de administrador** - Se ejecuta con usuario estándar  
✅ **Solo lectura** - No modifica ningún dato del navegador  
✅ **Múltiples navegadores** - Soporta Chrome, Edge, Brave, Firefox  
✅ **Reporte educativo** - Explicaciones en español de cada hallazgo  
✅ **Código abierto** - Puedes revisar exactamente qué hace

### ¿Qué analiza?

El script examina:

1. **Extensiones instaladas** - Detecta extensiones sospechosas o con permisos peligrosos
2. **Historial de navegación** - Busca dominios maliciosos conocidos
3. **Configuración del navegador** - Verifica alteraciones (proxy, página de inicio, motor de búsqueda)
4. **Certificados del sistema** - Identifica certificados raíz sospechosos
5. **Persistencia** - Detecta mecanismos de persistencia via navegador

---

## ¿Cuándo usarlo?

### Situaciones recomendadas

🔴 **Urgente - Ejecuta inmediatamente si:**
- Sospechas que tu navegador está comprometido
- Notas comportamiento extraño (redirecciones, anuncios excesivos)
- Detectaste malware en tu sistema
- Tu página de inicio cambió sin tu permiso
- Aparecen extensiones que no instalaste

🟡 **Preventivo - Ejecuta periódicamente:**
- Como parte de tu rutina de seguridad mensual
- Después de instalar software de fuentes desconocidas
- Tras visitar sitios web sospechosos
- Antes de realizar operaciones sensibles (banca online)

🟢 **Educativo:**
- Para aprender sobre indicadores de compromiso
- Para entender qué datos almacenan los navegadores
- Como práctica de análisis forense

---

## Cómo ejecutar el script

### Método 1: Ejecución directa (Recomendado)

1. **Abre PowerShell** (no requiere "Ejecutar como administrador")
2. **Navega a la carpeta del script**
   ```powershell
   cd c:\test\Alucard-Public\scripts
   ```
3. **Ejecuta el script**
   ```powershell
   .\analyze_browsers.ps1
   ```

### Método 2: Con salida detallada

```powershell
.\analyze_browsers.ps1 -Verbose
```

---

## Interpretación de resultados

### Niveles de severidad

| Icono | Severidad | Acción |
|-------|-----------|--------|
| 🔴 | **Crítico** | Actúa inmediatamente |
| 🟠 | **Alto** | Investiga hoy mismo |
| 🟡 | **Medio** | Revisa cuando puedas |
| 🔵 | **Bajo** | Informativo |

---

## Indicadores de compromiso explicados

### 🔌 Extensiones sospechosas

**Qué detecta:**
- Extensiones sin nombre legible
- Extensiones con permisos peligrosos (`webRequest`, `cookies`, `tabs`, `proxy`)

**Por qué es importante:**
Las extensiones maliciosas pueden robar cookies, interceptar páginas web, inyectar scripts maliciosos.

**Qué hacer:**
1. Abre `chrome://extensions`
2. Busca la extensión mencionada
3. Si no la reconoces: **Elimínala**

### 📜 Dominios maliciosos en historial

**Qué detecta:**
- TLDs gratuitos (`.tk`, `.ml`, `.ga`)
- Acortadores de URL
- Servicios de túnel (`ngrok.io`, `duckdns.org`)

**Qué hacer:**
1. Revisa tu historial
2. Si no recuerdas visitarlos: **Posible infección**
3. Ejecuta antivirus completo

### ⚙️ Configuración alterada

**Qué detecta:**
- Página de inicio cambiada
- Motor de búsqueda no estándar
- Configuración de proxy

**Qué hacer:**
1. Restablece página de inicio
2. Verifica motor de búsqueda
3. Desactiva proxy si no lo usas

### 🔐 Certificados sospechosos

**Qué detecta:**
- Certificados raíz autofirmados

**Qué hacer:**
1. Abre `certmgr.msc`
2. Busca el certificado
3. Si no lo reconoces: **Elimínalo**

---

## Acciones recomendadas

### Si NO se detectaron hallazgos

✅ Tu navegador parece limpio

### Si se detectaron hallazgos BAJA/MEDIA

🟡 Revisa manualmente cada hallazgo

### Si se detectaron hallazgos ALTA/CRÍTICA

🔴 **Acción inmediata:**
1. Desconecta de internet
2. Ejecuta antivirus completo
3. Considera restablecer navegador
4. Cambia contraseñas desde otro dispositivo

---

## Limitaciones

### ⚠️ Este script NO puede:

❌ Detectar malware sofisticado fuera del navegador  
❌ Analizar tráfico de red en tiempo real  
❌ Garantizar 100% que tu sistema está limpio

### ✅ Este script SÍ puede:

✅ Detectar indicadores comunes de compromiso  
✅ Identificar extensiones con permisos peligrosos  
✅ Encontrar configuraciones alteradas  
✅ Servir como primera línea de detección

---

## Preguntas frecuentes

**¿Necesito ser administrador?**  
No. El script funciona con usuario estándar.

**¿El script modifica algo?**  
No. Es 100% de solo lectura.

**¿Qué navegadores soporta?**  
Chrome, Edge, Brave, Firefox (básico)

**¿Con qué frecuencia debo ejecutarlo?**  
Mensualmente como prevención, inmediatamente si sospechas compromiso.

---

**Autor:** Proyecto Alucard  
**Versión:** 1.0  
**Licencia:** MIT

🛡️ **Alucard** - Defendiendo mientras aprendemos
