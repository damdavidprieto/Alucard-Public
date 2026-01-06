# Plan de Blindaje del Sistema

## Objetivo

Implementar un hardening completo del sistema para:
1. **Eliminar vectores de ataque externos** - Cerrar todos los puertos y servicios vulnerables
2. **Prevenir control remoto** - Bloquear mecanismos de acceso no autorizado
3. **Filtrar tráfico** - Implementar whitelist de aplicaciones y bloqueo de tráfico sospechoso
4. **Máxima seguridad** - Configuración "cerrada por defecto, abierta por excepción"

## Filosofía de Hardening

> **"Deny by Default, Allow by Exception"**
> 
> Todo bloqueado por defecto. Solo se permite lo estrictamente necesario.

---

## Fase 1: Protección Antivirus (CRÍTICO)

### 1.1 Habilitar Windows Defender

```powershell
# Habilitar todas las protecciones
Set-MpPreference -DisableRealtimeMonitoring $false
Set-MpPreference -DisableBehaviorMonitoring $false
Set-MpPreference -DisableIOAVProtection $false
Set-MpPreference -DisableScriptScanning $false

# Actualizar firmas
Update-MpSignature

# Habilitar protección de red
Set-MpPreference -EnableNetworkProtection Enabled

# Habilitar protección contra exploits
Set-ProcessMitigation -System -Enable DEP,SEHOP,ForceRelocateImages
```

**Impacto:** Protección activa contra malware, ransomware, y exploits.

---

## Fase 2: Cierre de Puertos Críticos

### 2.1 Bloquear SMB (Puerto 445)

```powershell
# Bloquear SMB entrante
New-NetFirewallRule -DisplayName "Block SMB Inbound" `
    -Direction Inbound -Protocol TCP -LocalPort 445 -Action Block -Profile Any

# Bloquear SMB saliente (opcional, más restrictivo)
New-NetFirewallRule -DisplayName "Block SMB Outbound" `
    -Direction Outbound -Protocol TCP -RemotePort 445 -Action Block -Profile Any
```

### 2.2 Bloquear RPC (Puerto 135)

```powershell
New-NetFirewallRule -DisplayName "Block RPC Inbound" `
    -Direction Inbound -Protocol TCP -LocalPort 135 -Action Block -Profile Any
```

### 2.3 Bloquear NetBIOS (Puerto 139)

```powershell
New-NetFirewallRule -DisplayName "Block NetBIOS Inbound" `
    -Direction Inbound -Protocol TCP -LocalPort 139 -Action Block -Profile Any
```

### 2.4 Bloquear RDP (Puerto 3389)

```powershell
New-NetFirewallRule -DisplayName "Block RDP Inbound" `
    -Direction Inbound -Protocol TCP -LocalPort 3389 -Action Block -Profile Any
```

### 2.5 Bloquear Puertos de Rango Alto Dinámicos

```powershell
# Bloquear rango de puertos dinámicos comunes en botnets
New-NetFirewallRule -DisplayName "Block High Ports Inbound" `
    -Direction Inbound -Protocol TCP -LocalPort 49152-65535 -Action Block -Profile Public
```

**Impacto:** Elimina vectores de ataque de ransomware, RCE, y acceso remoto no autorizado.

---

## Fase 3: Deshabilitar Servicios Vulnerables

### 3.1 Deshabilitar SMB v1 (Vulnerable)

```powershell
# Deshabilitar SMB v1 completamente
Disable-WindowsOptionalFeature -Online -FeatureName SMB1Protocol -NoRestart
```

### 3.2 Deshabilitar Recursos Compartidos Administrativos

```powershell
# Deshabilitar ADMIN$, C$, IPC$
Set-ItemProperty -Path "HKLM:\SYSTEM\CurrentControlSet\Services\LanmanServer\Parameters" `
    -Name "AutoShareWks" -Value 0

# Requiere reinicio para aplicar
```

### 3.3 Deshabilitar Remote Registry

```powershell
Stop-Service -Name "RemoteRegistry" -Force
Set-Service -Name "RemoteRegistry" -StartupType Disabled
```

### 3.4 Deshabilitar Servicios Innecesarios

```powershell
# Lista de servicios a deshabilitar (si no los usas)
$servicesToDisable = @(
    "RemoteRegistry",
    "RemoteAccess",
    "Telephony",
    "Fax",
    "WMPNetworkSvc"  # Windows Media Player Network Sharing
)

