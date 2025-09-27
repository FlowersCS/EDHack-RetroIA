# 🔧 Documentación Técnica - EDHack IA

## 📋 Arquitectura del Sistema

### Visión General
EDHack IA es un sistema MVP (Producto Mínimo Viable) diseñado para evaluación automática de escritura usando IA. La arquitectura sigue un patrón cliente-servidor con integración a APIs externas.

```
┌─────────────────┐    HTTP/REST    ┌─────────────────┐
│   Frontend      │ ←──────────────→ │    Backend      │
│   (React)       │                 │    (Flask)      │
└─────────────────┘                 └─────────────────┘
                                            │
                                            ├── Gemini API (IA)
                                            ├── Google Docs API
                                            └── File System (PDFs)
```

---

## 🗂️ Componentes del Sistema

### Backend (Flask/Python)

#### `app.py` - Aplicación Principal
```python
# Endpoints principales:
GET  /api/health          # Health check
POST /api/upload-pdf      # Subir PDF
POST /api/evaluate        # Evaluar con IA
POST /api/approve-feedback # Aprobar/revisar retroalimentación
GET  /api/sessions/{id}/status # Estado de sesión
```

#### `pdf_processor.py` - Procesamiento de PDF
- **Propósito**: Extraer y limpiar texto de archivos PDF
- **Librerías**: PyMuPDF (primario), pdfplumber (fallback)
- **Métodos principales**:
  - `extract_text()`: Extracción principal
  - `validate_pdf()`: Validación de archivo
  - `get_text_statistics()`: Estadísticas del texto

```python
# Ejemplo de uso
processor = PDFProcessor()
text = processor.extract_text("documento.pdf")
info = processor.get_pdf_info("documento.pdf")
```

#### `ai_evaluator.py` - Evaluación con IA
- **Propósito**: Interfaz con Gemini API para evaluación
- **Modelo**: Gemini Pro
- **Criterios hardcodeados**:
  - Ortografía (20%)
  - Gramática (20%)
  - Coherencia (25%)
  - Cohesión (15%)
  - Vocabulario (10%)
  - Estructura (10%)

```python
# Estructura de respuesta esperada
{
    "puntuacion_total": 85,
    "criterios": {
        "ortografia": {
            "puntuacion": 90,
            "comentario": "Excelente uso de reglas ortográficas",
            "ejemplos": ["corrección 1", "corrección 2"]
        }
    },
    "fortalezas": ["fortaleza 1", "fortaleza 2"],
    "areas_mejora": ["mejora 1", "mejora 2"],
    "comentario_general": "Comentario general del texto",
    "nivel_sugerido": "Intermedio"
}
```

#### `google_docs_manager.py` - Gestión Google Docs
- **Propósito**: Crear y gestionar documentos editables
- **APIs utilizadas**: Google Docs API, Google Drive API
- **Autenticación**: OAuth 2.0
- **Permisos**: Edición pública (MVP - sin seguridad robusta)

#### `report_generator.py` - Generación de Reportes
- **Propósito**: Crear reportes personalizados por audiencia
- **Templates**: Jinja2 para diferentes audiencias
- **Formatos**: Markdown con contenido específico
- **Audiencias**: Estudiante, Familia, Docente

### Frontend (React)

#### Estructura de Componentes
```
src/
├── App.js                    # Componente principal
├── components/
│   ├── Header.js            # Encabezado con estado
│   ├── StepIndicator.js     # Indicador de progreso
│   ├── UploadPDF.js         # Subida de archivos
│   ├── EvaluationProcess.js # Proceso de evaluación
│   ├── TeacherReview.js     # Revisión docente
│   └── FinalReports.js      # Reportes finales
└── index.css               # Estilos globales
```

#### Estado Global (useState)
```javascript
const [sessionData, setSessionData] = useState({
    sessionId: null,
    filename: null,
    evaluationResult: null,
    googleDocId: null,
    googleDocUrl: null,
    finalReports: null,
    status: 'ready' // ready, processing, completed, error
});
```

---

## 🔄 Flujo de Datos

### 1. Subida de PDF
```
Usuario → UploadPDF → POST /api/upload-pdf → PDFProcessor
                                           ↓
SessionData ← JSON Response ← Text Extract ← PDF Analysis
```

### 2. Evaluación con IA
```
SessionData → EvaluationProcess → POST /api/evaluate → AIEvaluator
                                                     ↓
                                   Gemini API → Evaluation Result
                                                     ↓
GoogleDocsManager ← Create Document ← Format Content ← Parse Response
```

### 3. Revisión Docente
```
Teacher Input → TeacherReview → POST /api/approve-feedback
                                       ↓
                              [approved] → ReportGenerator
                                       ↓
                              [revise] → AIEvaluator → Update Doc
```

### 4. Reportes Finales
```
FinalReports → Display Reports → Download/Share Options
```

---

## 🗄️ Estructura de Datos

