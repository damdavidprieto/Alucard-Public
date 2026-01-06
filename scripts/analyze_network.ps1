# ==============================================================================
# 🛡️ ANALISIS DE SEGURIDAD DE RED - ALUCARD
# ==============================================================================
# Propósito: Este script examina tu red de forma segura (pasiva).
#            No ataca ni escanea agresivamente, solo "escucha" y recopila información.
# ideal para entender qué está pasando en tu ordenador y red doméstica.
#
# Autor: Alucard Team
# Repositorio: Alucard-Public
# ==============================================================================

# "Clear-Host" limpia la pantalla de la terminal para empezar con un fondo limpio.
Clear-Host

# "Write-Host" escribe mensajes en la pantalla.
# "-ForegroundColor Cyan" cambia el color del texto a cian para que destaque.
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  ANALISIS DE SEGURIDAD DE RED - ALUCARD" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

# ------------------------------------------------------------------------------
# 1. CONFIGURACION DE RUTAS (PORTABILIDAD)
# ------------------------------------------------------------------------------
# Explicación:
# Para que este script funcione en el ordenador de cualquier persona, no podemos
# usar rutas fijas como "C:\Users\Juan...". Usamos variables automáticas
# como $PSScriptRoot que nos dicen dónde estamos ahora mismo.

# $PSScriptRoot es la carpeta donde guardaste este archivo .ps1.
$ScriptDir = $PSScriptRoot

# Split-Path -Parent sube un nivel (de "scripts" a la carpeta principal "Alucard-Public").
$ProjectRoot = Split-Path -Parent $ScriptDir

# Join-Path une partes de una ruta de forma segura (añade las barras \ automáticamente).
# Aquí definimos dónde guardaremos los informes (dentro de logs/AnalyzeNetwork).
$ScriptName = $MyInvocation.MyCommand.Name -replace '\.ps1$', ''
$LogBase = Join-Path $ProjectRoot "logs"
$ReportDir = Join-Path $LogBase $ScriptName
$JsonDir = Join-Path $ReportDir "json"

# Generamos la fecha y hora actual para poner nombre a los archivos.
# Ejemplo: 2025-12-21_17-30-00
$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$dateStr = Get-Date -Format "yyyy-MM-dd"

# Definimos el nombre final del reporte Markdown (.md).
$reportFile = Join-Path $ReportDir "network_analysis_$timestamp.md"

# Creamos las carpetas si no existen (-Force evita errores si ya están creadas).
Write-Host "[*] Preparando entorno..." -ForegroundColor Yellow
if (-not (Test-Path $ReportDir)) {
    New-Item -Path $ReportDir -ItemType Directory -Force | Out-Null
    Write-Host "    [+] Directorio de reportes creado: $ReportDir" -ForegroundColor DarkGray
}
if (-not (Test-Path $JsonDir)) {
    New-Item -ItemType Directory -Force -Path $JsonDir | Out-Null
}

# ------------------------------------------------------------------------------
# 2. INICIALIZACION DEL REPORTE
# ------------------------------------------------------------------------------
# Vamos a ir guardando todo el texto del reporte en una lista llamada $output.
# Al final, guardaremos esta lista en un archivo.

$output = @()
$output += "# Analisis de Seguridad de Red - Alucard-Public"
$output += ""
$output += "**Fecha**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  "
$output += "**Sistema**: $env:COMPUTERNAME  "  # Nombre de tu PC
$output += "**Usuario**: $env:USERNAME  "      # Tu usuario actual
$output += ""
$output += "---"
$output += ""
$output += "## Resumen"
$output += ""
$output += "Analisis pasivo y defensivo. Este reporte contiene informacion sobre la configuracion actual de red." 
$output += "No se han realizado escaneos activos (como Nmap agresivo) para evitar alertas."
$output += ""

# ------------------------------------------------------------------------------
# 3. ANALISIS DE DISPOSITIVOS (ARP)
# ------------------------------------------------------------------------------
# Explicación:
# ARP (Address Resolution Protocol) es como una "agenda de contactos" de tu tarjeta de red.
# Contiene las direcciones IP y MAC de los dispositivos con los que has hablado recientemente
# en tu red local (Router, otros PCs, impresora, móvil...).

Write-Host "[*] Analizando tabla ARP (Dispositivos cercanos)..." -ForegroundColor Yellow

# Ejecutamos el comando de Windows "arp -a" y capturamos el resultado.
$arpData = arp -a | Out-String

$devices = @()
# Leemos línea por línea para encontrar las IPs y MACs.
foreach ($line in ($arpData -split "`n")) {
    # Usamos una "Expresión Regular" (Regex) para identificar patrones de IP (ej: 192.168.1.1).
    if ($line -match '^\s+(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]+)\s+(\w+)') {
        # Si encontramos uno, lo guardamos en nuestra lista de dispositivos.
        $devices += [PSCustomObject]@{
            IP   = $matches[1]
            MAC  = $matches[2]
            Type = $matches[3]
        }
    }
}

Write-Host "    [OK] Se han detectado $($devices.Count) dispositivos en la cache ARP" -ForegroundColor Green

