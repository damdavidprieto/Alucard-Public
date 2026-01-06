<#
================================================================================
SCRIPT DE AUDITORIA DE DATOS SENSIBLES
================================================================================

PROPOSITO:
Este script busca automáticamente datos sensibles en tu código que NO deberían
estar ahí, como contraseñas, claves API, direcciones IP privadas, etc.

¿QUE HACE?
- Escanea todos los archivos de tu proyecto
- Busca patrones de datos sensibles (passwords, API keys, IPs, emails, etc)
- Clasifica los hallazgos por severidad (CRITICO, MEDIO, BAJO)
- Identifica automáticamente archivos del honeypot (falsos positivos)
- Genera un reporte detallado en archivo de texto

¿PARA QUIEN ES?
- Desarrolladores que quieren verificar que no hay datos sensibles en el código
- Personas que van a publicar código en GitHub/GitLab
- Equipos de seguridad que auditan proyectos

================================================================================
⚠️ ADVERTENCIAS DE USO - LEE ESTO ANTES DE EJECUTAR
================================================================================

1. ESTE SCRIPT ES SOLO LECTURA
   ✅ NO modifica ningún archivo
   ✅ NO borra nada
   ✅ Solo LEE archivos y genera un reporte
   ⚠️ Es seguro ejecutarlo

2. PUEDE TARDAR VARIOS MINUTOS
   - Escanea TODOS los archivos del proyecto
   - En proyectos grandes puede tardar 5-10 minutos
   - Verás mensajes en pantalla mientras trabaja

3. GENERA UN ARCHIVO DE RESULTADOS
   - Crea: audit_results.txt
   - Ubicación: Misma carpeta que este script
   - Puedes abrirlo con Notepad o cualquier editor de texto

4. FALSOS POSITIVOS SON NORMALES
   - El script puede encontrar cosas que NO son problemas
   - Por ejemplo: ejemplos en documentación
   - Por eso clasifica por severidad (CRITICO vs INFORMATIVO)

5. REVISA LOS RESULTADOS MANUALMENTE
   - El script te AYUDA a encontrar problemas
   - TU decides qué es importante y qué no
   - Lee el reporte completo antes de tomar decisiones

================================================================================
COMO USAR ESTE SCRIPT (PARA PRINCIPIANTES EN POWERSHELL)
================================================================================

OPCION 1: Uso Básico (Recomendado)
----------------------------------
1. Abre PowerShell:
   - Presiona tecla Windows
   - Escribe "PowerShell"
   - Click derecho → "Ejecutar como administrador"

2. Navega a la carpeta del script:
   cd C:\ruta\a\tu\proyecto\scripts

3. Ejecuta el script:
   .\audit_secrets.ps1

4. Espera a que termine (puede tardar varios minutos)

5. Abre el archivo de resultados:
   notepad audit_results.txt


OPCION 2: Analizar Otra Carpeta
--------------------------------
.\audit_secrets.ps1 -Path "C:\otro\proyecto"


OPCION 3: Guardar Resultados en Otro Lugar
-------------------------------------------
.\audit_secrets.ps1 -OutputFile "C:\mis_documentos\auditoria.txt"


OPCION 4: Ambas Opciones
-------------------------
.\audit_secrets.ps1 -Path "C:\proyecto" -OutputFile "C:\resultados.txt"

================================================================================
PARAMETROS DEL SCRIPT (OPCIONALES)
================================================================================
#>

param(
    # PARAMETRO 1: Ruta del proyecto a analizar
    # 
    # ¿Qué es? La carpeta que contiene tu código
    # Por defecto: Analiza la carpeta padre de donde está este script
    # 
    # Ejemplo de uso:
    #   .\audit_secrets.ps1 -Path "C:\MiProyecto"
    #
    [Parameter(Mandatory = $false)]
    [string]$Path = (Split-Path -Parent $PSScriptRoot),
    
    # PARAMETRO 2: Archivo donde guardar los resultados
    # 
    # ¿Qué es? El archivo .txt donde se guardará el reporte
    # Por defecto: audit_results.txt en la misma carpeta que este script
    # 
    # Ejemplo de uso:
    #   .\audit_secrets.ps1 -OutputFile "C:\resultados.txt"
    #
    [Parameter(Mandatory = $false)]
    [string]$OutputFile
)