foreach ($service in $servicesToDisable) {
    try {
        Stop-Service -Name $service -Force -ErrorAction SilentlyContinue
        Set-Service -Name $service -StartupType Disabled -ErrorAction SilentlyContinue
    } catch {
        Write-Host "Service $service not found or already disabled"
    }
}
```

**Impacto:** Reduce superficie de ataque eliminando servicios no utilizados.

---

## Fase 4: Hardening de Firewall

### 4.1 Configurar Política de Firewall Estricta

```powershell
# Bloquear TODO el tráfico entrante por defecto
Set-NetFirewallProfile -Profile Domain,Public,Private -DefaultInboundAction Block

# Permitir solo tráfico saliente necesario
Set-NetFirewallProfile -Profile Domain,Public,Private -DefaultOutboundAction Allow

# Habilitar firewall en todos los perfiles
Set-NetFirewallProfile -Profile Domain,Public,Private -Enabled True
```

### 4.2 Habilitar Logging Completo

```powershell
# Habilitar logging de conexiones bloqueadas y permitidas
Set-NetFirewallProfile -All -LogBlocked True -LogAllowed True

# Configurar tamaño de log
Set-NetFirewallProfile -All -LogMaxSizeKilobytes 16384  # 16 MB
```

### 4.3 Bloquear Conexiones de Aplicaciones No Autorizadas

```powershell
# Deshabilitar reglas predeterminadas permisivas
Get-NetFirewallRule | Where-Object {
    $_.Direction -eq "Inbound" -and 
    $_.Action -eq "Allow" -and 
    $_.Enabled -eq $true
} | Disable-NetFirewallRule
```

**Advertencia:** Esto puede romper conectividad. Solo aplicar si sabes qué reglas necesitas.

---

## Fase 5: Filtrado de Tráfico Avanzado

### 5.1 Configurar DNS Seguro

```powershell
# Usar Cloudflare DNS (con filtrado de malware)
Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("1.1.1.2","1.0.0.2")

# O usar Google DNS
# Set-DnsClientServerAddress -InterfaceAlias "Ethernet" -ServerAddresses ("8.8.8.8","8.8.4.4")
```

### 5.2 Bloquear Rangos de IPs Sospechosas

```powershell
# Bloquear rangos de IPs conocidos por C&C, botnets, etc.
# Ejemplo: Bloquear redes Tor (opcional)
New-NetFirewallRule -DisplayName "Block Tor Network" `
    -Direction Outbound -RemoteAddress @("185.220.100.0/22","185.220.101.0/24") -Action Block
```

### 5.3 Implementar Whitelist de Aplicaciones (Opcional)

```powershell
# Permitir solo aplicaciones específicas en el firewall
# Ejemplo: Permitir Chrome
New-NetFirewallRule -DisplayName "Allow Chrome" `
    -Direction Outbound -Program "C:\Program Files\Google\Chrome\Application\chrome.exe" -Action Allow
```

### 5.4 Bloquear Protocolos Inseguros

```powershell
# Bloquear Telnet (puerto 23)
New-NetFirewallRule -DisplayName "Block Telnet" `
    -Direction Inbound -Protocol TCP -LocalPort 23 -Action Block

# Bloquear FTP (puerto 21)
New-NetFirewallRule -DisplayName "Block FTP" `
    -Direction Inbound -Protocol TCP -LocalPort 21 -Action Block
```

---

## Fase 6: Auditoría y Monitoreo

### 6.1 Habilitar Auditoría de Eventos de Seguridad

```powershell
# Auditoría de logon/logoff
auditpol /set /subcategory:"Logon" /success:enable /failure:enable
auditpol /set /subcategory:"Logoff" /success:enable

# Auditoría de acceso a objetos
auditpol /set /subcategory:"File Share" /success:enable /failure:enable

# Auditoría de cambios de políticas
auditpol /set /subcategory:"Audit Policy Change" /success:enable /failure:enable