$output += "## 1. Dispositivos en Red (Tabla ARP)"
$output += ""
$output += "Estos son los dispositivos con los que tu PC ha interactuado recientemente."
$output += ""
$output += "**Total detectados**: $($devices.Count)"
$output += ""
foreach ($d in $devices) {
    $output += "- **IP**: $($d.IP) - **MAC**: $($d.MAC) - **Tipo**: $($d.Type)"
}
$output += ""

# Guardamos también en formato JSON para que sea fácil de procesar por otros programas.
$jsonDevicesPath = Join-Path $JsonDir "devices_$dateStr.json"
$devices | ConvertTo-Json | Out-File $jsonDevicesPath -Encoding UTF8

# ------------------------------------------------------------------------------
# 4. ADAPTADORES DE RED
# ------------------------------------------------------------------------------
# Explicación:
# Aquí miramos tus tarjetas de red (WiFi, Ethernet/Cable).
# Queremos saber su dirección IP (tu dni en la red) y la puerta de enlace (tu router).

Write-Host "[*] Auditando adaptadores de red..." -ForegroundColor Yellow

# Get-NetAdapter nos da la lista de tarjetas.
# "Where-Object { $_.Status -eq 'Up' }" filtra solo las que están conectadas (funcionando).
$adapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
Write-Host "    [OK] $($adapters.Count) interfaces activas encontradas" -ForegroundColor Green

$output += "## 2. Adaptadores Activos"
$output += ""
foreach ($a in $adapters) {
    # Obtenemos la IP de esta tarjeta exacta.
    $ipInfo = Get-NetIPAddress -InterfaceIndex $a.ifIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue | Select-Object -First 1
    # Obtenemos la ruta hacia internet (0.0.0.0/0) para saber cuál es el router.
    $routeInfo = Get-NetRoute -InterfaceIndex $a.ifIndex -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue | Select-Object -First 1
    
    $ip = if ($ipInfo) { $ipInfo.IPAddress } else { "No asignada" }
    $gw = if ($routeInfo) { $routeInfo.NextHop } else { "No detectado" }

    $output += "### Interfaz: $($a.Name)"
    $output += "- **Estado**: $($a.Status)"
    $output += "- **MAC Fisica**: $($a.MacAddress)"
    $output += "- **IP Local**: $ip"
    $output += "- **Gateway (Router)**: $gw"
    $output += ""
}

# ------------------------------------------------------------------------------
# 5. CONEXIONES ACTIVAS (NETSTAT)
# ------------------------------------------------------------------------------
# Explicación:
# ¿Con quién está hablando tu PC ahora mismo?
# Esto muestra todas las conexiones establecidas (navegadores web, actualizaciones, chats...).

Write-Host "[*] Identificando conexiones TCP activas..." -ForegroundColor Yellow

# Buscamos conexiones en estado "Established" (Conectado).
$conns = Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue
Write-Host "    [OK] $($conns.Count) conexiones establecidas actualmente" -ForegroundColor Green

$output += "## 3. Conexiones TCP Activas"
$output += ""
$output += "Conexiones que tu ordenador mantiene abiertas actualmente."
$output += ""
$output += "**Total**: $($conns.Count)"
$output += ""

# Hacemos un top 10 de las IPs con las que más hablas.
$topIPs = $conns | Group-Object RemoteAddress | Sort-Object Count -Descending | Select-Object -First 10
$output += "### Top 10 IPs Remotas"
$output += ""
foreach ($ip in $topIPs) {
    $output += "- **$($ip.Name)**: $($ip.Count) conexiones"
}
$output += ""

$jsonConnsPath = Join-Path $JsonDir "connections_$dateStr.json"
$conns | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State | ConvertTo-Json | Out-File $jsonConnsPath -Encoding UTF8

# ------------------------------------------------------------------------------
# 6. PUERTOS EN ESCUCHA (SUPERFICIE DE ATAQUE)
# ------------------------------------------------------------------------------
# Explicación:
# IMPORTANTE: Un "Puerto en Escucha" (Listen) es como una puerta abierta en tu casa.
# Significa que un programa de tu PC está esperando que alguien desde fuera le hable.
# Cuantos más puertos abiertos, mayor es tu "Superficie de Ataque" (más sitios por donde atacar).

Write-Host "[*] Analizando puertos en escucha (Listen)..." -ForegroundColor Yellow
$listening = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue
Write-Host "    [OK] $($listening.Count) puertos abiertos en tu sistema" -ForegroundColor Green

$output += "## 4. Superficie de Ataque (Puertos Abiertos)"
$output += ""
$output += "Estos puertos estan abiertos esperando conexiones. Revisa si reconoces los procesos."
$output += ""
$output += "**Total puertos**: $($listening.Count)"
$output += ""

