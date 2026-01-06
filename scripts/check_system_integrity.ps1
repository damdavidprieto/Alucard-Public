
# ALUCARD SYSTEM INTEGRITY - CHEQUEO DE SALUD
# ==============================================================================================
# Fecha: 2025-12-22
# Proposito: Verificar si tu PC esta "sano" y seguro antes de empezar a trabajar.
#
# QUE HACE ESTE SCRIPT? (Explicacion para principiantes)
# Imagina que este script es un medico que revisa los signos vitales de tu Windows.
# Revisa 7 cosas criticas para asegurarse de que nadie haya entrado a tu sistema.
# 1. Eres el jefe? (Admin)
# 2. Tienes el escudo activado? (Antivirus)
# 3. Quien mas vive aqui? (Usuarios extranos)
# 4. El mapa de carreteras es correcto? (Archivo Hosts)
# 5. Que programas arrancan solos? (Persistencia)
# 6. Hay intrusos escondidos en el sotano? (Carpetas temporales)
# 7. Alguien entro y salio sin que te enteraras? (Analisis historico)
# ==============================================================================================

# Silenciamos errores tecnicos feos para que la salida sea limpia
$ErrorActionPreference = "SilentlyContinue"
# Aseguramos compatibilidad
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

# =========================================================
# CONFIGURACION DE REPORTE (NUEVO)
# =========================================================
$ScriptName = $MyInvocation.MyCommand.Name -replace '\.ps1$', ''
$reportDir = Join-Path $PSScriptRoot "..\logs\$ScriptName"
if (-not (Test-Path $reportDir)) { New-Item -ItemType Directory -Path $reportDir -Force | Out-Null }
$reportPath = Join-Path $reportDir "${ScriptName}_Report_$(Get-Date -Format 'yyyyMMdd_HHmm').txt"
"ALUCARD - REPORTE DE INTEGRIDAD`nFecha: $(Get-Date)" | Out-File -FilePath $reportPath -Encoding UTF8

# =========================================================
# 0. VERIFICACION DE PERMISOS (MODO LITE VS ADMIN)
# =========================================================
$currentPrincipal = New-Object Security.Principal.WindowsPrincipal([Security.Principal.WindowsIdentity]::GetCurrent())
$isAdmin = $currentPrincipal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)

if (-not $isAdmin) {
    Write-Host "`n[!] EJECUTANDO EN MODO LIMITADO (SIN ADMIN)" -ForegroundColor Yellow
    Write-Host "    Algunas pruebas se saltaran o seran parciales." -ForegroundColor DarkGray
    Write-Host "    Para un analisis completo, ejecuta como Administrador.`n" -ForegroundColor DarkGray
    Start-Sleep -Seconds 2
}

# --- HERRAMIENTAS VISUALES + LOGGING ---
# Funcion Hibrida: Escribe en Pantalla (Bonito) y en Archivo (Texto Plano)
function Log-Output {
    param(
        [string]$Message,
        [string]$Color = "Gray",
        [switch]$NoNewLine
    )
    
    # 1. Escribir en Pantalla
    if ($NoNewLine) { Write-Host $Message -NoNewline -ForegroundColor $Color }
    else { Write-Host $Message -ForegroundColor $Color }
    
    # 2. Escribir en Archivo
    # Quitamos codigos de color ANSI si los hubiera
    $cleanMsg = $Message -replace '\e\[[0-9;]*m', ''
    $cleanMsg | Out-File -FilePath $reportPath -Append -Encoding UTF8
}

function Print-Header ($title) {
    Log-Output "`n=== $title ===" -Color Cyan
}

function Print-Result ($status, $message, $detail = "") {
    if ($status -eq "OK") {
        Log-Output "  [OK] $message" -Color Green
    }
    elseif ($status -eq "WARN") {
        Log-Output "  [!]  $message" -Color Yellow
    }
    elseif ($status -eq "CRIT") {
        Log-Output "  [X]  $message" -Color Red
    }
    
    if ($detail) {
        Log-Output "       > $detail" -Color Gray
    }
}

