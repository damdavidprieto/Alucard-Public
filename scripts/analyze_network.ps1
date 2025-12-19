# Network Security Analysis - Alucard
# Defensive passive monitoring - No active scanning
# Results saved to Alucard repository

Write-Host "`n=========================================" -ForegroundColor Cyan
Write-Host "  ANALISIS DE SEGURIDAD DE RED - ALUCARD" -ForegroundColor Cyan
Write-Host "=========================================`n" -ForegroundColor Cyan

$timestamp = Get-Date -Format "yyyy-MM-dd_HH-mm-ss"
$reportDir = ".\logs\network\reports"
$reportFile = "$reportDir\network_analysis_$timestamp.md"

# Create directories
New-Item -ItemType Directory -Force -Path $reportDir | Out-Null

# Initialize report
$output = @()
$output += "# Analisis de Seguridad de Red`n"
$output += "**Fecha**: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')  "
$output += "**Sistema**: $env:COMPUTERNAME  "
$output += "**Usuario**: $env:USERNAME  `n"
$output += "---`n"
$output += "## Resumen`n"
$output += "Analisis pasivo y defensivo. Sin escaneos activos.`n"

# 1. Dispositivos en red
Write-Host "[*] Dispositivos en red..." -ForegroundColor Yellow
$arpData = arp -a | Out-String
$devices = @()
foreach ($line in ($arpData -split "`n")) {
    if ($line -match '^\s+(\d+\.\d+\.\d+\.\d+)\s+([0-9a-f-]+)\s+(\w+)') {
        $devices += [PSCustomObject]@{
            IP   = $matches[1]
            MAC  = $matches[2]
            Type = $matches[3]
        }
    }
}

Write-Host "    [OK] $($devices.Count) dispositivos`n" -ForegroundColor Green

$output += "## 1. Dispositivos en Red`n"
$output += "**Total**: $($devices.Count)`n"
foreach ($d in $devices) {
    $output += "- **$($d.IP)** - MAC: $($d.MAC) - Tipo: $($d.Type)"
}
$output += "`n"

# Save JSON
$devices | ConvertTo-Json | Out-File ".\logs\network\devices_$(Get-Date -Format 'yyyy-MM-dd').json" -Encoding UTF8

# 2. Adaptadores
Write-Host "[*] Adaptadores de red..." -ForegroundColor Yellow
$adapters = Get-NetAdapter | Where-Object { $_.Status -eq "Up" }
Write-Host "    [OK] $($adapters.Count) activos`n" -ForegroundColor Green

$output += "## 2. Adaptadores Activos`n"
foreach ($a in $adapters) {
    $ip = (Get-NetIPAddress -InterfaceIndex $a.ifIndex -AddressFamily IPv4 -ErrorAction SilentlyContinue | Select-Object -First 1).IPAddress
    $gw = (Get-NetRoute -InterfaceIndex $a.ifIndex -DestinationPrefix "0.0.0.0/0" -ErrorAction SilentlyContinue | Select-Object -First 1).NextHop
    $output += "### $($a.Name)"
    $output += "- Estado: $($a.Status)"
    $output += "- MAC: $($a.MacAddress)"
    $output += "- IP: $ip"
    $output += "- Gateway: $gw`n"
}

# 3. Conexiones
Write-Host "[*] Conexiones activas..." -ForegroundColor Yellow
$conns = Get-NetTCPConnection -State Established -ErrorAction SilentlyContinue
Write-Host "    [OK] $($conns.Count) conexiones`n" -ForegroundColor Green

$output += "## 3. Conexiones TCP Activas`n"
$output += "**Total**: $($conns.Count)`n"
$topIPs = $conns | Group-Object RemoteAddress | Sort-Object Count -Descending | Select-Object -First 10
foreach ($ip in $topIPs) {
    $output += "- **$($ip.Name)**: $($ip.Count) conexiones"
}
$output += "`n"

# Save JSON
$conns | Select-Object LocalAddress, LocalPort, RemoteAddress, RemotePort, State | ConvertTo-Json | Out-File ".\logs\network\connections_$(Get-Date -Format 'yyyy-MM-dd').json" -Encoding UTF8

# 4. Puertos en escucha
Write-Host "[*] Puertos en escucha..." -ForegroundColor Yellow
$listening = Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue
Write-Host "    [OK] $($listening.Count) puertos`n" -ForegroundColor Green

