# ==============================================================================
# 🛡️ DETECTOR DE COMPROMISO DE ROUTER - ALUCARD
# ==============================================================================
# PROPOSITO:
# Este script analiza la configuracion de tu red para buscar señales de que tu
# router podria haber sido hackeado.
#
# UTILIDAD REAL (LO QUE DETECTA):
# 1. Secuestro de DNS ("DNS Hijacking"): Forma comun de robo de cuentas. Si un virus
#    cambia tus DNS para redirigirte a webs falsas, este script lo detecta.
# 2. Ataque "Man-in-the-Middle" (Gateway Falso): Si alguien intercepta tu trafico
#    haciendose pasar por tu router, el script lo detecta.
# 3. Intrusos en WiFi: Detecta si hay demasiados dispositivos desconocidos conectados.
#
# LO QUE NO HACE:
# - No "hackea" el router para buscar vulnerabilidades (eso seria "ciberataque").
# - No analiza el firmware interno del router.
#
# COMO SE USA:
# Ejecutar desde PowerShell: .\check_router_compromise.ps1
#
# Autor: Alucard
# Repositorio: Alucard-Public
# ==============================================================================

# Limpiamos la pantalla
Clear-Host

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  DETECCION DE COMPROMISO DE ROUTER" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# 1. CONFIGURACION DE RUTAS (PORTABILIDAD)
# ------------------------------------------------------------------------------
# Usamos $PSScriptRoot para asegurar que funcione en cualquier carpeta.
$ScriptDir = $PSScriptRoot
$ProjectRoot = Split-Path -Parent $ScriptDir

# Carpetas de salida
$LogBase = Join-Path $ProjectRoot "logs"
$ReportDir = Join-Path $LogBase "network\reports"

# Fecha para el nombre del archivo
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportFile = Join-Path $ReportDir "router_compromise_check_$timestamp.md"

# Crear carpetas si no existen
if (!(Test-Path $ReportDir)) {
    New-Item -ItemType Directory -Force -Path $ReportDir | Out-Null
}

$indicators = @()
$criticalFindings = 0
$warningFindings = 0

# Cabecera del reporte
$report = @()
$report += "# Analisis de Compromiso de Router"
$report += ""
$report += "**Fecha**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  "
$report += "**Sistema**: $env:COMPUTERNAME"
$report += ""
$report += "---"
$report += ""

# ------------------------------------------------------------------------------
# 2. VERIFICACION DE DNS (DETECTAR "DNS HIJACKING")
# ------------------------------------------------------------------------------
# Explicacion:
# Si un hacker entra en tu router, lo primero que suele cambiar son los DNS.
# Al cambiar los DNS, pueden redirigirte a paginas de bancos falsas sin que lo sepas.
# Verificamos si usas DNS conocidos (Google, Cloudflare) o la IP de tu router.
# Si aparece una IP rara y desconocida, ES PELIGROSO.

Write-Host "[*] 1. Verificando DNS (Busca de secuestro de DNS)..." -ForegroundColor Yellow

$dnsServers = Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 }
$suspiciousDNS = $false

$report += "## 1. Servidores DNS"
$report += ""

foreach ($dns in $dnsServers) {
    $servers = $dns.ServerAddresses
    $report += "### Interfaz: $($dns.InterfaceAlias)"
    
    foreach ($server in $servers) {
        $report += "- DNS Detectado: **$server**"
        
        # Validamos si es una IP privada (Router) o un DNS seguro conocido
        if ($server -notmatch '^192\.168\.' -and 
            $server -notmatch '^10\.' -and
            $server -notmatch '^172\.(1[6-9]|2[0-9]|3[0-1])\.' -and
            $server -ne '8.8.8.8' -and # Google
            $server -ne '8.8.4.4' -and # Google
            $server -ne '1.1.1.1' -and # Cloudflare
            $server -ne '1.0.0.1' -and # Cloudflare
            $server -ne '9.9.9.9') {
            # Quad9
            
            # Si no es ninguno de esos, ALERTA.
            $indicators += "[CRITICO] DNS sospechoso detectado: $server en $($dns.InterfaceAlias). Podria ser un servidor malicioso."
            $report += "  - [!] SOSPECHOSO: No es un DNS comun ni local."
            $suspiciousDNS = $true
            $criticalFindings++
        }
    }
    $report += ""
}