Log-Output "`nALUCARD - SYSTEM INTEGRITY SANITY CHECK" -Color Magenta
Log-Output "   Verificando estado del host en tiempo real..." -Color Gray
Log-Output "   Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')" -Color Gray
Log-Output "   Reporte guardado en: $reportPath" -Color Cyan

# =========================================================
# 1. VERIFICAR PRIVILEGIOS DE ADMIN
# =========================================================
Print-Header "1. Privilegios de Ejecucion"
if ($isAdmin) {
    Print-Result "OK" "Ejecutando como Administrador (Analisis Completo)"
}
else {
    Print-Result "WARN" "Ejecutando como Usuario Estandar (Analisis Parcial)" "No se podran leer logs de seguridad ni detalles profundos."
}


# =========================================================
# 2. ESTADO DEL ANTIVIRUS
# =========================================================
Print-Header "2. Estado del Antivirus"
$foundAV = $false

# 2.1 Primero revisamos Windows Defender
try {
    $defender = Get-MpComputerStatus
    if ($defender.RealTimeProtectionEnabled) {
        Print-Result "OK" "Windows Defender: Proteccion en Tiempo Real ACTIVADA"
        $foundAV = $true
    }
}
catch {
    # Ignoramos error, seguimos buscando
}

# 2.2 Si Defender no es el rey, buscamos Antivirus de Terceros (BitDefender, etc)
if (-not $foundAV) {
    try {
        $avList = Get-CimInstance -Namespace root/SecurityCenter2 -ClassName AntivirusProduct -ErrorAction SilentlyContinue
        foreach ($av in $avList) {
            Print-Result "OK" "Antivirus Detectado: $($av.displayName)" "Gestion externa detectada."
            $foundAV = $true
        }
    }
    catch {
        # Fallo WMI
    }
}

# 2.3 Si no encontramos NADA
if (-not $foundAV) {
    Print-Result "CRIT" "NO SE DETECTO NINGUN ANTIVIRUS ACTIVO!" "Activa Windows Defender o tu Antivirus inmediatamente."
}


# =========================================================
# 3. AUDITORIA DE USUARIOS
# =========================================================
Print-Header "3. Auditoria de Usuarios"

$users = Get-WmiObject Win32_UserAccount -Filter "LocalAccount=True"
$guest = $users | Where-Object { $_.Name -eq "Guest" -or $_.Name -eq "Invitado" }

if ($guest.Disabled) {
    Print-Result "OK" "Cuenta de Invitado deshabilitada (Seguro)"
}
else {
    Print-Result "CRIT" "La cuenta de Invitado esta HABILITADA!" "Esto permite el acceso anonimo a tu PC. Desactivala."
}


# =========================================================
# 4. INTEGRIDAD DEL ARCHIVO HOSTS
# =========================================================
Print-Header "4. Integridad Archivo Hosts"
$hostsPath = "$env:SystemRoot\System32\drivers\etc\hosts"

if (Test-Path $hostsPath) {
    $content = Get-Content $hostsPath
    $validLines = $content | Where-Object { $_ -notmatch "^\s*#" -and $_.Trim().Length -gt 0 }
    
    if ($validLines.Count -eq 0) {
        Print-Result "OK" "Archivo Hosts limpio (0 redirecciones)"
    }
    else {
        Print-Result "WARN" "Archivo Hosts tiene modificaciones ($($validLines.Count) lineas activas)"
        foreach ($line in $validLines) {
            Log-Output "       > $line" -Color DarkGray
        }
    }
}
else {
    Print-Result "WARN" "Archivo Hosts no encontrado (Esto es muy raro)"
}


# =========================================================
# 5. PROGRAMAS DE INICIO (PERSISTENCIA)
# =========================================================
Print-Header "5. Persistencia (Items de Inicio)"

$regPaths = @(
    "HKLM:\Software\Microsoft\Windows\CurrentVersion\Run",
    "HKCU:\Software\Microsoft\Windows\CurrentVersion\Run"
)