if (-not $OutputFile) {
    $ScriptName = $MyInvocation.MyCommand.Name -replace '\.ps1$', ''
    $logDir = Join-Path $PSScriptRoot "..\logs\$ScriptName"
    if (-not (Test-Path $logDir)) { New-Item -ItemType Directory -Path $logDir -Force | Out-Null }
    $OutputFile = Join-Path $logDir "${ScriptName}_results.txt"
}

# ===============================================================================
# CONFIGURACION - Palabras clave para identificar archivos del honeypot
# ===============================================================================
#
# ¿QUE ES ESTO?
# Esta lista contiene palabras que identifican archivos del honeypot.
# Si la ruta de un archivo contiene alguna de estas palabras, el script
# lo marcará como "honeypot" y sus hallazgos serán "falsos positivos".
#
# ¿POR QUE?
# El honeypot contiene credenciales FALSAS a propósito (trampas para atacantes).
# No queremos que el script las marque como problemas reales.
#
# EJEMPLO:
# Si un archivo se llama "C:\proyecto\honeypot\responses\login.py"
# El script verá la palabra "honeypot" y "responses" y dirá:
# "Este archivo es del honeypot, sus credenciales son falsas, no es problema"
#

$HONEYPOT_KEYWORDS = @(
    "honeypot",      # Carpeta principal del honeypot
    "\responses\",   # Carpeta de respuestas HTTP del honeypot
    "\profiles\",    # Perfiles de dispositivos simulados
    "\exploits",     # Exploits simulados
    "\detectors"     # Detectores de ataques
)

# ===============================================================================
# BANNER - Mensaje de inicio del script
# ===============================================================================
#
# Esta sección muestra información en pantalla cuando ejecutas el script.
# Te dice qué proyecto está analizando y dónde guardará los resultados.
#

# Extraer nombre del proyecto de la ruta analizada
# EXPLICACION: Si analizas "C:\MisProyectos\Alucard-Public"
# El nombre del proyecto será "Alucard-Public"
$projectName = Split-Path -Leaf $Path

# Si el nombre es muy genérico (test, src, etc), intentar obtener mejor nombre
# EXPLICACION: A veces la carpeta se llama "test" o "src", que no es descriptivo.
# En ese caso, el script intenta encontrar un nombre mejor.
if ($projectName -match '^(test|src|code|projects?)$') {
    $scriptParent = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
    $betterName = Split-Path -Leaf $scriptParent
    if ($betterName -and $betterName -ne $projectName) {
        $projectName = $betterName
    }
}

# Mostrar banner en pantalla con colores
# COLORES: Cyan = Azul claro, Yellow = Amarillo, Gray = Gris
Write-Host "`n=== AUDITORIA DE DATOS SENSIBLES ===" -ForegroundColor Cyan
Write-Host "Proyecto: $projectName" -ForegroundColor Cyan
Write-Host "Con detección inteligente de honeypot y niveles de severidad" -ForegroundColor Gray
Write-Host "`nAnalizando: $Path" -ForegroundColor Yellow
Write-Host "Resultados: $OutputFile" -ForegroundColor Yellow
Write-Host ""

# ===============================================================================
# VARIABLES Y CONTADORES
# ===============================================================================

# Array principal para el reporte
$results = @()
$results += "AUDITORIA DE DATOS SENSIBLES - $projectName"
$results += "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$results += "Ruta: $Path"
$results += "=" * 80
$results += ""

# Contadores generales
$honeypotMatches = 0
$realMatches = 0
$totalMatches = 0

# Contadores por severidad (para archivos NO honeypot)
$highSeverityMatches = 0    # Código ejecutable (.py, .js, etc)
$mediumSeverityMatches = 0  # Scripts (.ps1, .sh, .bat)
$lowSeverityMatches = 0     # Documentación (.md, .txt, .html)

# Arrays para almacenar hallazgos
$honeypotFindings = @()
$realFindings = @()

# Arrays por severidad
$highSeverityFindings = @()
$mediumSeverityFindings = @()
$lowSeverityFindings = @()

# Arrays para honeypot leak detection
$honeypotLeaks = @()
$honeypotLeakCount = 0

# ===============================================================================
# PATRONES DE BUSQUEDA GENERALES
# ===============================================================================

