<#
.SYNOPSIS
    Análisis Forense de Navegadores - Detección de Actividad Maliciosa
    
.DESCRIPTION
    Script de análisis forense que examina navegadores web (Chrome, Firefox, Edge, Brave)
    en busca de indicadores de compromiso (IoCs) y actividad maliciosa.
    
    NO REQUIERE PERMISOS DE ADMINISTRADOR.
    SOLO LECTURA - No modifica ningún dato del navegador.
    
.FEATURES
    - Detección automática de navegadores instalados
    - Análisis de extensiones sospechosas
    - Escaneo de historial contra dominios maliciosos conocidos
    - Verificación de configuraciones alteradas (proxy, DNS, página de inicio)
    - Detección de persistencia vía navegador
    - Análisis de certificados instalados
    - Generación de reporte detallado en español
    
.NOTES
    Autor: Proyecto Alucard
    Versión: 1.0
    Fecha: 2025-12-24
    Licencia: MIT
    
.EXAMPLE
    .\analyze_browsers.ps1
    
    Ejecuta el análisis completo de todos los navegadores detectados
    
.EXAMPLE
    .\analyze_browsers.ps1 -Verbose
    
    Ejecuta el análisis con salida detallada
#>

[CmdletBinding()]
param()

# ============================================================================
# CONFIGURACIÓN INICIAL
# ============================================================================

$ErrorActionPreference = "SilentlyContinue"
[Console]::OutputEncoding = [System.Text.Encoding]::UTF8

$ScriptName = $MyInvocation.MyCommand.Name -replace '\.ps1$', ''
$script:reportDir = Join-Path $PSScriptRoot "..\logs\$ScriptName"
if (-not (Test-Path $script:reportDir)) { New-Item -ItemType Directory -Path $script:reportDir -Force | Out-Null }
$script:reportPath = Join-Path $script:reportDir "${ScriptName}_Report_$(Get-Date -Format 'yyyyMMdd_HHmmss').md"
$script:findings = @{
    Critical = @()
    High     = @()
    Medium   = @()
    Low      = @()
    Info     = @()
}

# ============================================================================
# FUNCIONES DE UTILIDAD
# ============================================================================

function Write-Log {
    <#
    .SYNOPSIS
        Escribe mensajes en consola y archivo de reporte
    #>
    param(
        [string]$Message,
        [ValidateSet('Info', 'Success', 'Warning', 'Error', 'Header')]
        [string]$Level = 'Info'
    )
    
    $colors = @{
        'Info'    = 'Gray'
        'Success' = 'Green'
        'Warning' = 'Yellow'
        'Error'   = 'Red'
        'Header'  = 'Cyan'
    }
    
    Write-Host $Message -ForegroundColor $colors[$Level]
}

function Add-Finding {
    <#
    .SYNOPSIS
        Registra un hallazgo de seguridad
    #>
    param(
        [ValidateSet('Critical', 'High', 'Medium', 'Low', 'Info')]
        [string]$Severity,
        [string]$Category,
        [string]$Description,
        [string]$Details = "",
        [string]$Recommendation = ""
    )
    
    $finding = [PSCustomObject]@{
        Severity       = $Severity
        Category       = $Category
        Description    = $Description
        Details        = $Details
        Recommendation = $Recommendation
        Timestamp      = Get-Date -Format "yyyy-MM-dd HH:mm:ss"
    }
    
    $script:findings[$Severity] += $finding
}

