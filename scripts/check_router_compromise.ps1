# Router Compromise Detection Script - Alucard
# Detects indicators of router compromise using defensive techniques
# No active scanning - only analyzes existing network behavior

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  DETECCION DE COMPROMISO DE ROUTER" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportDir = ".\logs\network\reports"
$reportFile = "$reportDir\router_compromise_check_$timestamp.md"

New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

$indicators = @()
$criticalFindings = 0
$warningFindings = 0

# Report header
$report = @()
$report += "# Analisis de Compromiso de Router`n"
$report += "**Fecha**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  "
$report += "**Sistema**: $env:COMPUTERNAME`n"
$report += "---`n"

# 1. DNS Hijacking Detection
Write-Host "[*] 1. Verificando DNS hijacking..." -ForegroundColor Yellow

$dnsServers = Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 }
$suspiciousDNS = $false

$report += "## 1. Servidores DNS`n"

foreach ($dns in $dnsServers) {
    $servers = $dns.ServerAddresses
    $report += "### $($dns.InterfaceAlias)"
    
    foreach ($server in $servers) {
        $report += "- DNS: ``$server``"
        
        # Check if DNS is not router or known good DNS
        if ($server -notmatch '^192\.168\.' -and 
            $server -notmatch '^10\.' -and
            $server -notmatch '^172\.(1[6-9]|2[0-9]|3[0-1])\.' -and
            $server -ne '8.8.8.8' -and 
            $server -ne '8.8.4.4' -and
            $server -ne '1.1.1.1' -and
            $server -ne '1.0.0.1' -and
            $server -ne '9.9.9.9') {
            
            $indicators += "[CRITICO] DNS sospechoso detectado: $server en $($dns.InterfaceAlias)"
            $report += "  - [!] SOSPECHOSO - No es DNS conocido"
            $suspiciousDNS = $true
            $criticalFindings++
        }
    }
    $report += ""
}

if ($suspiciousDNS) {
    Write-Host "    [!] DNS SOSPECHOSO DETECTADO" -ForegroundColor Red
}
else {
    Write-Host "    [OK] DNS parece legitimo`n" -ForegroundColor Green
}

# 2. Gateway Verification
Write-Host "[*] 2. Verificando gateway..." -ForegroundColor Yellow

$routes = Get-NetRoute -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue
$report += "## 2. Gateway Predeterminado`n"

foreach ($route in $routes) {
    $gateway = $route.NextHop
    $report += "- Gateway: ``$gateway`` (Interfaz: $($route.InterfaceAlias))"
    
    # Gateway should be in private IP range
    if ($gateway -notmatch '^192\.168\.' -and 
        $gateway -notmatch '^10\.' -and
        $gateway -notmatch '^172\.(1[6-9]|2[0-9]|3[0-1])\.') {
        
        $indicators += "[CRITICO] Gateway sospechoso: $gateway - No es IP privada"
        $report += "  - [!] CRITICO - Gateway no es IP privada"
        $criticalFindings++
        Write-Host "    [!] GATEWAY SOSPECHOSO" -ForegroundColor Red
    }
    else {
        Write-Host "    [OK] Gateway normal ($gateway)`n" -ForegroundColor Green
    }
}
$report += "`n"

# 3. Suspicious Connections to Router
Write-Host "[*] 3. Analizando conexiones al router..." -ForegroundColor Yellow

$gateway = (Get-NetRoute -DestinationPrefix "0.0.0.0/0" | Select-Object -First 1).NextHop
$routerConnections = Get-NetTCPConnection -RemoteAddress $gateway -ErrorAction SilentlyContinue

$report += "## 3. Conexiones al Router`n"
$report += "**Gateway**: $gateway  "
$report += "**Conexiones activas**: $($routerConnections.Count)`n"

if ($routerConnections.Count -gt 0) {
    foreach ($conn in $routerConnections) {
        $proc = (Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue).ProcessName
        $report += "- Puerto local $($conn.LocalPort) -> Router:$($conn.RemotePort) - Proceso: $proc"
        
        # Suspicious ports on router
        if ($conn.RemotePort -notin @(80, 443, 53)) {
            $indicators += "[ADVERTENCIA] Conexion inusual al router: Puerto $($conn.RemotePort) desde $proc"
            $report += "  - [!] Puerto inusual"
            $warningFindings++
        }
    }
}
else {
    $report += "- Sin conexiones activas al router"
}
$report += "`n"