$patterns = @{
    "1. CREDENCIALES Y SECRETOS" = @(
        "password\s*=",      # password=, password =
        "passwd\s*=",        # passwd=
        "pwd\s*=",           # pwd=
        "api_key\s*=",       # api_key=
        "apikey\s*=",        # apikey=
        "secret\s*=",        # secret=
        "token\s*=",         # token=
        "auth\s*="           # auth=
    )
    
    "2. IPS PRIVADAS"            = @(
        "\b192\.168\.\d{1,3}\.\d{1,3}\b",  # 192.168.x.x
        "\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # 10.x.x.x
        "\b172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}\b"  # 172.16-31.x.x
    )
    
    "3. DIRECCIONES MAC"         = @(
        "([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"  # XX:XX:XX:XX:XX:XX
    )
    
    "4. EMAILS"                  = @(
        "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    )
    
    "5. NOMBRES DE USUARIO"      = @(
        "username\s*=",
        "user\s*=",
        "Usuario"
    )
}

# ===============================================================================
# PATRONES ESPECIFICOS PARA HONEYPOT
# ===============================================================================
# Estos patrones buscan FUGAS REALES en el honeypot
# Ignoran credenciales falsas comunes (password=admin, etc)
# Detectan: API keys reales, IPs no genéricas, MACs reales, rutas locales

$honeypotPatterns = @{
    "1. CREDENCIALES SOSPECHOSAS (No trampas)" = @(
        "api_key\s*=\s*['`"]?(sk-|pk-|rk-)",  # API keys reales
        "apikey\s*=\s*['`"]?[A-Za-z0-9]{32,}",  # Keys largas
        "token\s*=\s*['`"]?eyJ[A-Za-z0-9_-]+\.",  # JWT tokens
        "password\s*=\s*['`"]?[A-Za-z0-9!@#\$%\^&*]{12,}"  # Passwords largos
    )
    
    "2. IPS PRIVADAS (Posiblemente reales)"    = @(
        "\b192\.168\.(?!0\.1|1\.1)\d{1,3}\.\d{1,3}\b",  # No .0.1 o .1.1
        "\b10\.(?!0\.0\.1)\d{1,3}\.\d{1,3}\.\d{1,3}\b",  # No 10.0.0.1
        "\b172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}\b"
    )
    
    "3. DIRECCIONES MAC (No genéricas)"        = @(
        "(?!XX:XX|00:00:00)([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
    )
    
    "4. EMAILS (Revisar)"                      = @(
        "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    )
    
    "5. RUTAS LOCALES (Posible fuga)"          = @(
        "c:\\users\\[^\\]+",
        "c:\\test\\",
        "/home/[^/]+",
        "/Users/[^/]+"
    )
}

# ===============================================================================
# FUNCIONES
# ===============================================================================

# Función para determinar si un archivo es parte del honeypot
function Test-IsHoneypotFile {
    param([string]$FilePath)
    
    $lowerPath = $FilePath.ToLower()
    
    foreach ($keyword in $HONEYPOT_KEYWORDS) {
        if ($lowerPath -like "*$keyword*") {
            return $true
        }
    }
    
    return $false
}

# Función para determinar severidad según extensión de archivo
function Get-FileSeverity {
    param([string]$FilePath)
    
    $extension = [System.IO.Path]::GetExtension($FilePath).ToLower()
    
    # ALTA: Archivos de código ejecutable
    if ($extension -in @('.py', '.js', '.java', '.cpp', '.c', '.cs', '.rb', '.php', '.go')) {
        return 'HIGH'
    }
    # MEDIA: Scripts
    elseif ($extension -in @('.ps1', '.sh', '.bat', '.cmd')) {
        return 'MEDIUM'
    }
    # BAJA: Documentación
    elseif ($extension -in @('.md', '.txt', '.rst', '.adoc', '.html', '.htm')) {
        return 'LOW'
    }
    # Por defecto: MEDIA
    else {
        return 'MEDIUM'
    }
}

# ===============================================================================
# BUSQUEDA DE PATRONES GENERALES
# ===============================================================================