$output += "## 4. Superficie de Ataque`n"
$output += "**Puertos en escucha**: $($listening.Count)`n"
foreach ($p in ($listening | Sort-Object LocalPort | Select-Object -First 20)) {
    $proc = (Get-Process -Id $p.OwningProcess -ErrorAction SilentlyContinue).ProcessName
    if (-not $proc) { $proc = "Unknown" }
    $output += "- Puerto **$($p.LocalPort)** en $($p.LocalAddress) - Proceso: $proc"
}
$output += "`n"

# 5. Firewall
Write-Host "[*] Firewall..." -ForegroundColor Yellow
$fw = Get-NetFirewallProfile

$output += "## 5. Firewall de Windows`n"
foreach ($f in $fw) {
    $status = if ($f.Enabled) { "[OK] ACTIVO" } else { "[X] DESACTIVADO" }
    $color = if ($f.Enabled) { "Green" } else { "Red" }
    Write-Host "    $status - $($f.Name)" -ForegroundColor $color
    $output += "- **$($f.Name)**: $($f.Enabled) - In: $($f.DefaultInboundAction) - Out: $($f.DefaultOutboundAction)"
}
Write-Host ""
$output += "`n"

# 6. DNS
Write-Host "[*] DNS..." -ForegroundColor Yellow
$dns = Get-DnsClientServerAddress -AddressFamily IPv4 | Where-Object { $_.ServerAddresses.Count -gt 0 }
Write-Host "    [OK] Configurado`n" -ForegroundColor Green

$output += "## 6. Servidores DNS`n"
foreach ($d in $dns) {
    $servers = $d.ServerAddresses -join ", "
    $output += "- **$($d.InterfaceAlias)**: $servers"
}
$output += "`n"

# 7. Alertas
Write-Host "[*] Alertas..." -ForegroundColor Yellow
$alerts = @()

$fwOff = $fw | Where-Object { -not $_.Enabled }
if ($fwOff) {
    $alerts += "[CRITICO] Firewall desactivado en $($fwOff.Name -join ', ')"
}

$publicPorts = $listening | Where-Object { $_.LocalAddress -eq "0.0.0.0" }
if ($publicPorts) {
    $ports = ($publicPorts.LocalPort | Select-Object -Unique) -join ", "
    $alerts += "[ADVERTENCIA] Puertos publicos: $ports"
}

$output += "## 7. Alertas`n"
if ($alerts.Count -eq 0) {
    $output += "[OK] Sin alertas criticas`n"
    Write-Host "    [OK] Sin alertas`n" -ForegroundColor Green
}
else {
    foreach ($a in $alerts) {
        $output += "- $a"
        Write-Host "    $a" -ForegroundColor Yellow
    }
    Write-Host ""
    $output += "`n"
}

# 8. Proximos pasos
$output += "## 8. Proximos Pasos`n"
$output += "### Auditoria Manual del Router`n"
$output += "Ver: ``docs/ROUTER_SECURITY_AUDIT.md```n"
$output += "**Puntos clave**:"
$output += "1. Cambiar contrasena por defecto"
$output += "2. Desactivar administracion remota"
$output += "3. WiFi WPA2/WPA3"
$output += "4. Desactivar WPS y UPnP"
$output += "5. Actualizar firmware`n"
$output += "---`n"
$output += "## Trazabilidad`n"
$output += "- Reporte: ``$reportFile``"
$output += "- Dispositivos: ``logs/network/devices_*.json``"
$output += "- Conexiones: ``logs/network/connections_*.json``"
$output += "- Repositorio: Alucard (GitHub)`n"
$output += "*Analisis defensivo - Sin escaneos activos*"

# Save report
$output -join "`n" | Out-File -FilePath $reportFile -Encoding UTF8

Write-Host "=========================================" -ForegroundColor Cyan
Write-Host "[OK] Analisis completado" -ForegroundColor Green
Write-Host "[INFO] Reporte: $reportFile" -ForegroundColor Cyan
Write-Host "`n[NEXT] Auditar router manualmente" -ForegroundColor Yellow
Write-Host "       Ver: docs\ROUTER_SECURITY_AUDIT.md`n" -ForegroundColor Gray