if ($suspiciousDNS) {
    Write-Host "    [!] ALERTA: DNS SOSPECHOSO DETECTADO (Revisar reporte)" -ForegroundColor Red
}
else {
    Write-Host "    [OK] Los servidores DNS parecen legitimos" -ForegroundColor Green
}

# ------------------------------------------------------------------------------
# 3. VERIFICACION DEL GATEWAY (PUERTA DE ENLACE)
# ------------------------------------------------------------------------------
# Explicacion:
# El Gateway suele ser tu router (ej: 192.168.1.1).
# Si tu Gateway NO es una direccion privada (como 192.168.x.x), podrias estar
# conectado a una red VPN maliciosa o tener una configuracion corrupta.

Write-Host "[*] 2. Verificando Gateway (Tu Router)..." -ForegroundColor Yellow

$routes = Get-NetRoute -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue
$report += "## 2. Gateway Predeterminado"
$report += ""

foreach ($route in $routes) {
    $gateway = $route.NextHop
    $report += "- Gateway: **$gateway** (Interfaz: $($route.InterfaceAlias))"
    
    # El Gateway DEBE ser una IP privada (Red local)
    if ($gateway -notmatch '^192\.168\.' -and 
        $gateway -notmatch '^10\.' -and
        $gateway -notmatch '^172\.(1[6-9]|2[0-9]|3[0-1])\.' -and
        $gateway -ne '0.0.0.0') {
        # A veces aparece 0.0.0.0 en interfaces VPN, pero hay que revisar
        
        $indicators += "[CRITICO] Gateway sospechoso: $gateway - No parece una IP local privada."
        $report += "  - [!] CRITICO: El Gateway no es una IP privada estandar."
        $criticalFindings++
        Write-Host "    [!] GATEWAY SOSPECHOSO: $gateway" -ForegroundColor Red
    }
    else {
        Write-Host "    [OK] Gateway correcto ($gateway)" -ForegroundColor Green
    }
}
$report += ""

# ------------------------------------------------------------------------------
# 4. DISPOSITIVOS DESCONOCIDOS (DETECTAR INTRUSOS)
# ------------------------------------------------------------------------------
# Explicacion:
# Buscamos en la lista ARP (dispositivos cercanos).
# Si hay demasiados dispositivos que no son tu PC ni tu Router, podria haber intrusos
# en tu WiFi.

Write-Host "[*] 3. Buscando dispositivos desconocidos en la red..." -ForegroundColor Yellow

$arpData = arp -a | Out-String
$devices = @()
foreach ($line in ($arpData -split "`n")) {
    # Buscamos IPs dinamicas
    if ($line -match '^\s+(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]+)\s+(dinámico|dinamico)') {
        $devices += [PSCustomObject]@{
            IP  = $matches[1]
            MAC = $matches[2]
        }
    }
}

# Intentamos identificar cual es la IP del Gateway principal para excluirlo
$gateway = (Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Select-Object -First 1).NextHop

# Identificar mi propia IP
$myIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -match '^192\.168\.' } | Select-Object -First 1).IPAddress

# Filtramos: Dispositivos desconocidos = Todos - (Gateway + Yo mismo)
$unknownDevices = $devices | Where-Object { $_.IP -ne $gateway -and $_.IP -ne $myIP }

$report += "## 3. Dispositivos Extraños"
$report += ""
$report += "**Tu IP**: $myIP"
$report += "**Router**: $gateway"
$report += ""