foreach ($category in $patterns.Keys | Sort-Object) {
    Write-Host "Buscando: $category..." -ForegroundColor Yellow
    
    $categoryHoneypot = 0
    $categoryReal = 0
    
    foreach ($pattern in $patterns[$category]) {
        try {
            # Obtener archivos recursivamente, excluyendo:
            # - .git
            # - node_modules
            # - audit_results.txt
            # - el script mismo (auto-exclusión)
            $files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object {
                $_.FullName -notmatch '\\.git\\' -and
                $_.FullName -notmatch '\\node_modules\\' -and
                $_.FullName -notmatch 'audit_results\.txt' -and
                $_.FullName -ne $PSCommandPath
            }
            
            # Buscar patrón en archivos
            $matches = $files | Select-String -Pattern $pattern -ErrorAction SilentlyContinue
            
            if ($matches) {
                foreach ($match in $matches) {
                    $totalMatches++
                    
                    $lineInfo = "$($match.Path):$($match.LineNumber)"
                    $lineContent = "  >> $($match.Line.Trim())"
                    
                    # Verificar si es archivo del honeypot
                    if (Test-IsHoneypotFile $match.Path) {
                        # ES HONEYPOT - Falso positivo
                        $honeypotFindings += ""
                        $honeypotFindings += "[$category] Patron: $pattern"
                        $honeypotFindings += $lineInfo
                        $honeypotFindings += $lineContent
                        $categoryHoneypot++
                        $honeypotMatches++
                    }
                    else {
                        # NO ES HONEYPOT - Clasificar por severidad
                        $severity = Get-FileSeverity $match.Path
                        
                        # Agregar a findings generales
                        $realFindings += ""
                        $realFindings += "[$category] Patron: $pattern"
                        $realFindings += $lineInfo
                        $realFindings += $lineContent
                        $categoryReal++
                        $realMatches++
                        
                        # Agregar a findings por severidad con prefijo apropiado
                        $severityPrefix = switch ($severity) {
                            'HIGH' { '[!!!]' }
                            'MEDIUM' { '[!]' }
                            'LOW' { '[i]' }
                        }
                        
                        $findingEntry = @(
                            "",
                            "$severityPrefix [$category] Patron: $pattern",
                            $lineInfo,
                            $lineContent
                        )
                        
                        switch ($severity) {
                            'HIGH' {
                                $highSeverityFindings += $findingEntry
                                $highSeverityMatches++
                            }
                            'MEDIUM' {
                                $mediumSeverityFindings += $findingEntry
                                $mediumSeverityMatches++
                            }
                            'LOW' {
                                $lowSeverityFindings += $findingEntry
                                $lowSeverityMatches++
                            }
                        }
                    }
                }
            }
        }
        catch {
            Write-Host "  Error buscando patron: $pattern" -ForegroundColor Red
        }
    }
    
    # Mostrar resumen de categoría
    if ($categoryHoneypot -gt 0 -or $categoryReal -gt 0) {
        Write-Host "  [!] Honeypot: $categoryHoneypot | Real: $categoryReal" -ForegroundColor Gray
    }
}

# ===============================================================================
# BUSQUEDA ESPECIFICA EN HONEYPOT (Fugas reales)
# ===============================================================================

Write-Host "`nEscaneando honeypot con patrones específicos..." -ForegroundColor Cyan

foreach ($category in $honeypotPatterns.Keys | Sort-Object) {
    Write-Host "  Buscando: $category..." -ForegroundColor Yellow
    
    foreach ($pattern in $honeypotPatterns[$category]) {
        try {
            # SOLO buscar en archivos del honeypot
            $files = Get-ChildItem -Path $Path -File -Recurse -ErrorAction SilentlyContinue |
            Where-Object {
                (Test-IsHoneypotFile $_.FullName) -and
                $_.FullName -notmatch 'audit_results\.txt' -and
                $_.FullName -ne $PSCommandPath
            }
            
            $matches = $files | Select-String -Pattern $pattern -ErrorAction SilentlyContinue
            
            if ($matches) {
                foreach ($match in $matches) {
                    $lineInfo = "$($match.Path):$($match.LineNumber)"
                    $lineContent = "  >> $($match.Line.Trim())"
                    
                    $honeypotLeaks += ""
                    $honeypotLeaks += "[$category] Patron: $pattern"
                    $honeypotLeaks += $lineInfo
                    $honeypotLeaks += $lineContent
                    $honeypotLeakCount++
                }
            }
        }
        catch {
            Write-Host "    Error: $_" -ForegroundColor Red
        }
    }
    
    if ($honeypotLeakCount -eq 0) {
        Write-Host "    [OK] Sin fugas detectadas" -ForegroundColor Green
    }
}

# ===============================================================================
# GENERAR REPORTE
# ===============================================================================

$results += "RESUMEN:"
$results += "Total de coincidencias: $totalMatches"
$results += "  - Honeypot (Falsos Positivos): $honeypotMatches"
$results += "  - Resto del Proyecto (REVISAR): $realMatches"
$results += "  - Fugas en Honeypot (INFORMATIVO): $honeypotLeakCount"
$results += ""