# Auditoría de procesos
auditpol /set /subcategory:"Process Creation" /success:enable
```

### 6.2 Habilitar Auditoría de SMB

```powershell
Set-SmbServerConfiguration -AuditSmb1Access $true -Force
```

### 6.3 Configurar Retención de Logs

```powershell
# Aumentar tamaño de Event Logs
wevtutil sl Security /ms:1048576000  # 1 GB
wevtutil sl System /ms:524288000     # 512 MB
wevtutil sl Application /ms:524288000 # 512 MB
```

---

## Fase 7: Configuraciones Adicionales de Seguridad

### 7.1 Deshabilitar PowerShell Remoting

```powershell
Disable-PSRemoting -Force
Stop-Service WinRM
Set-Service WinRM -StartupType Disabled
```

### 7.2 Deshabilitar Ejecución de Scripts No Firmados

```powershell
Set-ExecutionPolicy AllSigned -Scope LocalMachine -Force
```

### 7.3 Habilitar UAC al Máximo

```powershell
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" `
    -Name "ConsentPromptBehaviorAdmin" -Value 2

Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\System" `
    -Name "EnableLUA" -Value 1
```

### 7.4 Deshabilitar Autorun/Autoplay

```powershell
Set-ItemProperty -Path "HKLM:\SOFTWARE\Microsoft\Windows\CurrentVersion\Policies\Explorer" `
    -Name "NoDriveTypeAutoRun" -Value 255
```

---

## Plan de Verificación

### Verificación de Puertos

```powershell
# Verificar que puertos críticos estén cerrados
Get-NetTCPConnection -State Listen | Where-Object {
    $_.LocalPort -in @(445, 135, 139, 3389)
}
# Resultado esperado: Vacío o solo localhost
```

### Verificación de Firewall

```powershell
# Verificar política de firewall
Get-NetFirewallProfile | Select-Object Name, Enabled, DefaultInboundAction, DefaultOutboundAction

# Verificar reglas de bloqueo
Get-NetFirewallRule | Where-Object {
    $_.DisplayName -like "Block*" -and $_.Enabled -eq $true
}
```

### Verificación de Servicios

```powershell
# Verificar servicios deshabilitados
Get-Service | Where-Object {
    $_.Name -in @("RemoteRegistry", "RemoteAccess", "WinRM") -and $_.Status -eq "Running"
}
# Resultado esperado: Vacío
```

### Test de Conectividad Externa

```powershell
# Verificar que puertos críticos no sean accesibles desde fuera
Test-NetConnection -ComputerName portquiz.net -Port 445
# Resultado esperado: TcpTestSucceeded = False (si bloqueado saliente)
```

---

## Impacto Esperado

### Antes del Hardening
```
Puertos expuestos: 445, 135, 139, 3389, 49664+
Servicios vulnerables: SMB, RPC, NetBIOS, RDP
Windows Defender: Deshabilitado
Firewall: Permisivo
Auditoría: Mínima
```

### Después del Hardening
```
Puertos expuestos: Ninguno (o solo localhost)
Servicios vulnerables: Deshabilitados
Windows Defender: Activo y actualizado
Firewall: Deny by default
Auditoría: Completa
```

---

## Advertencias Importantes

> [!WARNING]
> **Posibles Efectos Secundarios**
> 
> - Compartición de archivos en red local dejará de funcionar
> - Escritorio remoto (RDP) no será accesible
> - Algunas aplicaciones pueden requerir reglas de firewall específicas
> - PowerShell remoting quedará deshabilitado

> [!CAUTION]
> **Antes de Aplicar**
> 
> 1. Asegúrate de tener acceso físico al equipo
> 2. Haz backup de configuración actual
> 3. Documenta aplicaciones que necesitan acceso a red
> 4. Ten un plan de rollback

---

## Orden de Ejecución Recomendado

1. ✅ **Fase 1:** Habilitar Windows Defender (sin reinicio)
2. ✅ **Fase 2:** Bloquear puertos críticos (sin reinicio)
3. ✅ **Fase 4:** Configurar firewall (sin reinicio)
4. ✅ **Fase 6:** Habilitar auditoría (sin reinicio)
5. ⚠️ **Fase 3:** Deshabilitar servicios (requiere reinicio)
6. ✅ **Fase 5:** Filtrado avanzado (sin reinicio)
7. ✅ **Fase 7:** Verificación completa

---

## Próximos Pasos

Después de implementar el hardening:
1. Configurar Metatron para monitoreo continuo
2. Establecer baseline de tráfico normal
3. Revisar logs diariamente
4. Actualizar sistema semanalmente
5. Realizar auditorías de seguridad mensuales
