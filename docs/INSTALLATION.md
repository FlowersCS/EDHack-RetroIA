# 🚀 EDHack IA - Guía de Instalación y Configuración

## 📋 Requisitos Previos

### Sistema Operativo
- Linux (Ubuntu 18.04+, CentOS 7+)
- macOS 10.14+
- Windows 10+ (con WSL recomendado)

### Software Requerido
- **Python 3.8+** (recomendado 3.9 o 3.10)
- **Node.js 16+** y npm
- **Git**
- Navegador web moderno (Chrome, Firefox, Safari, Edge)

### APIs Externas Necesarias
1. **Google Gemini API** - Para evaluación con IA
2. **Google Cloud Console** - Para Google Docs API
3. **Google Docs API** - Para crear documentos editables

---

## 🛠️ Instalación Paso a Paso

### 1. Clonar el Repositorio
```bash
git clone https://github.com/FlowersCS/EDHack-RetroIA.git
cd EDHack-RetroIA
```

### 2. Configurar Backend (Python/Flask)

#### 2.1 Crear Entorno Virtual
```bash
cd backend
python3 -m venv venv
source venv/bin/activate  # En Windows: venv\Scripts\activate
```

#### 2.2 Instalar Dependencias
```bash
pip install -r requirements.txt
```

#### 2.3 Configurar Variables de Entorno
```bash
# Copiar archivo de ejemplo
cp .env.example .env

# Editar .env con tus configuraciones
nano .env
```

Configurar en `.env`:
```env
GEMINI_API_KEY=tu_api_key_de_gemini_aqui
FLASK_ENV=development
FLASK_DEBUG=True
```

### 3. Configurar APIs de Google

