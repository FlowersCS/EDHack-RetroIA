#!/bin/bash
set -e

echo "🔧 Configurando entorno..."
export DEV_MODE=true
export FLASK_ENV=production

echo "📁 Cambiando al directorio backend..."
cd backend

echo " Iniciando aplicación Flask..."
exec python app.py