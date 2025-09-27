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

# Cambiar al directorio backend para que las rutas relativas funcionen
os.chdir(backend_dir)

# Configurar variables de entorno necesarias
os.environ['DEV_MODE'] = 'true'
os.environ['FLASK_ENV'] = 'production'

# Importar y ejecutar la aplicación
try:
    from app import app
    print("✅ App importada correctamente")
    
    if __name__ == '__main__':
        port = int(os.environ.get('PORT', 5000))
        print(f"🚀 Iniciando servidor en puerto {port}")
        app.run(host='0.0.0.0', port=port, debug=False)
        
except Exception as e:
    print(f"❌ Error al importar o iniciar la app: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)