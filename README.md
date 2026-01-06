# 🛡️ Alucard - Mi Viaje de Aprendizaje en Blue Team

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Status: Learning](https://img.shields.io/badge/Status-Learning-yellow.svg)]()
[![Approach: Defensive](https://img.shields.io/badge/Approach-Defensive-green.svg)]()

> **"Si he visto más lejos es porque estoy sentado sobre los hombros de gigantes."** - Isaac Newton
> **"El arte es la mentira que nos permite comprender la verdad"** - Pablo Picasso
---

## ⚠️ Aviso Importante

Este es un **proyecto de aprendizaje en desarrollo**. Documenta mi viaje desde principiante hasta (espero) competente en ciberseguridad defensiva.

### 🎯 Qué Encontrarás Aquí

- ✅ **Proceso de aprendizaje real** - Incluyendo errores y correcciones
- ✅ **Documentación honesta** - Sin ocultar los tropiezos
- ✅ **Código en evolución** - Mejorando con el tiempo
- ✅ **Lecciones aprendidas** - Para que otros no repitan mis errores
- ✅ **Transparencia total** - Todas las fuentes citadas

### ❌ Qué NO Encontrarás

- ❌ Código perfecto o production-ready
- ❌ Soluciones enterprise
- ❌ Herramientas ofensivas
- ❌ Tutoriales definitivos

---

## 📖 Empieza Aquí - Guía de Lectura

Lee los documentos en este orden para entender el proyecto:

### 1️⃣ [Léeme Primero](docs/01_Introduccion.md)
**Contexto y Agradecimientos**
- El momento de reflexión (2025-12-19)
- Por qué existe este proyecto
- Agradecimientos a la comunidad
- Filosofía de transparencia

### 2️⃣ [Diario de Aprendizaje](docs/02_Diario_Aprendizaje.md)
**Mi Viaje Día a Día**
- Entradas diarias de progreso
- Qué aprendí cada día
- Proceso de pensamiento
- Recursos que me ayudaron

### 3️⃣ [Errores y Lecciones](docs/03_Errores_Lecciones.md)
**Errores Específicos Documentados**
- Qué hice mal (con detalles)
- Por qué fue peligroso
- Cómo lo corregí
- Lecciones para otros

### 4️⃣ [Herramientas y Metodología](docs/04_Metodologia.md)
**Transparencia sobre el Desarrollo**
- Uso de Antigravity (Google Gemini)
- Código generado vs manual
- Proceso de colaboración humano-IA
- Lecciones sobre desarrollo asistido por IA

### 5️⃣ Documentación Técnica
- [Referencias y Atribuciones](docs/01_Introduccion.md)

- [Auditoría de Seguridad del Router](docs/05_Auditoria_Router_Manual.md)
- [Guía de Auditoría de Red](docs/06_Guia_Auditoria_Red.md)

---

## 🎯 Sobre el Proyecto

### ¿Qué es Alucard?

Alucard es mi ecosistema de aprendizaje en ciberseguridad defensiva (Blue Team). Incluye:

- **Scripts de Análisis** - Monitoreo pasivo de red
- **Herramientas de Auditoría** - Verificación de seguridad
- **Sistema de Logging** - Trazabilidad completa
- **Documentación** - Proceso de aprendizaje

### ¿Por Qué "Alucard"?

Porque es "Dracula" al revés - un guardián que protege en lugar de atacar. Representa el enfoque defensivo del proyecto.
Además tiene su poder totalmente restringido y solo puede ser liberado cuando se lo permiten. 
Solo sirve a Integra, la cual tiene la sangre dulce y por eso la protege. Contiene todas las almas acumuladas y cuando es necesario las usa. 
Actúa como un honeypot: evaluando al oponente, recibiendo, cambiando de forma y respondiendo cuando le dan permiso.
Nunca utiliza más poder del necesario y solo cuando es necesario. 
Aparece cuando es necesario y desaparece cuando es necesario.

### Componentes Principales

```
Alucard/
├── 📄 Documentación de Aprendizaje
│   ├── docs/01_Introduccion.md
│   ├── docs/02_Diario_Aprendizaje.md
│   ├── docs/03_Errores_Lecciones.md
│   └── docs/04_Metodologia.md
│
├── 🛠️ Scripts de Seguridad
│   ├── analyze_browsers.ps1         # Análisis forense de navegadores
│   ├── analyze_network.ps1          # Análisis pasivo de red
│   └── check_router_compromise.ps1  # Detección de compromiso
│
├── 📚 Documentación Técnica
│   ├── 01_REFERENCIAS_Y_ATRIBUCIONES.md
│   ├── 05_Auditoria_Router_Manual.md
│   ├── 06_Guia_Auditoria_Red.md
│   ├── 07_Arquitectura_Sistema.md   # Arquitectura de 3 capas
│   ├── 08_Escenarios_Ataque_Honeypot.md # Escenarios de pentesting
│   ├── 09_Manual_Codigo_Honeypot.md # Guía de aprendizaje Python
│   └── 10_Guia_Hardening.md         # Plan de blindaje del sistema
│
├── 🍯 Honeypot Educativo
│   ├── README.md                    # ⚠️ Ver disclaimers
│   ├── main.py                      # Punto de entrada
│   ├── config.py                    # Configuración
│   ├── services/                    # HTTP, SSH
│   ├── responses/                   # Endpoints y trampas
│   └── detection/                   # Detección de ataques
│
└── 📊 Logs y Reportes
    └── logs/network/
```

---

## 🚀 Características

### ✅ Implementado

- [x] Análisis pasivo de red local
- [x] Detección de indicadores de compromiso
- [x] Auditoría manual de router
- [x] Sistema de logging centralizado
- [x] Generación de reportes en Markdown
- [x] Documentación ética completa

### 🔄 En Desarrollo

- [ ] Dashboard de monitoreo (Metatron)
- [ ] Base de datos centralizada (Samael)
- [ ] Integración con SIEM
- [ ] Análisis de amenazas avanzado
- [ ] Automatización de respuestas

### 📋 Planificado

- [ ] Integración con VMs para experimentos
- [ ] Análisis de logs con ML
- [ ] Correlación de eventos
- [ ] Threat hunting automatizado

---

## 📚 Recursos Educativos

Esta sección contiene guías detalladas para aprender sobre diferentes aspectos de la ciberseguridad defensiva:

### 🏗️ [Arquitectura del Sistema](docs/07_Arquitectura_Sistema.md)
**Arquitectura de 3 Capas: Windows + Docker + Kali VM**
- Diagramas completos del sistema
- Flujo de datos entre capas
- Comparación de tecnologías
- Escenarios de uso por capa
- Recomendaciones de seguridad

### 🎯 [Escenarios de Ataque](docs/08_Escenarios_Ataque_Honeypot.md)
**Guía Práctica de Pentesting Ético**
- Reconocimiento con nmap
- Enumeración web (nikto, dirb, gobuster)
- Ataques de inyección (SQL, XSS, Command Injection)
- Fuerza bruta SSH con Hydra
- Análisis de tráfico con Wireshark
- Scripts automatizados de ataque
- ⚠️ **Solo para uso en tus propios sistemas**

### 🔍 [Guía de Auditoría de Red](docs/06_Guia_Auditoria_Red.md)
**Cómo Auditar Tu Red Doméstica**
- Opciones: DIY, Profesional, Automatizada
- Herramientas gratuitas (Fing, nmap, Wireshark)
- Auditoría de router paso a paso
- Escaneo de vulnerabilidades
- Hardening de dispositivos IoT
- Checklist completa de seguridad

### 🌐 [Análisis Forense de Navegadores](docs/11_Guia_Analisis_Navegadores.md)
**Detección de Compromiso en Navegadores Web**
- Análisis de extensiones sospechosas
- Detección de dominios maliciosos en historial
- Verificación de configuraciones alteradas
- Identificación de certificados sospechosos
- Guía de interpretación de resultados
- Sin permisos de administrador requeridos

### 🛡️ [Plan de Hardening](docs/10_Guia_Hardening.md)
**Blindaje Completo del Sistema Windows**
- Filosofía "Deny by Default"
- Cierre de puertos críticos (SMB, RPC, RDP)
- Configuración de firewall restrictivo
- Deshabilitación de servicios vulnerables
- Auditoría y monitoreo
- Scripts PowerShell listos para usar

### 🎓 [Manual Técnico de Python](docs/09_Manual_Codigo_Honeypot.md)
**Aprende Python con el Código del Honeypot**
- Sistema de módulos e imports
- Concurrencia con threading
- Programación de sockets
- Clases y herencia
- Manejo de excepciones
- Explicaciones paso a paso del código

---

## 🛠️ Tecnologías

- **PowerShell** - Scripts de análisis y monitoreo
- **Python** - Herramientas de procesamiento (futuro)
- **Markdown** - Documentación
- **Git** - Control de versiones

---

## 🙏 Inspiración y Referencias

Este proyecto no existiría sin el trabajo de la comunidad de ciberseguridad. Especialmente:

### Proyectos de Referencia

- **[U7Dani](https://github.com/U7Dani)** - Inspiración principal
  - [wazuh-kali-lab](https://github.com/U7Dani/wazuh-kali-lab) - Integración SIEM
  - [PhishScope](https://github.com/U7Dani/PhishScope) - Análisis de phishing
  - [Laboratorio-Blue-Team](https://github.com/U7Dani/Laboratorio-Blue-Team-T-Pot-Wazuh-TheHive) - Arquitectura completa

### Herramientas Open Source

- [Wazuh](https://wazuh.com/) - SIEM
- [T-Pot](https://github.com/telekom-security/tpotce) - Honeypots
- [TheHive](https://thehive-project.org/) - Incident Response

**Ver [01_REFERENCIAS_Y_ATRIBUCIONES.md](docs/01_Introduccion.md) para detalles completos.**

---

## 📚 Para Otros Aprendices

### Si Estás Empezando

**Lee primero**:
1. [Errores y Lecciones](docs/03_Errores_Lecciones.md) - Aprende de mis errores
2. [Diario de Aprendizaje](docs/02_Diario_Aprendizaje.md) - Ve el proceso real

**Consejos**:
- ✅ Usa VMs SIEMPRE para experimentar
- ✅ Documenta tu proceso desde el principio
- ✅ No tengas vergüenza de preguntar
- ✅ Cita tus fuentes
- ✅ Está bien equivocarse

### Si Eres Experto

**Agradecería**:
- 🐛 Reportar errores en mi código
- 💡 Sugerencias de mejora
- 📖 Recursos de aprendizaje
- 🤝 Feedback constructivo

**Pero recuerda**:
- Este es un proyecto de aprendizaje
- Los errores están documentados intencionalmente
- La perfección no es el objetivo

---

## 🔒 Enfoque de Seguridad

### Principios

1. **Defensivo Siempre** - Sin herramientas ofensivas
2. **Pasivo Primero** - Monitoreo sin escaneos activos
3. **Aislamiento** - Experimentos en VMs
4. **Documentación** - Trazabilidad total
5. **Ética** - Transparencia y atribución

### Seguridad de Este Repositorio

- ✅ Sin credenciales hardcodeadas
- ✅ Sin datos personales
- ✅ IPs sanitizadas (ejemplos)
- ✅ Logs sin información sensible
- ✅ Código revisado antes de publicar

---

## 📄 Licencia

Este proyecto está bajo [Licencia MIT](LICENSE).

**Importante**: 
- Puedes usar, modificar y distribuir el código
- Debes mantener el aviso de copyright
- Debes citar las fuentes originales (ver REFERENCIAS.md)

---

## 🤝 Contribuciones

### ¿Puedo Contribuir?

**¡Sí!** Especialmente si:
- Encuentras errores en la documentación
- Tienes sugerencias de mejora
- Quieres añadir recursos de aprendizaje
- Encuentras bugs en el código

### Cómo Contribuir

1. Abre un Issue describiendo la mejora/error
2. Si quieres contribuir código, haz un Fork
3. Crea un Pull Request con descripción clara
4. Sé respetuoso - este es un proyecto de aprendizaje

---

## 📞 Contacto

- **GitHub**: [Cuando sea público]
- **Documentación**: Ver archivos en `docs/`
- **Issues**: Para reportar problemas o sugerencias

---

## 🎓 Cronología del Proyecto

### 2025-12-19: Inicio y Reflexión
- ✅ Momento de reflexión sobre seguridad
- ✅ Descubrimiento de referencias (U7Dani)
- ✅ Creación de documentación ética
- ✅ Primera entrada en diario de aprendizaje
- ✅ Documentación de errores cometidos

### Próximos Hitos
- [ ] Migración completa a VMs
- [ ] Implementación de Metatron (Dashboard)
- [ ] Integración con Samael (Database)
- [ ] Primera contribución a proyecto open source

---

## 💡 Filosofía del Proyecto

### Por Qué Comparto Mis Errores

Muchos proyectos solo muestran el resultado final perfecto. Yo muestro el proceso real:
- Los errores que cometí
- Cómo me di cuenta
- Cómo los corregí
- Qué aprendí

**Porque creo que**:
- El aprendizaje real es imperfecto
- Los errores son oportunidades
- La honestidad construye comunidad
- Otros pueden aprender de mis tropiezos

### Compromiso de Transparencia

Este proyecto se compromete a:
1. **Documentar TODO** - Éxitos y fracasos
2. **Citar SIEMPRE** - Todas las fuentes
3. **Ser HONESTO** - Sobre nivel de experiencia
4. **Compartir GENEROSAMENTE** - Para ayudar a otros

---

## 🌟 Agradecimientos Especiales

A todos los que comparten conocimiento en la comunidad de ciberseguridad:
- Por hacer el aprendizaje accesible
- Por no juzgar a los principiantes
- Por documentar su trabajo
- Por inspirar a otros

**Especialmente a U7Dani** por proyectos que no solo enseñan técnicas, sino también cómo compartir conocimiento de forma generosa.

---

## 📊 Estado del Proyecto

| Aspecto | Estado |
|---------|--------|
| Documentación | 🟢 Completa |
| Código Base | 🟡 En desarrollo |
| Seguridad | 🟢 Verificada |
| Tests | 🔴 Pendiente |
| CI/CD | 🔴 Pendiente |

---

## 🔗 Enlaces Rápidos

- [Léeme Primero](docs/01_Introduccion.md) - Empieza aquí
- [Diario](docs/02_Diario_Aprendizaje.md) - Progreso día a día
- [Errores](docs/03_Errores_Lecciones.md) - Aprende de mis errores
- [Metodología](docs/04_Metodologia.md) - Desarrollo con IA
- [Referencias](docs/01_Introduccion.md) - Fuentes y atribuciones
- [Licencia](LICENSE) - MIT License

---

**⚡ Última actualización**: 2025-12-19  
**📈 Versión**: 0.1.0-alpha (Aprendizaje activo)  
**🎯 Estado**: En desarrollo constante

---

*"El único error real es aquel del que no aprendemos nada."* - Henry Ford

**Este proyecto es un testimonio de que está bien no saber, está bien equivocarse, y está bien aprender en público.**

🛡️ **Alucard** - Defendiendo mientras aprendo
