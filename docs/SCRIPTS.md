# 🚀 Scripts de Inicio Rápido

## Ejecutar Todo el Sistema

### Linux/macOS
```bash
#!/bin/bash
# Ejecutar este script desde la carpeta raíz del proyecto

echo "🚀 Iniciando EDHack IA..."

# Backend
echo "📡 Iniciando Backend Flask..."
cd backend
source venv/bin/activate
python app.py &
BACKEND_PID=$!

# Frontend  
echo "🎨 Iniciando Frontend React..."
cd ../frontend
npm start &
FRONTEND_PID=$!

echo "✅ Sistema iniciado!"
echo "📡 Backend: http://localhost:5000"
echo "🎨 Frontend: http://localhost:3000"
echo ""
echo "Para detener el sistema, presiona Ctrl+C"

# Manejar interrupción
trap "kill $BACKEND_PID $FRONTEND_PID; exit" INT

# Esperar
wait
```

### Windows (PowerShell)
```powershell
# Ejecutar desde la carpeta raíz del proyecto

Write-Host "🚀 Iniciando EDHack IA..." -ForegroundColor Green

# Backend
Write-Host "📡 Iniciando Backend Flask..." -ForegroundColor Blue
Start-Process -FilePath "cmd" -ArgumentList "/c", "cd backend && venv\Scripts\activate && python app.py" -WindowStyle Normal

# Esperar un poco para que inicie el backend
Start-Sleep -Seconds 3

# Frontend
Write-Host "🎨 Iniciando Frontend React..." -ForegroundColor Blue  
Start-Process -FilePath "cmd" -ArgumentList "/c", "cd frontend && npm start" -WindowStyle Normal

Write-Host "✅ Sistema iniciado!" -ForegroundColor Green
Write-Host "📡 Backend: http://localhost:5000" -ForegroundColor Yellow
Write-Host "🎨 Frontend: http://localhost:3000" -ForegroundColor Yellow
```

## Instalación Completa

### Linux/macOS
```bash
#!/bin/bash
echo "📦 Instalando EDHack IA..."

# Verificar Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 no está instalado"
    exit 1
fi

# Verificar Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js no está instalado" 
    exit 1
fi

# Backend
echo "🔧 Configurando Backend..."
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Crear archivo .env si no existe
if [ ! -f .env ]; then
    cp .env.example .env
    echo "⚠️  Configura tu GEMINI_API_KEY en backend/.env"
fi

# Frontend
echo "🎨 Configurando Frontend..."
cd ../frontend
npm install

# Crear directorios necesarios
echo "📁 Creando directorios..."
mkdir -p ../uploads
mkdir -p ../config

echo "✅ Instalación completada!"
echo ""
echo "📋 Próximos pasos:"
echo "1. Configurar GEMINI_API_KEY en backend/.env"
echo "2. Configurar Google Docs API (ver docs/INSTALLATION.md)"
echo "3. Ejecutar: ./start.sh"
```

## Scripts de Utilidad

### Limpiar Sistema
```bash
#!/bin/bash
echo "🧹 Limpiando sistema..."

# Limpiar uploads
rm -rf uploads/*

# Limpiar cache Python
find . -type d -name __pycache__ -exec rm -rf {} +
find . -name "*.pyc" -delete

# Limpiar node_modules si es necesario
# rm -rf frontend/node_modules

echo "✅ Sistema limpiado!"
```

### Ejecutar Tests
```bash
#!/bin/bash
echo "🧪 Ejecutando tests..."

cd backend
source venv/bin/activate

# Tests unitarios
echo "📋 Tests unitarios..."
pytest tests/ -v -m "not integration"

# Tests de integración (si están configuradas las APIs)
echo "🔌 Tests de integración..."
pytest tests/ -v -m integration

echo "✅ Tests completados!"
```