Write-Host "    [OK] $($routerConnections.Count) conexiones al router`n" -ForegroundColor Green

# 4. Unknown Devices on Network
Write-Host "[*] 4. Verificando dispositivos desconocidos..." -ForegroundColor Yellow

$arpData = arp -a | Out-String
$devices = @()
foreach ($line in ($arpData -split "`n")) {
    if ($line -match '^\s+(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]+)\s+(dinámico|dinamico)') {
        $devices += [PSCustomObject]@{
            IP  = $matches[1]
            MAC = $matches[2]
        }
    }
}

# Exclude gateway and this machine
$myIP = (Get-NetIPAddress -AddressFamily IPv4 | Where-Object { $_.IPAddress -match '^192\.168\.' } | Select-Object -First 1).IPAddress
$unknownDevices = $devices | Where-Object { $_.IP -ne $gateway -and $_.IP -ne $myIP }

$report += "## 4. Dispositivos en Red`n"
$report += "**Total dispositivos dinamicos**: $($devices.Count)  "
$report += "**Tu IP**: $myIP  "
$report += "**Gateway**: $gateway`n"

if ($unknownDevices.Count -gt 0) {
    $report += "### Dispositivos Desconocidos ($($unknownDevices.Count))`n"
    foreach ($dev in $unknownDevices) {
        $report += "- ``$($dev.IP)`` - MAC: ``$($dev.MAC)``"
    }
    $report += "`n"
    
    if ($unknownDevices.Count -gt 5) {
        $indicators += "[ADVERTENCIA] Muchos dispositivos desconocidos en red: $($unknownDevices.Count)"
        $warningFindings++
        Write-Host "    [!] $($unknownDevices.Count) dispositivos desconocidos (revisar)`n" -ForegroundColor Yellow
    }
    else {
        Write-Host "    [OK] $($unknownDevices.Count) dispositivos desconocidos (normal)`n" -ForegroundColor Green
    }
}
else {
    $report += "- Solo tu equipo y el gateway detectados`n"
    Write-Host "    [OK] Solo dispositivos conocidos`n" -ForegroundColor Green
}

# 5. Suspicious Outbound Connections
Write-Host "[*] 5. Analizando conexiones sospechosas..." -ForegroundColor Yellow

$connections = Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue
$suspiciousConns = @()

# Check for connections to suspicious ports
foreach ($conn in $connections) {
    # Skip localhost
    if ($conn.RemoteAddress -eq "127.0.0.1" -or $conn.RemoteAddress -eq "::1") { continue }
    
    # Check for suspicious ports (common C2 ports)
    if ($conn.RemotePort -in @(4444, 5555, 6666, 7777, 8888, 31337, 12345)) {
        $proc = (Get-Process -Id $conn.OwningProcess -ErrorAction SilentlyContinue).ProcessName
        $suspiciousConns += [PSCustomObject]@{
            RemoteIP   = $conn.RemoteAddress
            RemotePort = $conn.RemotePort
            LocalPort  = $conn.LocalPort
            Process    = $proc
        }
    }
}

$report += "## 5. Conexiones Sospechosas`n"

if ($suspiciousConns.Count -gt 0) {
    $report += "**[!] ADVERTENCIA**: Conexiones a puertos sospechosos detectadas`n"
    foreach ($sc in $suspiciousConns) {
        $report += "- ``$($sc.RemoteIP):$($sc.RemotePort)`` - Proceso: $($sc.Process)"
        $indicators += "[CRITICO] Conexion a puerto sospechoso: $($sc.RemoteIP):$($sc.RemotePort) desde $($sc.Process)"
        $criticalFindings++
    }
    $report += "`n"
    Write-Host "    [!] CONEXIONES SOSPECHOSAS DETECTADAS" -ForegroundColor Red
}
else {
    $report += "- Sin conexiones a puertos sospechosos conocidos`n"
    Write-Host "    [OK] Sin conexiones sospechosas`n" -ForegroundColor Green
}

# 6. Check for Port Forwarding (indirect detection)
Write-Host "[*] 6. Verificando indicadores de port forwarding..." -ForegroundColor Yellow

$publicListening = Get-NetTCPConnection -State Listen | Where-Object { 
    $_.LocalAddress -eq "0.0.0.0" -or $_.LocalAddress -eq "::" 
}

$report += "## 6. Puertos Publicos (Posible Port Forwarding)`n"
$report += "**Puertos escuchando en todas las interfaces**: $($publicListening.Count)`n"