$startupCount = 0
foreach ($path in $regPaths) {
    if (Test-Path $path) {
        $keys = Get-ItemProperty -Path $path
        foreach ($name in $keys.PSObject.Properties.Name) {
            if ($name -notin @("PSPath", "PSParentPath", "PSChildName", "PSDrive", "PSProvider")) {
                $startupCount++
                $val = $keys.$name
                if ($val -match "AppData" -or $val -match "Temp") {
                    Print-Result "WARN" "Inicio Sospechoso detectado: $name" "$val"
                }
            }
        }
    }
}
Print-Result "OK" "Revisados todos los items de inicio" "Total encontrados: $startupCount"


# =========================================================
# 6. PROCESOS FANTASMAS (EJECUTANDOSE DESDE TEMP)
# =========================================================
Print-Header "6. Procesos en Ejecucion (Paths Volatiles)"

try {
    $procs = Get-Process | Select-Object Name, Path, Id
    $susProcs = $procs | Where-Object { 
        $_.Path -match "AppData\\Local\\Temp" -or 
        $_.Path -match "Windows\\Temp" 
    }

    if ($susProcs.Count -eq 0) {
        Print-Result "OK" "Limpio: Sin procesos raros en carpetas temporales"
    }
    else {
        foreach ($p in $susProcs) {
            Print-Result "CRIT" "Proceso sospechoso detectado!: $($p.Name) (PID: $($p.Id))" "Ruta: $($p.Path)"
        }
    }
}
catch {
    Print-Result "WARN" "No pude ver todos los procesos" "Algunos son del sistema y estan protegidos."
}


# =========================================================
# 7. ANALISIS FORENSE (HISTORICO)
# =========================================================
Print-Header "7. Analisis Forense (Historico)"
Log-Output "   Analizando TODOS los logs de seguridad de la historia..." -Color Gray
Log-Output "   (Paciencia, estoy leyendo miles de eventos...)" -Color Gray

$forensicEvents = @()
$logError = $false

try {
    if (-not $isAdmin) {
        throw "RequiresAdmin"
    }

    # 4720: Usuario Creado, 4726: Usuario Eliminado, 4732: Elevado
    $events = Get-WinEvent -FilterHashtable @{
        LogName = 'Security'
        Id      = 4720, 4726, 4732
    } -ErrorAction Stop
    
    if ($events) {
        foreach ($e in $events) {
            $type = switch ($e.Id) {
                4720 { "CREADO" }
                4726 { "ELIMINADO" }
                4732 { "ELEVADO A ADMIN" }
            }
            
            $targetUser = "Desconocido"
            if ($e.Properties.Count -gt 0) {
                $msg = $e.Message
                if ($msg -match "Account Name:\s+(\w+)") { $targetUser = $matches[1] }
            }

            $forensicEvents += [PSCustomObject]@{
                Time = $e.TimeCreated
                Type = $type
                ID   = $e.Id
                User = $targetUser
            }
        }
    }
}
catch {
    $logError = $true
}

if ($logError) {
    if (-not $isAdmin) {
        Print-Result "WARN" "Analisis Forense saltado (Requiere Admin)" "No se pueden leer logs de Seguridad sin permisos."
    }
    else {
        Print-Result "WARN" "No se pudo leer el Historial de Seguridad." "Faltan permisos de auditoria o el log esta vacio."
    }
}
elseif ($forensicEvents.Count -eq 0) {
    Print-Result "OK" "Limpio: Nadie ha creado ni borrado usuarios en el historial disponible."
}
else {
    Print-Result "WARN" "Se encontraron eventos historicos ($($forensicEvents.Count)):"
    $forensicEvents | Sort-Object Time | ForEach-Object {
        $color = if ($_.Type -eq "ELIMINADO") { "Red" } else { "Yellow" }
        Log-Output "       [$($_.Time.ToString('yyyy-MM-dd HH:mm'))] $($_.Type) - Usuario: $($_.User)" -Color $color
    }
    Log-Output "`n       [!] IMPORTANTE: Si ves usuarios creados y luego borrados que no fuiste tu, INVESTIGA." -Color Yellow
}

# --- FIN DEL CHEQUEO ---
Log-Output "`n-------------------------------------------" -Color Gray
Log-Output "Verificacion completada." -Color Green
Log-Output "Reporte guardado en: $reportPath" -Color Cyan
Log-Output "Pulsa ENTER para salir..." -Color Gray
Read-Host