# Listamos los primeros 20 puertos para no saturar el reporte.
foreach ($p in ($listening | Sort-Object LocalPort | Select-Object -First 20)) {
    # Averiguamos qué programa (.exe) abrió ese puerto.
    $proc = (Get-Process -Id $p.OwningProcess -ErrorAction SilentlyContinue).ProcessName
    if (-not $proc) { $proc = "System/Unknown" }
    
    $output += "- Puerto **$($p.LocalPort)** ($($p.LocalAddress)) - Proceso: $proc"
}
$output += ""

# ------------------------------------------------------------------------------
# 7. ESTADO DEL FIREWALL
# ------------------------------------------------------------------------------
# Explicación:
# El Firewall de Windows es tu primera línea de defensa.
# Debe estar ACTIVADO en todos los perfiles (Publico, Privado, Dominio).

Write-Host "[*] Verificando Firewall de Windows..." -ForegroundColor Yellow
$fw = Get-NetFirewallProfile

$output += "## 5. Firewall de Windows"
$output += ""
foreach ($f in $fw) {
    if ($f.Enabled) {
        $statusStr = "[OK] ACTIVO"
        $consoleColor = "Green"
        $icon = "OK"
    }
    else {
        # Si está desactivado, lo marcamos en ROJO.
        $statusStr = "[X] DESACTIVADO (PELIGRO)"
        $consoleColor = "Red"
        $icon = "PELIGRO"
    }
    
    Write-Host "    $statusStr - Perfil: $($f.Name)" -ForegroundColor $consoleColor
    $output += "- **Perfil $($f.Name)** ($icon): Activado: $($f.Enabled) | Entrada: $($f.DefaultInboundAction)"
}
Write-Host ""
$output += ""

# ------------------------------------------------------------------------------
# 8. DNS (RESOLUCION DE NOMBRES)
# ------------------------------------------------------------------------------
# Explicación:
# El DNS es quien traduce "google.com" a "142.250.x.x".
# Si usas un DNS malicioso, podrían dirigirte a webs falsas.

Write-Host "[*] Verificando configuracion DNS..." -ForegroundColor Yellow
$dns = Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 }
Write-Host "    [OK] Configuracion DNS obtenida" -ForegroundColor Green

$output += "## 6. Servidores DNS"
$output += ""
foreach ($d in $dns) {
    $servers = $d.ServerAddresses -join ", "
    $output += "- **Interfaz ($($d.InterfaceAlias))**: $servers"
}
$output += ""

# ------------------------------------------------------------------------------
# 9. SISTEMA DE ALERTAS
# ------------------------------------------------------------------------------
# Analizamos los datos anteriores buscando problemas obvios.

Write-Host "[*] Generando alertas de seguridad..." -ForegroundColor Yellow
$alerts = @()

# Alerta 1: Firewall desactivado (Muy grave)
$fwOff = $fw | Where-Object { -not $_.Enabled }
if ($fwOff) {
    $alerts += "CRITICO: El Firewall esta desactivado en el perfil: $($fwOff.Name)"
}

# Alerta 2: Puertos expuestos a todo internet (IP 0.0.0.0)
# Esto es peligroso en redes publicas (cafeterias, aeropuertos).
$publicPorts = $listening | Where-Object { $_.LocalAddress -eq "0.0.0.0" }
if ($publicPorts) {
    $ports = ($publicPorts.LocalPort | Select-Object -Unique) -join ", "
    $alerts += "ADVERTENCIA: Hay puertos expuestos a todas las interfaces (0.0.0.0): $ports. Revisa si es necesario."
}

$output += "## 7. Hallazgos y Alertas"
$output += ""
if ($alerts.Count -eq 0) {
    $output += "**Sistema saludable**: No se detectaron alertas criticas en este analisis basico."
    $output += ""
    Write-Host "    [OK] El sistema parece saludable (sin alertas graves)" -ForegroundColor Green
}
else {
    foreach ($a in $alerts) {
        $output += "- $a"
        Write-Host "    $a" -ForegroundColor Yellow
    }
    Write-Host ""
    $output += ""
}

# ------------------------------------------------------------------------------
# 10. CIERRE Y GUARDADO
# ------------------------------------------------------------------------------
$output += "## 8. Proximos Pasos"
$output += ""
$output += "Este script es solo el primer paso (Reconocimiento). Para mejorar tu seguridad:"
$output += "1. Si encontraste dispositivos desconocidos en la seccion 1, investiga sus MACs."
$output += "2. Asegurate de que el Firewall este siempre activo."
$output += "3. Cierra aplicaciones que abran puertos innecesarios (Seccion 4)."
$output += ""
$output += "---"
$output += ""
$output += "Generado por **Alucard Security Script** - Repositorio: Alucard-Public"

# Escribimos el archivo final con codificacion UTF8 universal.
$output -join "`r`n" | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "[OK] Analisis completado exitosamente" -ForegroundColor Green
Write-Host "[INFO] Reporte guardado en:" -ForegroundColor Cyan
Write-Host "       $reportFile" -ForegroundColor Gray
Write-Host "`n[TIP] Abre el archivo .md para ver el detalle." -ForegroundColor Yellow
Write-Host "=========================================" -ForegroundColor Cyan

# Pausa eliminada para automatizacion
# Write-Host "Presione Enter para cerrar..."
# Read-Host
