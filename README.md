# 📝 EDHack IA - Sistema de Evaluación Automática de Escritura

> **Sistema MVP de Evaluación Automática de Escritura con Inteligencia Artificial**

[![Version](https://img.shields.io/badge/version-1.0.0-blue.svg)](https://github.com/FlowersCS/EDHack-RetroIA)
[![License](https://img.shields.io/badge/license-Educational-green.svg)](https://opensource.org/licenses/MIT)
[![Python](https://img.shields.io/badge/python-3.8+-blue.svg)](https://python.org)
[![React](https://img.shields.io/badge/react-18+-blue.svg)](https://reactjs.org)

---

## 🎯 ¿Qué es EDHack IA?

EDHack IA es un sistema innovador que combina inteligencia artificial con supervisión docente para evaluar automáticamente textos escritos por estudiantes, generando retroalimentación personalizada y reportes detallados.

### ✨ Características Principales

- 🤖 **Evaluación automática** con IA Gemini de Google
- 📄 **Procesamiento de PDFs** con extracción inteligente de texto
- 👩‍🏫 **Revisión docente** con documentos Google Docs editables
- 📊 **Reportes personalizados** para estudiantes, familias y docentes
- 🔄 **Proceso iterativo** hasta aprobación final
- 🏠 **Ejecución local** sin servidores remotos (MVP)

---

## 🚀 Inicio Rápido

### 1. Requisitos Previos
- Python 3.8+
- Node.js 16+
- Cuenta Google (para APIs)

### 2. Instalación
```bash
# Clonar repositorio
git clone https://github.com/FlowersCS/EDHack-RetroIA.git
cd EDHack-RetroIA

# Backend
cd backend
python -m venv venv
source venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# Frontend  
cd ../frontend
npm install
```

### 3. Configuración
```bash
# Configurar variables de entorno
cd backend
cp .env.example .env
# Editar .env con tu GEMINI_API_KEY
```

### 4. Ejecutar
```bash
# Terminal 1 - Backend
cd backend && python app.py

# Terminal 2 - Frontend  
cd frontend && npm start
```

🌐 **Acceder**: http://localhost:3000

---

## 📋 Cómo Funciona

### Flujo del Sistema

```
📄 PDF del Estudiante → 🤖 Evaluación IA → 👩‍🏫 Revisión Docente → 📊 Reportes Finales
```

### 1. **Subida de PDF** 📄
- El estudiante/docente sube un PDF con texto escrito
- Sistema extrae y valida el contenido
- Genera vista previa para confirmación

### 2. **Evaluación con IA** 🤖
- Gemini API analiza el texto según 6 criterios:
  - **Ortografía** (20%): Reglas ortográficas
  - **Gramática** (20%): Estructura sintáctica  
  - **Coherencia** (25%): Lógica y flujo de ideas
  - **Cohesión** (15%): Conexión entre párrafos
  - **Vocabulario** (10%): Riqueza léxica
  - **Estructura** (10%): Organización textual

### 3. **Revisión Docente** 👩‍🏫
- Se crea documento Google Docs editable
- Docente revisa y puede modificar la evaluación
- Opción de aprobar o solicitar nueva iteración IA

### 4. **Reportes Finales** 📊
- **Estudiante**: Reporte motivacional con próximos pasos
- **Familia**: Guía comprensible con actividades de apoyo
- **Docente**: Análisis técnico con recomendaciones pedagógicas

---

## 🗂️ Estructura del Proyecto

```
EDHack/
├── 🔧 backend/              # API Flask + IA
│   ├── app.py              # Aplicación principal
│   ├── pdf_processor.py    # Procesamiento PDF
│   ├── ai_evaluator.py     # Evaluación Gemini
│   ├── google_docs_manager.py # Google Docs
│   └── report_generator.py # Generación reportes
├── 🎨 frontend/            # Interfaz React
│   ├── src/components/     # Componentes UI
│   └── public/            # Archivos estáticos
├── 🧪 tests/              # Tests automatizados
├── 📚 docs/               # Documentación
├── ⚙️ config/             # Configuraciones
└── 📁 uploads/            # PDFs subidos
```

---

## 🎓 Criterios de Evaluación

| Criterio | Peso | Descripción |
|----------|------|-------------|
| 📝 Ortografía | 20% | Uso correcto de reglas ortográficas |
| 📚 Gramática | 20% | Estructura gramatical y sintaxis |
| 🧠 Coherencia | 25% | Lógica y flujo de ideas |
| 🔗 Cohesión | 15% | Conexión entre párrafos y oraciones |
| 📖 Vocabulario | 10% | Riqueza y precisión del vocabulario |
| 🏗️ Estructura | 10% | Organización del texto |

### Escala de Puntuación
- 🌟 **90-100**: Excelente
- 👍 **80-89**: Muy Bueno  
- ✅ **70-79**: Bueno
- ⚠️ **60-69**: Regular
- 📚 **0-59**: Necesita Mejora

---

## 🛠️ Tecnologías Utilizadas

### Backend
- **Flask**: Framework web Python
- **Gemini API**: Inteligencia artificial de Google
- **PyMuPDF**: Procesamiento de PDFs
- **Google Docs API**: Documentos editables
- **Jinja2**: Templates para reportes

### Frontend  
- **React**: Biblioteca de interfaces
- **Material-UI**: Componentes de diseño
- **Axios**: Cliente HTTP
- **React Dropzone**: Subida de archivos

### Herramientas
- **Pytest**: Testing automatizado
- **Git**: Control de versiones
- **OAuth 2.0**: Autenticación Google

---

## 📖 Documentación

- 📋 **[Guía de Instalación](docs/INSTALLATION.md)** - Setup completo paso a paso
- 👥 **[Manual de Usuario](docs/USER_MANUAL.md)** - Cómo usar el sistema
- 🔧 **[Documentación Técnica](docs/TECHNICAL.md)** - Arquitectura y APIs

---

## 🧪 Testing

```bash
# Tests backend
cd backend
pytest tests/ -v

# Tests con cobertura
pytest --cov=backend tests/

# Solo tests unitarios
pytest -m "not integration"
```

---

## ⚠️ Consideraciones MVP

Este es un **Producto Mínimo Viable** diseñado para **uso local y educativo**:

### ✅ Incluye
- Funcionalidad core completa
- Integración con APIs de IA
- Interfaz web intuitiva
- Generación de reportes
- Tests básicos

### ⚠️ No incluye (para producción)
- Autenticación robusta de usuarios
- Base de datos persistente
- Seguridad avanzada
- Escalabilidad para múltiples usuarios
- Deployment automatizado

---

## 🤝 Contribuir

Este proyecto es educativo y experimental. Para contribuir:

1. Fork el repositorio
2. Crear rama feature (`git checkout -b feature/nueva-funcionalidad`)
3. Commit cambios (`git commit -am 'Añadir nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/nueva-funcionalidad`)
5. Crear Pull Request

---

## 📞 Soporte

- 📧 **Email**: [tu-email@dominio.com]
- 🐛 **Issues**: [GitHub Issues](https://github.com/FlowersCS/EDHack-RetroIA/issues)
- 📚 **Wiki**: [Documentación adicional](https://github.com/FlowersCS/EDHack-RetroIA/wiki)

---

## 📄 Licencia

Este proyecto está bajo licencia educativa. Ver archivo `LICENSE` para más detalles.

---

## 🙏 Agradecimientos

- **Google AI** por la API Gemini
- **Google Cloud** por las APIs de documentos
- **Comunidad educativa** por feedback y sugerencias

---

<div align="center">

**🚀 ¿Listo para revolucionar la evaluación de escritura?**

[📥 Descargar](https://github.com/FlowersCS/EDHack-RetroIA/archive/refs/heads/main.zip) | [📖 Documentación](docs/) | [🐛 Reportar Bug](https://github.com/FlowersCS/EDHack-RetroIA/issues)

---

*Desarrollado con ❤️ para la educación*

</div>