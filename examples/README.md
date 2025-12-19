# Ejemplos de Salida - Alucard

Esta carpeta contiene ejemplos de salida de los scripts de Alucard con **datos ficticios**.

## 📄 Archivos de Ejemplo

### `sample_network_analysis.md`
Ejemplo de salida del script `analyze_network.ps1`

**Muestra**:
- Dispositivos en red (IPs y MACs de ejemplo)
- Adaptadores activos
- Conexiones TCP
- Puertos en escucha
- Configuración de firewall y DNS
- Alertas de seguridad

### `sample_router_check.md`
Ejemplo de salida del script `check_router_compromise.ps1`

**Muestra**:
- Verificación de DNS
- Verificación de gateway
- Análisis de conexiones
- Detección de dispositivos desconocidos
- Verificación de puertos sospechosos
- Veredicto final

## ⚠️ Importante

**Todos los datos en estos archivos son ficticios**:
- IPs: 192.168.1.x (ejemplos genéricos)
- MACs: XX:XX:XX:XX:XX:XX (placeholders)
- Nombres: DESKTOP-EJEMPLO, usuario (genéricos)

**No contienen información real** de ningún sistema.

## 🎯 Propósito

Estos ejemplos sirven para:
1. Entender el formato de salida de los scripts
2. Ver qué tipo de información se analiza
3. Aprender a interpretar los resultados
4. Tener referencia sin ejecutar los scripts

## 🚀 Uso Real

Para generar reportes con datos reales de tu sistema:

```powershell
# Análisis de red
.\scripts\analyze_network.ps1

# Verificación de router
.\scripts\check_router_compromise.ps1
```

**Nota**: Los reportes reales se guardan en `logs/network/reports/` (no incluido en este repositorio público por contener datos sensibles).

---

*Ejemplos creados para el proyecto Alucard - Blue Team Learning Journey*