# ===============================================================================
# SECCION 1: HONEYPOT (FALSOS POSITIVOS)
# ===============================================================================

$results += ""
$results += "=" * 80
$results += "SECCION 1: HONEYPOT (FALSOS POSITIVOS)"
$results += "=" * 80
$results += ""
$results += "INFORMACION:"
$results += "Estos hallazgos estan en archivos del HONEYPOT."
$results += "Son credenciales FALSAS intencionales (trampas para atacantes)."
$results += "NO requieren accion."
$results += ""

if ($honeypotMatches -eq 0) {
    $results += "[OK] No se encontraron coincidencias en honeypot"
}
else {
    $results += "[!] Se encontraron $honeypotMatches coincidencias en honeypot:"
    $results += "-" * 80
    $results += $honeypotFindings
}

# ===============================================================================
# SECCION 1.5: FUGAS REALES EN HONEYPOT (INFORMATIVO)
# ===============================================================================

$results += ""
$results += ""
$results += "=" * 80
$results += "SECCION 1.5: FUGAS REALES EN HONEYPOT (INFORMATIVO)"
$results += "=" * 80
$results += ""
$results += "ATENCION ESPECIAL:"
$results += "Esta seccion busca datos sensibles REALES dentro del honeypot."
$results += "Ignora credenciales falsas comunes (password=admin, etc)."
$results += "Son datos sensibles REALES encontrados en archivos del honeypot."
$results += ""
$results += "EJEMPLOS DE FUGAS REALES:"
$results += "- API keys reales con prefijos sk-, pk-, rk-"
$results += "- IPs de tu red real, no las genericas 192.168.0.1"
$results += "- MACs reales, no XX:XX:XX:XX:XX:XX"
$results += "- Rutas locales como c:\users\TuNombre"
$results += "- Emails personales"
$results += ""

if ($honeypotLeakCount -eq 0) {
    $results += "[OK] No se detectaron fugas reales en el honeypot"
    $results += ""
    $results += "El honeypot solo contiene datos falsos. Perfecto!"
}
else {
    $results += "[i] INFORMATIVO: Se encontraron $honeypotLeakCount patrones para revisar:"
    $results += "-" * 80
    $results += $honeypotLeaks
    $results += ""
    $results += "ACCION REQUERIDA:"
    $results += "Revisa CADA UNA de estas fugas y sanitizalas INMEDIATAMENTE."
}

# ===============================================================================
# SECCION 2: RESTO DEL PROYECTO POR SEVERIDAD
# ===============================================================================

$results += ""
$results += ""
$results += "=" * 80
$results += "SECCION 2.1: HALLAZGOS CRITICOS (Archivos de Codigo)"
$results += "=" * 80
$results += ""
$results += "ATENCION:"
$results += "Estos hallazgos estan en archivos de CODIGO EJECUTABLE (.py, .js, etc)"
$results += "DEBEN ser revisados INMEDIATAMENTE."
$results += ""

if ($highSeverityMatches -eq 0) {
    $results += "[OK] No se encontraron hallazgos criticos en codigo"
}
else {
    $results += "[!!!] CRITICO: Se encontraron $highSeverityMatches coincidencias en codigo:"
    $results += "-" * 80
    $results += $highSeverityFindings
}

$results += ""
$results += ""
$results += "=" * 80
$results += "SECCION 2.2: HALLAZGOS MEDIOS (Scripts)"
$results += "=" * 80
$results += ""
$results += "ATENCION:"
$results += "Estos hallazgos estan en SCRIPTS (.ps1, .sh, .bat)"
$results += "Revisar para asegurar que no hay credenciales hardcodeadas."
$results += ""

if ($mediumSeverityMatches -eq 0) {
    $results += "[OK] No se encontraron hallazgos en scripts"
}
else {
    $results += "[!] Se encontraron $mediumSeverityMatches coincidencias en scripts:"
    $results += "-" * 80
    $results += $mediumSeverityFindings
}

$results += ""
$results += ""
$results += "=" * 80
$results += "SECCION 2.3: HALLAZGOS INFORMATIVOS (Documentacion)"
$results += "=" * 80
$results += ""
$results += "INFORMACION:"
$results += "Estos hallazgos estan en DOCUMENTACION (.md, .txt, .html)"
$results += "Probablemente son ejemplos educativos, pero verificar por seguridad."
$results += ""

