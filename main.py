#!/usr/bin/env python3
"""
EDHack IA - Sistema de Evaluación Automática de Escritura
Entry point para Railway deployment
"""

import os
import sys

# Agregar el directorio backend al path
backend_dir = os.path.join(os.path.dirname(__file__), 'backend')
sys.path.insert(0, backend_dir)

# Cambiar al directorio backend
os.chdir(backend_dir)

# Importar y ejecutar la aplicación
from app import app

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=False)