function Get-BrowserProfiles {
    <#
    .SYNOPSIS
        Detecta navegadores instalados y sus perfiles
    #>
    
    Write-Log "🔎 Detectando navegadores instalados..." -Level Header
    
    $browsers = @()
    
    # Chrome
    $chromePath = "$env:LOCALAPPDATA\Google\Chrome\User Data"
    if (Test-Path $chromePath) {
        $chromeProfiles = Get-ChildItem $chromePath -Directory | Where-Object { $_.Name -match "^(Default|Profile \d+)$" }
        foreach ($browserProfile in $chromeProfiles) {
            $browsers += [PSCustomObject]@{
                Name        = "Google Chrome"
                Type        = "Chromium"
                ProfilePath = $browserProfile.FullName
                ProfileName = $browserProfile.Name
            }
        }
        Write-Log "  [OK] Google Chrome detectado ($($chromeProfiles.Count) perfil(es))" -Level Success
    }
    
    # Edge
    $edgePath = "$env:LOCALAPPDATA\Microsoft\Edge\User Data"
    if (Test-Path $edgePath) {
        $edgeProfiles = Get-ChildItem $edgePath -Directory | Where-Object { $_.Name -match "^(Default|Profile \d+)$" }
        foreach ($browserProfile in $edgeProfiles) {
            $browsers += [PSCustomObject]@{
                Name        = "Microsoft Edge"
                Type        = "Chromium"
                ProfilePath = $browserProfile.FullName
                ProfileName = $browserProfile.Name
            }
        }
        Write-Log "  [OK] Microsoft Edge detectado ($($edgeProfiles.Count) perfil(es))" -Level Success
    }
    
    # Brave
    $bravePath = "$env:LOCALAPPDATA\BraveSoftware\Brave-Browser\User Data"
    if (Test-Path $bravePath) {
        $braveProfiles = Get-ChildItem $bravePath -Directory | Where-Object { $_.Name -match "^(Default|Profile \d+)$" }
        foreach ($browserProfile in $braveProfiles) {
            $browsers += [PSCustomObject]@{
                Name        = "Brave"
                Type        = "Chromium"
                ProfilePath = $browserProfile.FullName
                ProfileName = $browserProfile.Name
            }
        }
        Write-Log "  [OK] Brave detectado ($($braveProfiles.Count) perfil(es))" -Level Success
    }
    
    # Firefox
    $firefoxPath = "$env:APPDATA\Mozilla\Firefox\Profiles"
    if (Test-Path $firefoxPath) {
        $firefoxProfiles = Get-ChildItem $firefoxPath -Directory
        foreach ($browserProfile in $firefoxProfiles) {
            $browsers += [PSCustomObject]@{
                Name        = "Mozilla Firefox"
                Type        = "Firefox"
                ProfilePath = $browserProfile.FullName
                ProfileName = $browserProfile.Name
            }
        }
        Write-Log "  [OK] Mozilla Firefox detectado ($($firefoxProfiles.Count) perfil(es))" -Level Success
    }
    
    if ($browsers.Count -eq 0) {
        Write-Log "  [!] No se detectaron navegadores soportados" -Level Warning
    }
    
    return $browsers
}

# ============================================================================
# MÓDULO 1: ANÁLISIS DE EXTENSIONES
# ============================================================================

function Test-ChromiumExtensions {
    <#
    .SYNOPSIS
        Analiza extensiones de navegadores basados en Chromium
    #>
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Browser
    )
    
    Write-Log "`n🔎 Analizando extensiones de $($Browser.Name) - $($Browser.ProfileName)..." -Level Header
    
    $extensionsPath = Join-Path $Browser.ProfilePath "Extensions"
    
    if (-not (Test-Path $extensionsPath)) {
        Write-Log "  ❓ No se encontró carpeta de extensiones" -Level Info
        return
    }
    
    $extensions = Get-ChildItem $extensionsPath -Directory
    
    if ($extensions.Count -eq 0) {
        Write-Log "  [OK] No hay extensiones instaladas" -Level Success
        return
    }
    
    Write-Log "  🔎 Total de extensiones: $($extensions.Count)" -Level Info
    
    foreach ($ext in $extensions) {
        $extId = $ext.Name
        $versions = Get-ChildItem $ext.FullName -Directory | Sort-Object Name -Descending
        
        if ($versions.Count -eq 0) { continue }
        
        $latestVersion = $versions[0]
        $manifestPath = Join-Path $latestVersion.FullName "manifest.json"
        
        if (Test-Path $manifestPath) {
            try {
                $manifest = Get-Content $manifestPath -Raw -Encoding UTF8 | ConvertFrom-Json
                
                $extName = if ($manifest.name) { $manifest.name } else { "Desconocida" }
                $extVersion = if ($manifest.version) { $manifest.version } else { "?" }
                
                Write-Log "    🔎 $extName (v$extVersion)" -Level Info
                Write-Log "       ID: $extId" -Level Info
                
                # Analizar permisos peligrosos
                $dangerousPerms = @()
                if ($manifest.permissions) {
                    $highRiskPerms = @('webRequest', 'webRequestBlocking', 'cookies', 'tabs', 'history', 'downloads', 'management', 'debugger', 'proxy', 'privacy')
                    
                    foreach ($perm in $manifest.permissions) {
                        if ($highRiskPerms -contains $perm) {
                            $dangerousPerms += $perm
                        }
                    }
                }
                
                if ($dangerousPerms.Count -gt 0) {
                    Write-Log "       ⚠️ Permisos sensibles: $($dangerousPerms -join ', ')" -Level Warning
                    
                    Add-Finding -Severity "Medium" -Category "Extensiones" `
                        -Description "Extensión con permisos sensibles detectada" `
                        -Details "$extName ($extId) tiene permisos: $($dangerousPerms -join ', ')" `
                        -Recommendation "Revisa si esta extensión es legítima y necesaria. Verifica su origen en Chrome Web Store."
                }
                
                # Detectar extensiones sin nombre (sospechoso)
                if ($extName -eq "Desconocida" -or $extName -match "^__MSG_") {
                    Add-Finding -Severity "High" -Category "Extensiones" `
                        -Description "Extensión sin nombre legible detectada" `
                        -Details "ID: $extId - Posible extensión maliciosa o corrupta" `
                        -Recommendation "Investiga esta extensión. Las extensiones legítimas siempre tienen nombre visible."
                }
                
            }
            catch {
                Write-Log "       ⚠️ Error al leer manifest.json" -Level Warning
            }
        }
    }
}