#### 3.1 Obtener API Key de Gemini
1. Ir a [Google AI Studio](https://makersuite.google.com/app/apikey)
2. Crear nuevo proyecto o usar existente
3. Generar API Key
4. Copiar la clave al archivo `.env`

#### 3.2 Configurar Google Docs API
1. Ir a [Google Cloud Console](https://console.cloud.google.com/)
2. Crear nuevo proyecto o seleccionar existente
3. Habilitar las APIs:
   - Google Docs API
   - Google Drive API
4. Ir a "Credenciales" → "Crear credenciales" → "ID de cliente OAuth 2.0"
5. Configurar tipo: "Aplicación de escritorio"
6. Descargar el archivo JSON de credenciales
7. Renombrar como `credentials.json` y colocar en `config/credentials.json`

```bash
# Crear directorio de configuración
mkdir -p config
# Mover archivo de credenciales descargado
mv ~/Downloads/credentials.json config/credentials.json
```

### 4. Configurar Frontend (React)

#### 4.1 Instalar Dependencias
```bash
cd ../frontend
npm install
```

#### 4.2 Verificar Configuración
El archivo `package.json` ya incluye proxy para desarrollo local.

### 5. Verificar Instalación

#### 5.1 Ejecutar Tests Backend
```bash
cd ../backend
source venv/bin/activate
pytest tests/ -v
```

#### 5.2 Test de Conectividad APIs
```bash
# Test rápido de Gemini API
python -c "
import os
import google.generativeai as genai
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))
model = genai.GenerativeModel('gemini-pro')
response = model.generate_content('Hello world')
print('✅ Gemini API funcionando')
print(response.text[:50])
"
```

---

## 🚀 Ejecutar el Sistema

### Modo Desarrollo (Recomendado para MVP)

#### Terminal 1 - Backend
```bash
cd backend
source venv/bin/activate  # En Windows: venv\Scripts\activate
python app.py
```
El backend estará disponible en: http://localhost:5000

#### Terminal 2 - Frontend
```bash
cd frontend
npm start
```
El frontend estará disponible en: http://localhost:3000

### Acceder al Sistema
1. Abrir navegador en http://localhost:3000
2. El sistema mostrará la interfaz de EDHack IA
3. Seguir el flujo de 4 pasos:
   - Subir PDF
   - Evaluación IA
   - Revisión Docente
   - Reportes Finales

---

## 🔧 Configuración Adicional

### Configurar Límites de Archivo
En `backend/app.py`, línea 11:
```python
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB
```

### Personalizar Criterios de Evaluación
En `backend/ai_evaluator.py`, líneas 15-35:
```python
self.evaluation_criteria = {
    'ortografia': {'peso': 20, 'descripcion': 'Uso correcto de las reglas ortográficas'},
    # Modificar según necesidades específicas
}
```

### Configurar Directorio de Uploads
```bash
# Asegurar que existe el directorio
mkdir -p uploads
chmod 755 uploads
```

---

## 🧪 Testing

### Tests Backend
```bash
cd backend
source venv/bin/activate

# Todos los tests
pytest

# Solo tests unitarios
pytest -m "not integration"

# Tests con cobertura
pytest --cov=backend tests/
```

### Tests Frontend (Opcional)
```bash
cd frontend
npm test
```

---

## 🚨 Solución de Problemas Comunes

### Error: "GEMINI_API_KEY not set"
```bash
# Verificar variable de entorno
echo $GEMINI_API_KEY

# Si está vacía, configurar en .env
echo "GEMINI_API_KEY=tu_clave_aqui" >> backend/.env
```

### Error: "Google credentials not found"
```bash
# Verificar que existe el archivo
ls -la config/credentials.json

# Si no existe, seguir pasos de configuración Google Docs API
```

### Error: "Module not found"
```bash
# Reinstalar dependencias backend
cd backend
pip install -r requirements.txt

# Reinstalar dependencias frontend
cd frontend
npm install
```

### Error: "Port already in use"
```bash
# Backend (Puerto 5000)
lsof -ti:5000 | xargs kill -9

# Frontend (Puerto 3000)
lsof -ti:3000 | xargs kill -9
```

### PDF no se puede procesar
- Verificar que el PDF contiene texto extraíble (no solo imágenes)
- Tamaño máximo: 16MB
- Formato soportado: solo PDF

---

## 📚 Estructura del Proyecto

```
EDHack/
├── backend/                 # API Flask
│   ├── app.py              # Aplicación principal
│   ├── pdf_processor.py    # Procesamiento PDF
│   ├── ai_evaluator.py     # Evaluación con IA
│   ├── google_docs_manager.py # Google Docs
│   ├── report_generator.py # Generación reportes
│   ├── requirements.txt    # Dependencias Python
│   └── .env.example       # Variables de entorno
├── frontend/               # Interfaz React
│   ├── src/
│   │   ├── components/    # Componentes React
│   │   ├── App.js        # Aplicación principal
│   │   └── index.js      # Punto de entrada
│   ├── public/           # Archivos estáticos
│   └── package.json      # Dependencias Node
├── config/                 # Configuraciones
│   ├── credentials.json   # Credenciales Google (crear)
│   └── token.json        # Token OAuth (auto-generado)
├── uploads/               # Archivos PDF subidos
├── tests/                 # Tests del sistema
├── docs/                  # Documentación
└── README.md             # Documentación principal
```

---

## 🔐 Consideraciones de Seguridad (MVP)

> **⚠️ IMPORTANTE**: Este es un MVP para uso local. Para producción, implementar:

- Autenticación de usuarios
- Validación robusta de archivos
- Límites de rate limiting
- Cifrado de datos sensibles
- Configuración HTTPS
- Variables de entorno seguras

---

## 🆘 Soporte

Para problemas técnicos:
1. Revisar logs en terminal donde ejecutas backend/frontend
2. Verificar configuración de APIs
3. Consultar sección de "Solución de Problemas"
4. Crear issue en el repositorio GitHub

---

## 📄 Licencia
Este proyecto es un MVP educativo. Usar bajo tu propia responsabilidad.