if ($unknownDevices.Count -gt 0) {
    $report += "### Posibles Intrusos / Otros Dispositivos ($($unknownDevices.Count))"
    $report += ""
    foreach ($dev in $unknownDevices) {
        $report += "- IP: **$($dev.IP)** - MAC: $($dev.MAC)"
    }
    $report += ""
    
    # Si hay mas de 5 dispositivos desconocidos, lanzamos advertencia (en una casa normal es raro tener 20 cosas activas a la vez hablando con el PC)
    if ($unknownDevices.Count -gt 10) {
        $indicators += "[ADVERTENCIA] Hay muchos dispositivos desconocidos ($($unknownDevices.Count)). Revisa quien esta en tu WiFi."
        $warningFindings++
        Write-Host "    [!] Se encontraron $($unknownDevices.Count) dispositivos extraños (Revisar WiFi)" -ForegroundColor Yellow
    }
    else {
        Write-Host "    [OK] $($unknownDevices.Count) otros dispositivos encontrados (Normal)" -ForegroundColor Green
    }
}
else {
    $report += "- Solo tu equipo y el router estan visibles."
    Write-Host "    [OK] Red limpia (Solo tu y el router)" -ForegroundColor Green
}
$report += ""

# ------------------------------------------------------------------------------
# 5. GENERAR VEREDICTO FINAL
# ------------------------------------------------------------------------------

Write-Host "`n[*] Generando veredicto de seguridad..." -ForegroundColor Yellow

$report += "---"
$report += "## Resumen y Veredicto"
$report += ""
$report += "**Criticos**: $criticalFindings"
$report += "**Advertencias**: $warningFindings"
$report += ""

if ($criticalFindings -gt 0) {
    $verdict = "[PELIGRO] POSIBLE COMPROMISO DETECTADO"
    $verdictColor = "Red"
    $report += "### [!] Veredicto: PELIGRO"
    $report += "Se detectaron configuraciones criticas (DNS o Gateway) que indican un posible ataque."
    $report += "Revisa la seccion de recomendaciones abajo INMEDIATAMENTE."
}
elseif ($warningFindings -gt 0) {
    $verdict = "[PRECAUCION] Revisar configuracion"
    $verdictColor = "Yellow"
    $report += "### [!] Veredicto: PRECAUCION"
    $report += "No hay compromiso confirmado, pero hay cosas inusuales."
}
else {
    $verdict = "[OK] Router aparentemente seguro"
    $verdictColor = "Green"
    $report += "### [OK] Veredicto: SEGURO"
    $report += "No se detectaron indicadores de compromiso en este analisis pasivo."
}

$report += ""
$report += "### Indicadores Detectados"
if ($indicators.Count -gt 0) {
    foreach ($ind in $indicators) {
        $report += "- $ind"
    }
}
else {
    $report += "- Ninguno"
}
$report += ""

# ------------------------------------------------------------------------------
# 6. RECOMENDACIONES DE SEGURIDAD
# ------------------------------------------------------------------------------
$report += "---"
$report += "## Recomendaciones"
$report += ""

if ($criticalFindings -gt 0) {
    $report += "### [!] ACCION INMEDIATA REQUERIDA"
    $report += "Si no configuraste esos DNS o Gateway manualmente:"
    $report += "1. **Desconecta** el router de Internet."
    $report += "2. **Resetea** el router a valores de fabrica (boton fisico Reset)."
    $report += "3. Entra y **cambia la contraseña** de admin inmediatamente."
    $report += "4. Actualiza el firmware del router."
}
else {
    $report += "Para mantener tu router seguro:"
    $report += "1. Cambia la contraseña por defecto (no uses admin/admin)."
    $report += "2. Desactiva 'WPS' y 'UPnP' en la configuracion del router."
    $report += "3. Actualiza el firmware periodicamente."
}

$report += ""
$report += "---"
$report += "Generado por **Alucard Security Script**"

# Guardar
$report -join "`r`n" | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host $verdict -ForegroundColor $verdictColor
Write-Host "Reporte guardado en: $reportFile" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

Write-Host "Presione Enter para cerrar..."
Read-Host