$riskyPorts = $publicListening | Where-Object { 
    $_.LocalPort -in @(21, 22, 23, 3389, 5900, 8080, 8888) 
}

if ($riskyPorts.Count -gt 0) {
    $report += "### Puertos de Alto Riesgo`n"
    foreach ($port in $riskyPorts) {
        $proc = (Get-Process -Id $port.OwningProcess -ErrorAction SilentlyContinue).ProcessName
        $report += "- Puerto ``$($port.LocalPort)`` - $proc"
        $portName = switch ($port.LocalPort) {
            21 { "FTP" }
            22 { "SSH" }
            23 { "Telnet" }
            3389 { "RDP" }
            5900 { "VNC" }
            default { "Servicio web" }
        }
        $indicators += "[ADVERTENCIA] Puerto de riesgo expuesto: $($port.LocalPort) ($portName) - $proc"
        $warningFindings++
    }
    $report += "`n"
    Write-Host "    [!] Puertos de riesgo detectados`n" -ForegroundColor Yellow
}
else {
    $report += "- Sin puertos de alto riesgo expuestos`n"
    Write-Host "    [OK] Sin puertos de alto riesgo`n" -ForegroundColor Green
}

# 7. Summary and Verdict
Write-Host "`n[*] Generando veredicto..." -ForegroundColor Yellow

$report += "---`n"
$report += "## Resumen de Hallazgos`n"
$report += "**Indicadores criticos**: $criticalFindings  "
$report += "**Advertencias**: $warningFindings  "
$report += "**Total indicadores**: $($indicators.Count)`n"

if ($indicators.Count -eq 0) {
    $verdict = "[OK] No se detectaron indicadores de compromiso"
    $verdictColor = "Green"
    $report += "### Veredicto: SIN INDICADORES DE COMPROMISO`n"
    $report += "El router parece estar seguro basado en el analisis pasivo.`n"
}
elseif ($criticalFindings -gt 0) {
    $verdict = "[CRITICO] POSIBLE COMPROMISO DETECTADO"
    $verdictColor = "Red"
    $report += "### Veredicto: POSIBLE COMPROMISO`n"
    $report += "Se detectaron indicadores criticos. Accion inmediata requerida.`n"
}
else {
    $verdict = "[ADVERTENCIA] Indicadores sospechosos detectados"
    $verdictColor = "Yellow"
    $report += "### Veredicto: REVISAR`n"
    $report += "Se detectaron advertencias. Revisar configuracion.`n"
}

$report += "### Indicadores Detectados`n"
if ($indicators.Count -gt 0) {
    foreach ($ind in $indicators) {
        $report += "- $ind"
    }
}
else {
    $report += "- Ninguno"
}
$report += "`n"

# Recommendations
$report += "---`n"
$report += "## Recomendaciones`n"

if ($criticalFindings -gt 0) {
    $report += "### ACCION INMEDIATA`n"
    $report += "1. **Desconectar el router de Internet** temporalmente"
    $report += "2. **Cambiar todas las contrasenas** (router, WiFi, admin)"
    $report += "3. **Resetear el router** a valores de fabrica"
    $report += "4. **Actualizar firmware** a la ultima version"
    $report += "5. **Revisar dispositivos conectados** y bloquear desconocidos"
    $report += "6. **Escanear todos los equipos** con antivirus actualizado`n"
}
elseif ($warningFindings -gt 0) {
    $report += "1. Revisar la configuracion del router manualmente"
    $report += "2. Verificar que el DNS sea correcto"
    $report += "3. Cerrar puertos innecesarios"
    $report += "4. Actualizar firmware del router"
    $report += "5. Cambiar contrasenas si no se ha hecho recientemente`n"
}
else {
    $report += "1. Mantener el router actualizado"
    $report += "2. Revisar periodicamente con este script"
    $report += "3. Seguir la guia de auditoria manual: ``docs/ROUTER_SECURITY_AUDIT.md```n"
}

$report += "---`n"
$report += "## Trazabilidad`n"
$report += "- Reporte: ``$reportFile``"
$report += "- Repositorio: Alucard (GitHub)`n"
$report += "*Analisis defensivo - Sin escaneos activos*"

# Save report
$report -join "`n" | Out-File -FilePath $reportFile -Encoding UTF8

# Display verdict
Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host $verdict -ForegroundColor $verdictColor
Write-Host "Criticos: $criticalFindings | Advertencias: $warningFindings" -ForegroundColor Gray
Write-Host "Reporte: $reportFile" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan
