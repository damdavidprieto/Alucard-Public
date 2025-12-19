# Script de Auditoría de Secretos y Datos Sensibles
# Fecha: 2025-12-19
# Propósito: Identificar datos sensibles antes de hacer el repo público

param(
    [string]$Path = "c:\test\Alucard",
    [string]$OutputFile = "c:\test\Alucard\audit_results.txt"
)

Write-Host "`n=== AUDITORIA DE DATOS SENSIBLES ===" -ForegroundColor Cyan
Write-Host "Analizando: $Path" -ForegroundColor Yellow
Write-Host ""

$results = @()
$results += "AUDITORIA DE DATOS SENSIBLES - Alucard"
$results += "Fecha: $(Get-Date -Format 'yyyy-MM-dd HH:mm:ss')"
$results += "=" * 80
$results += ""

# Patrones a buscar
$patterns = @{
    "1. CREDENCIALES Y SECRETOS" = @(
        "password\s*=",
        "passwd\s*=",
        "pwd\s*=",
        "api_key\s*=",
        "apikey\s*=",
        "secret\s*=",
        "token\s*=",
        "auth\s*="
    )
    "2. IPS PRIVADAS"            = @(
        "\b192\.168\.\d{1,3}\.\d{1,3}\b",
        "\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b",
        "\b172\.(1[6-9]|2[0-9]|3[0-1])\.\d{1,3}\.\d{1,3}\b"
    )
    "3. DIRECCIONES MAC"         = @(
        "([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})"
    )
    "4. EMAILS"                  = @(
        "\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"
    )
    "5. NOMBRES DE USUARIO"      = @(
        "Usuario",
        "DESKTOP-",
        "PC-"
    )
}

$totalMatches = 0

foreach ($category in $patterns.Keys | Sort-Object) {
    Write-Host "Buscando: $category..." -ForegroundColor Yellow
    $results += ""
    $results += "=" * 80
    $results += $category
    $results += "=" * 80
    
    $categoryMatches = 0
    
    foreach ($pattern in $patterns[$category]) {
        try {
            $matches = Select-String -Path "$Path\*" -Pattern $pattern -Recurse -ErrorAction SilentlyContinue |
            Where-Object { $_.Path -notmatch '\\\.git\\' -and 
                $_.Path -notmatch '\\node_modules\\' -and
                $_.Path -notmatch 'audit_results\.txt' }
            
            if ($matches) {
                $categoryMatches += $matches.Count
                $results += ""
                $results += "Patrón: $pattern"
                $results += "-" * 80
                
                foreach ($match in $matches) {
                    $relativePath = $match.Path.Replace($Path, ".")
                    $results += "${relativePath}:$($match.LineNumber)"
                    $results += "  >> $($match.Line.Trim())"
                }
            }
        }
        catch {
            Write-Host "  Error buscando patrón: $pattern" -ForegroundColor Red
        }
    }
    
    if ($categoryMatches -eq 0) {
        $results += ""
        $results += "[OK] No se encontraron coincidencias"
    }
    else {
        $results += ""
        $results += "[!] Total de coincidencias: $categoryMatches"
        $totalMatches += $categoryMatches
    }
}

# Resumen final
$results += ""
$results += "=" * 80
$results += "RESUMEN FINAL"
$results += "=" * 80
$results += ""
$results += "Total de coincidencias encontradas: $totalMatches"
$results += ""

if ($totalMatches -eq 0) {
    $results += "[OK] No se encontraron datos sensibles"
    Write-Host "`n[OK] No se encontraron datos sensibles" -ForegroundColor Green
}
else {
    $results += "[!] ATENCION: Se encontraron $totalMatches coincidencias que requieren revision"
    Write-Host "`n[!] ATENCION: Se encontraron $totalMatches coincidencias" -ForegroundColor Red
}

$results += ""
$results += "Proximos pasos:"
$results += "1. Revisar manualmente cada coincidencia"
$results += "2. Sanitizar datos sensibles"
$results += "3. Crear archivos de ejemplo con datos ficticios"
$results += "4. Actualizar .gitignore"
$results += ""

# Guardar resultados
$results | Out-File $OutputFile -Encoding UTF8
Write-Host "`nResultados guardados en: $OutputFile" -ForegroundColor Cyan
Write-Host "Revisa el archivo para ver los detalles completos.`n" -ForegroundColor Yellow