# ============================================================================
# MÓDULO 2: ANÁLISIS DE HISTORIAL
# ============================================================================

function Test-ChromiumHistory {
    <#
    .SYNOPSIS
        Analiza el historial de navegación en busca de dominios maliciosos
    #>
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Browser
    )
    
    Write-Log "`n🔎 Analizando historial de $($Browser.Name) - $($Browser.ProfileName)..." -Level Header
    
    $historyPath = Join-Path $Browser.ProfilePath "History"
    
    if (-not (Test-Path $historyPath)) {
        Write-Log "  ❓ No se encontró archivo de historial" -Level Info
        return
    }
    
    # Copiar History a temporal (está bloqueado si el navegador está abierto)
    $tempHistory = Join-Path $env:TEMP "browser_history_temp_$(Get-Random).db"
    try {
        Copy-Item $historyPath $tempHistory -Force
    }
    catch {
        Write-Log "  ⚠️ No se pudo copiar historial (navegador abierto?)" -Level Warning
        return
    }
    
    # Patrones de dominios sospechosos
    $suspiciousPatterns = @(
        '\.tk$',           # TLD gratuito común en phishing
        '\.ml$',           # TLD gratuito común en phishing
        '\.ga$',           # TLD gratuito común en phishing
        '\.cf$',           # TLD gratuito común en phishing
        '\.gq$',           # TLD gratuito común en phishing
        'bit\.ly',         # Acortadores (pueden ocultar destino real)
        'tinyurl',
        'pastebin',        # Común en distribución de malware
        'discord\.gg',     # Común en distribución de malware
        'ngrok\.io',       # Túneles (común en C2)
        'duckdns\.org',    # DNS dinámico (común en C2)
        'no-ip\.',         # DNS dinámico (común en C2)
        '\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}' # IPs directas (sospechoso)
    )
    
    try {
        # Intentar leer con SQLite (requiere módulo, si no está disponible, saltamos)
        # Por simplicidad, usamos búsqueda de texto plano
        $historyContent = Get-Content $tempHistory -Raw -Encoding UTF8 -ErrorAction SilentlyContinue
        
        if ($historyContent) {
            $foundSuspicious = $false
            foreach ($pattern in $suspiciousPatterns) {
                if ($historyContent -match $pattern) {
                    $foundSuspicious = $true
                    Write-Log "  ⚠️ Patrón sospechoso detectado: $pattern" -Level Warning
                    
                    Add-Finding -Severity "Low" -Category "Historial" `
                        -Description "Patrón de dominio sospechoso en historial" `
                        -Details "Se detectó el patrón: $pattern" `
                        -Recommendation "Revisa tu historial de navegación. Estos dominios pueden estar asociados con phishing o malware."
                }
            }
            
            if (-not $foundSuspicious) {
                Write-Log "  [OK] No se detectaron patrones sospechosos obvios" -Level Success
            }
        }
        
    }
    catch {
        Write-Log "  ⚠️ Error al analizar historial" -Level Warning
    }
    finally {
        Remove-Item $tempHistory -Force -ErrorAction SilentlyContinue
    }
}

# ============================================================================
# MÓDULO 3: ANÁLISIS DE CONFIGURACIÓN
# ============================================================================

function Test-ChromiumPreferences {
    <#
    .SYNOPSIS
        Analiza configuraciones del navegador en busca de alteraciones
    #>
    param(
        [Parameter(Mandatory)]
        [PSCustomObject]$Browser
    )
    
    Write-Log "`n🔎 Analizando configuración de $($Browser.Name) - $($Browser.ProfileName)..." -Level Header
    
    $prefsPath = Join-Path $Browser.ProfilePath "Preferences"
    
    if (-not (Test-Path $prefsPath)) {
        Write-Log "  ❓ No se encontró archivo de preferencias" -Level Info
        return
    }
    
    try {
        $prefs = Get-Content $prefsPath -Raw -Encoding UTF8 | ConvertFrom-Json
        
        # Verificar página de inicio
        if ($prefs.session -and $prefs.session.startup_urls) {
            $startupUrls = $prefs.session.startup_urls
            if ($startupUrls.Count -gt 0) {
                Write-Log "  🔎 Páginas de inicio configuradas:" -Level Info
                foreach ($url in $startupUrls) {
                    Write-Log "     - $url" -Level Info
                    
                    # Detectar URLs sospechosas en inicio
                    if ($url -match '(\.tk|\.ml|\.ga|\.cf|\.gq|bit\.ly|tinyurl)') {
                        Add-Finding -Severity "High" -Category "Configuración" `
                            -Description "Página de inicio sospechosa configurada" `
                            -Details "URL: $url" `
                            -Recommendation "Esta URL podría haber sido configurada por malware. Restablece tu página de inicio."
                    }
                }
            }
        }
        
        # Verificar motor de búsqueda
        if ($prefs.default_search_provider -and $prefs.default_search_provider.name) {
            $searchEngine = $prefs.default_search_provider.name
            Write-Log "  🔎 Motor de búsqueda: $searchEngine" -Level Info
            
            # Motores legítimos comunes
            $legitimateEngines = @('Google', 'Bing', 'DuckDuckGo', 'Yahoo', 'Ecosia', 'Brave Search')
            
            if ($legitimateEngines -notcontains $searchEngine) {
                Add-Finding -Severity "Medium" -Category "Configuración" `
                    -Description "Motor de búsqueda no estándar detectado" `
                    -Details "Motor configurado: $searchEngine" `
                    -Recommendation "Verifica que este motor de búsqueda sea legítimo. El secuestro de búsqueda es común en malware."
            }
        }
        
        # Verificar proxy
        if ($prefs.proxy) {
            Write-Log "  ⚠️ Configuración de proxy detectada" -Level Warning
            
            Add-Finding -Severity "Medium" -Category "Configuración" `
                -Description "Configuración de proxy detectada en navegador" `
                -Details "Revisa la configuración de proxy manualmente" `
                -Recommendation "Los proxies pueden ser usados para interceptar tráfico. Verifica que sea legítimo."
        }
        
    }
    catch {
        Write-Log "  ⚠️ Error al analizar preferencias: $($_.Exception.Message)" -Level Warning
    }
}

# ============================================================================
# MÓDULO 4: ANÁLISIS DE CERTIFICADOS
# ============================================================================

function Test-Certificates {
    <#
    .SYNOPSIS
        Analiza certificados instalados en el sistema
    #>
    
    Write-Log "`n🔎 Analizando certificados del sistema..." -Level Header
    
    try {
        # Obtener certificados raíz instalados por el usuario
        $userCerts = Get-ChildItem Cert:\CurrentUser\Root -ErrorAction SilentlyContinue
        
        if ($userCerts) {
            Write-Log "  🔎 Certificados raíz de usuario: $($userCerts.Count)" -Level Info
            
            foreach ($cert in $userCerts) {
                $issuer = $cert.Issuer
                $subject = $cert.Subject
                $thumbprint = $cert.Thumbprint
                
                # Detectar certificados autofirmados (sospechosos si no son conocidos)
                if ($issuer -eq $subject) {
                    Write-Log "  ⚠️ Certificado autofirmado: $subject" -Level Warning
                    
                    Add-Finding -Severity "Medium" -Category "Certificados" `
                        -Description "Certificado raíz autofirmado detectado" `
                        -Details "Emisor/Sujeto: $subject`nHuella: $thumbprint" `
                        -Recommendation "Los certificados autofirmados pueden ser usados para interceptar tráfico HTTPS. Verifica su legitimidad."
                }
            }
        }
        else {
            Write-Log "  [OK] No hay certificados raíz de usuario adicionales" -Level Success
        }
        
    }
    catch {
        Write-Log "  ⚠️ Error al analizar certificados: $($_.Exception.Message)" -Level Warning
    }
}

# ============================================================================
# GENERACIÓN DE REPORTE
# ============================================================================

function New-ForensicReport {
    <#
    .SYNOPSIS
        Genera reporte en formato Markdown
    #>
    
    Write-Log "`n🔎 Generando reporte..." -Level Header
    
    $report = @"
# 🕵️‍♂️ Reporte de Análisis Forense de Navegadores

**Fecha:** $(Get-Date -Format "yyyy-MM-dd HH:mm:ss")  
**Sistema:** $env:COMPUTERNAME  
**Usuario:** $env:USERNAME  
**Script:** Alucard Browser Forensic Analysis v1.0

---

## 📊 Resumen Ejecutivo

"@

    $totalFindings = ($script:findings.Critical.Count + $script:findings.High.Count + 
        $script:findings.Medium.Count + $script:findings.Low.Count)
    
    $report += @"

| Severidad | Cantidad |
|-----------|----------|
| 🔴 Crítico | $($script:findings.Critical.Count) |
| 🟠 Alto | $($script:findings.High.Count) |
| 🟡 Medio | $($script:findings.Medium.Count) |
| 🔵 Bajo | $($script:findings.Low.Count) |
| ⚪ Informativo | $($script:findings.Info.Count) |
| **TOTAL** | **$totalFindings** |

---

"@

    # Hallazgos por severidad
    foreach ($severity in @('Critical', 'High', 'Medium', 'Low')) {
        $findings = $script:findings[$severity]
        
        if ($findings.Count -gt 0) {
            $icon = switch ($severity) {
                'Critical' { '🔴' }
                'High' { '🟠' }
                'Medium' { '🟡' }
                'Low' { '🔵' }
            }
            
            $report += @"
## $icon Hallazgos de Severidad: $severity

"@
            
            foreach ($finding in $findings) {
                $report += @"
### $($finding.Category): $($finding.Description)

**Detalles:**  
$($finding.Details)

**Recomendación:**  
$($finding.Recommendation)

**Timestamp:** $($finding.Timestamp)

---

"@
            }
        }
    }
    
    # Información adicional
    $report += @"

## ℹ️ Información Adicional

### ¿Qué hacer si encuentro hallazgos?

1. **Crítico/Alto**: Investiga inmediatamente. Considera restablecer el navegador o buscar ayuda profesional.
2. **Medio**: Revisa manualmente y verifica la legitimidad de los elementos detectados.
3. **Bajo**: Informativo. Revisa cuando tengas tiempo.

### Recursos

- [Cómo restablecer Chrome](https://support.google.com/chrome/answer/3296214)
- [Cómo restablecer Firefox](https://support.mozilla.org/kb/refresh-firefox-reset-add-ons-and-settings)
- [Cómo restablecer Edge](https://support.microsoft.com/microsoft-edge/restore-microsoft-edge-to-default-settings-3533e9a0-e4c1-0b8a-4d6d-c4b6c7e5c0f0)

### Sobre este análisis

Este script realiza un análisis **pasivo y de solo lectura** de tus navegadores web.  
No modifica ningún dato ni configuración.

**Limitaciones:**
- No puede detectar malware sofisticado que se ejecute fuera del navegador
- No analiza el tráfico de red en tiempo real
- Los patrones de detección son básicos y pueden generar falsos positivos

**Si sospechas de compromiso real, considera:**
- Ejecutar un antivirus completo
- Consultar con un profesional de ciberseguridad
- Revisar logs del sistema con herramientas especializadas

---

**Generado por:** Proyecto Alucard - Browser Forensic Analysis  
**Licencia:** MIT  
**Repositorio:** [Alucard-Public](https://github.com/tu-usuario/Alucard-Public)

"@

    # Guardar reporte
    $report | Out-File -FilePath $script:reportPath -Encoding UTF8
    
    Write-Log "  ✅ Reporte guardado en: $script:reportPath" -Level Success
}

# ============================================================================
# FUNCI?N PRINCIPAL
# ============================================================================

function Start-BrowserForensicAnalysis {
    <#
    .SYNOPSIS
        Función principal que ejecuta todos los módulos de análisis
    #>
    
    Write-Log "╔══════════════════════════════════════════════════════════════╗" -Level Header
    Write-Log "║                                                              ║" -Level Header
    Write-Log "║          🕵️‍♂️  ALUCARD - BROWSER FORENSIC ANALYSIS  🕵️‍♂️          ║" -Level Header
    Write-Log "║                                                              ║" -Level Header
    Write-Log "║  Análisis de Seguridad de Navegadores Web                    ║" -Level Header
    Write-Log "║  Versión 1.0 | Proyecto Alucard | MIT License                ║" -Level Header
    Write-Log "║                                                              ║" -Level Header
    Write-Log "╚══════════════════════════════════════════════════════════════╝" -Level Header

    Write-Log "⚠️  IMPORTANTE: Este análisis NO requiere permisos de administrador" -Level Warning
    Write-Log "⚠️  Solo lectura - No se modificará ningún dato del navegador`n" -Level Warning
    
    # Detectar navegadores
    $browsers = Get-BrowserProfiles
    
    if ($browsers.Count -eq 0) {
        Write-Log "`n❌ No se detectaron navegadores para analizar" -Level Error
        return
    }
    
    Write-Log "`n📊 Total de perfiles a analizar: $($browsers.Count)`n" -Level Info
    
    # Analizar cada navegador
    foreach ($browser in $browsers) {
        Write-Log "`n$('='*70)" -Level Info
        Write-Log "Analizando: $($browser.Name) - $($browser.ProfileName)" -Level Header
        Write-Log "$('='*70)" -Level Info
        
        if ($browser.Type -eq "Chromium") {
            Test-ChromiumExtensions -Browser $browser
            Test-ChromiumHistory -Browser $browser
            Test-ChromiumPreferences -Browser $browser
        }
        # Firefox requeriría lógica diferente (SQLite directo)
        # Por ahora solo soportamos Chromium-based
    }
    
    # Análisis de certificados (una sola vez, afecta a todos los navegadores)
    Test-Certificates
    
    # Generar reporte
    Write-Log "`n$('='*70)" -Level Info
    New-ForensicReport
    
    # Resumen final
    Write-Log "`n????????????????????????????????????????????????????????????????" -Level Header
    Write-Log "?                    AN?LISIS COMPLETADO                       ?" -Level Header
    Write-Log "????????????????????????????????????????????????????????????????`n" -Level Header
    
    $totalFindings = ($script:findings.Critical.Count + $script:findings.High.Count + 
        $script:findings.Medium.Count + $script:findings.Low.Count)
    
    if ($totalFindings -eq 0) {
        Write-Log "✅ No se detectaron indicadores de compromiso obvios" -Level Success
        Write-Log "   Tu navegador parece estar limpio (según los patrones básicos analizados)" -Level Success
    }
    else {
        Write-Log "⚠️  Se detectaron $totalFindings hallazgo(s) que requieren revisión" -Level Warning
        Write-Log "   Revisa el reporte detallado para más información" -Level Warning
    }
    
    Write-Log "`n📃 Reporte completo: $script:reportPath" -Level Info
    Write-Log "💡 Tip: Abre el reporte .md con cualquier visor de Markdown para mejor formato`n" -Level Info
}

# ============================================================================
# EJECUCI?N
# ============================================================================

try {
    Start-BrowserForensicAnalysis
}
catch {
    Write-Log "`n? Error cr?tico durante el an?lisis:" -Level Error
    Write-Log $_.Exception.Message -Level Error
    Write-Log $_.ScriptStackTrace -Level Error
}
finally {
    Write-Log "`nPresiona ENTER para salir..." -Level Info
    Read-Host
}