if ($lowSeverityMatches -eq 0) {
    $results += "[OK] No se encontraron hallazgos en documentacion"
}
else {
    $results += "[i] Se encontraron $lowSeverityMatches coincidencias en documentacion:"
    $results += "-" * 80
    $results += $lowSeverityFindings
}

# ===============================================================================
# PROXIMOS PASOS
# ===============================================================================

$results += ""
$results += ""
$results += "=" * 80
$results += "PROXIMOS PASOS"
$results += "=" * 80
$results += ""
$results += "1. Revisa la Seccion 2.1 (CRITICO) primero"
$results += "2. Luego revisa la Seccion 2.2 (MEDIO)"
$results += "3. Verifica la Seccion 2.3 (BAJO) si hay tiempo"
$results += "4. La Seccion 1 (Honeypot) es informativa, no requiere accion"
$results += "5. La Seccion 1.5 requiere revision si hay hallazgos"
$results += ""

# ===============================================================================
# GUARDAR RESULTADOS
# ===============================================================================

$results | Out-File -FilePath $OutputFile -Encoding UTF8
Write-Host "Resultados guardados en: $OutputFile" -ForegroundColor Green
Write-Host "Revisa el archivo para ver los detalles completos.`n" -ForegroundColor Gray

# ===============================================================================
# RESUMEN EN CONSOLA
# ===============================================================================

Write-Host "RESUMEN:" -ForegroundColor Cyan
Write-Host "  Total: $totalMatches coincidencias" -ForegroundColor White
Write-Host "  - Honeypot (Falsos Positivos): $honeypotMatches" -ForegroundColor Gray
Write-Host "  - Resto del Proyecto (REVISAR): $realMatches" -ForegroundColor $(if ($realMatches -eq 0) { "Green" } else { "Yellow" })
Write-Host "  - Fugas en Honeypot (INFORMATIVO): $honeypotLeakCount" -ForegroundColor $(if ($honeypotLeakCount -eq 0) { "Green" } else { "Yellow" })
Write-Host ""
Write-Host "Por Severidad:" -ForegroundColor Cyan
Write-Host "  - CRITICO (Codigo): $highSeverityMatches" -ForegroundColor $(if ($highSeverityMatches -eq 0) { "Green" } else { "Red" })
Write-Host "  - MEDIO (Scripts): $mediumSeverityMatches" -ForegroundColor $(if ($mediumSeverityMatches -eq 0) { "Green" } else { "Yellow" })
Write-Host "  - BAJO (Docs): $lowSeverityMatches" -ForegroundColor $(if ($lowSeverityMatches -eq 0) { "Green" } else { "Gray" })

if ($honeypotLeakCount -gt 0) {
    Write-Host "`n[i] INFORMATIVO: Patrones detectados en honeypot (revisar si son ejemplos)" -ForegroundColor Yellow
    Write-Host "Revisa la Seccion 1.5 del reporte INMEDIATAMENTE.`n" -ForegroundColor Yellow
}
elseif ($highSeverityMatches -gt 0) {
    Write-Host "`n[!!!] CRITICO: Hallazgos en codigo ejecutable!" -ForegroundColor Red
    Write-Host "Revisa la Seccion 2.1 del reporte INMEDIATAMENTE.`n" -ForegroundColor Red
}
elseif ($mediumSeverityMatches -gt 0) {
    Write-Host "`n[!] ATENCION: Hallazgos en scripts" -ForegroundColor Yellow
    Write-Host "Revisa la Seccion 2.2 del reporte.`n" -ForegroundColor Yellow
}
elseif ($lowSeverityMatches -gt 0) {
    Write-Host "`n[i] INFO: Hallazgos solo en documentacion" -ForegroundColor Gray
    Write-Host "Revisa la Seccion 2.3 cuando puedas.`n" -ForegroundColor Gray
}
elseif ($realMatches -eq 0) {
    Write-Host "`n[OK] Tu codigo parece estar limpio!" -ForegroundColor Green
    Write-Host "Los hallazgos del honeypot son esperados - trampas falsas.`n" -ForegroundColor Gray
}
else {
    Write-Host "`n[!] ATENCION: Revisa el reporte completo" -ForegroundColor Yellow
    Write-Host "Hay $realMatches hallazgos que requieren revision.`n" -ForegroundColor Yellow
}