### Sesión de Evaluación
```javascript
{
    sessionId: "uuid-string",
    filename: "documento.pdf",
    textPreview: "Los primeros 200 caracteres...",
    evaluationResult: {
        puntuacion_total: 85,
        criterios: { /* criterios detallados */ },
        fortalezas: ["fortaleza1", "fortaleza2"],
        areas_mejora: ["mejora1", "mejora2"],
        comentario_general: "Texto del comentario",
        nivel_sugerido: "Intermedio",
        timestamp: "2024-01-01T12:00:00Z"
    },
    googleDocId: "doc-id-string",
    googleDocUrl: "https://docs.google.com/document/d/...",
    finalReports: {
        estudiante: { content: "...", format: "text/markdown" },
        familia: { content: "...", format: "text/markdown" },
        docente: { content: "...", format: "text/markdown" },
        metadata: {
            session_id: "uuid",
            generated_at: "timestamp",
            version: "1.0",
            system: "EDHack IA MVP"
        }
    },
    status: "completed"
}
```

---

## 🔌 APIs Externas

### Gemini API
- **URL Base**: `https://generativelanguage.googleapis.com/v1/`
- **Modelo**: `gemini-pro`
- **Autenticación**: API Key
- **Rate Limits**: Según plan de Google
- **Configuración**:
```python
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
```

### Google Docs API
- **URL Base**: `https://docs.googleapis.com/v1/`
- **Autenticación**: OAuth 2.0
- **Scopes necesarios**:
  - `https://www.googleapis.com/auth/documents`
  - `https://www.googleapis.com/auth/drive.file`
- **Operaciones**:
  - Crear documento
  - Insertar contenido
  - Obtener contenido
  - Actualizar permisos

---

## 🔒 Configuración de Seguridad (MVP)

### Variables de Entorno
```bash
# Críticas (nunca commitear)
GEMINI_API_KEY=secret_key_here

# Configuración
FLASK_ENV=development
FLASK_DEBUG=True
UPLOAD_FOLDER=../uploads
MAX_FILE_SIZE=16777216
```

### Archivos Sensibles
```
config/
├── credentials.json    # Credenciales Google (no commitear)
├── token.json         # Token OAuth (auto-generado)
└── .gitignore         # Asegurar que ignora archivos sensibles
```

### Limitaciones MVP
- Sin autenticación de usuarios
- Documentos públicos con enlace
- Sin cifrado de datos
- Sin rate limiting robusto
- Validación básica de archivos

---

## 🧪 Testing

### Backend Tests (pytest)
```bash
# Estructura de tests
tests/
├── test_backend.py        # Tests principales
├── pytest.ini           # Configuración pytest
└── conftest.py          # Fixtures (si necesario)

# Ejecutar tests
pytest tests/ -v
pytest -m "not integration"  # Solo unitarios
pytest --cov=backend tests/  # Con cobertura
```

### Tipos de Tests
1. **Unitarios**: Funciones individuales
2. **Integración**: APIs externas (requieren configuración)
3. **End-to-end**: Flujo completo (manual para MVP)

### Fixtures Importantes
```python
@pytest.fixture
def client():
    """Cliente de pruebas Flask"""
    
@pytest.fixture  
def pdf_processor():
    """Instancia PDFProcessor"""
    
@pytest.fixture
def sample_evaluation():
    """Datos de evaluación de muestra"""
```

---

## 📊 Monitoreo y Logs

### Logs Backend (Flask)
```python
import logging

# Configuración básica
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Uso en endpoints
logger.info(f"PDF uploaded: {filename}")
logger.error(f"Evaluation failed: {str(e)}")
```

### Métricas Importantes
- Tiempo de procesamiento PDF
- Tiempo de respuesta Gemini API
- Rate de éxito de evaluaciones
- Errores de Google Docs API

---

## 🚀 Deployment (Futuro)

### Consideraciones para Producción
1. **Seguridad**:
   - Implementar autenticación JWT
   - Validación robusta de archivos
   - Rate limiting por usuario
   - HTTPS obligatorio

2. **Escalabilidad**:
   - Base de datos para persistencia
   - Queue system para procesamiento async
   - Load balancing
   - CDN para archivos estáticos

3. **Monitoreo**:
   - APM (Application Performance Monitoring)
   - Logs centralizados
   - Alertas automáticas
   - Métricas de negocio

### Stack Sugerido para Producción
- **Backend**: Flask + Gunicorn + Nginx
- **Database**: PostgreSQL + Redis
- **Queue**: Celery + Redis
- **Monitoring**: Sentry + Prometheus
- **Deployment**: Docker + Kubernetes

---

## 🔧 Mantenimiento

### Actualizaciones Regulares
1. **Dependencias Python**: `pip list --outdated`
2. **Dependencias Node**: `npm outdated`
3. **APIs externas**: Verificar deprecaciones
4. **Criterios de evaluación**: Revisar con docentes

### Backups Necesarios
- Configuraciones de APIs
- Credenciales (encriptadas)
- Logs de sistema
- Base de datos (cuando se implemente)

### Monitoreo de Performance
- Tiempo respuesta endpoints
- Uso de memoria/CPU
- Rate limits de APIs externas
- Espacio en disco (uploads)

---

## 📚 Referencias Técnicas

### Documentación APIs
- [Google Gemini API](https://ai.google.dev/docs)
- [Google Docs API](https://developers.google.com/docs/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [React Documentation](https://react.dev/)

### Librerías Clave
- **PyMuPDF**: Procesamiento PDF avanzado
- **pdfplumber**: Extracción texto PDF alternativa
- **google-generativeai**: Cliente oficial Gemini
- **google-api-python-client**: APIs Google
- **jinja2**: Templates para reportes
- **axios**: HTTP client para React

---

*Documentación técnica EDHack IA v1.0 - MVP Local*