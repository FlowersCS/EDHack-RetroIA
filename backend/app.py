from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import os
from datetime import datetime
from dotenv import load_dotenv
from pdf_processor import PDFProcessor
import os
if os.getenv('DEV_MODE') == 'true':
    from ai_evaluator_dev import AIEvaluator
else:
    from ai_evaluator import AIEvaluator
# Usar versión de desarrollo para evitar problemas de OAuth
from google_docs_manager_dev import GoogleDocsManager
from report_generator import ReportGenerator

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)
# Configurar CORS para producción
CORS(app, origins=[
    "http://localhost:3000",  # Desarrollo
    "https://tu-frontend-vercel.vercel.app",  # Reemplazar con tu URL de Vercel
    "https://*.vercel.app"  # Permite todos los subdominios de Vercel
])  # Para desarrollo local

# Configuración
upload_folder = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'uploads')
app.config['UPLOAD_FOLDER'] = upload_folder
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size

# Inicializar servicios
pdf_processor = PDFProcessor()
ai_evaluator = AIEvaluator()
docs_manager = GoogleDocsManager()
report_generator = ReportGenerator()

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'ok', 'message': 'EDHack IA API is running'})

@app.route('/api/upload-pdf', methods=['POST'])
def upload_pdf():
    """Subir PDF del estudiante"""
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'No file provided'}), 400
        
        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if file and file.filename.lower().endswith('.pdf'):
            filename = secure_filename(file.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(filepath)
            
            # Extraer texto del PDF
            extracted_text = pdf_processor.extract_text(filepath)
            
            return jsonify({
                'success': True,
                'filename': filename,
                'text_preview': extracted_text[:200] + '...' if len(extracted_text) > 200 else extracted_text,
                'session_id': generate_session_id()
            })
        
        return jsonify({'error': 'Invalid file format. Only PDF allowed'}), 400
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/evaluate', methods=['POST'])
def evaluate_text():
    """Evaluar texto con IA y crear documento Google Docs"""
    try:
        data = request.json
        session_id = data.get('session_id')
        filename = data.get('filename')
        
        if not session_id or not filename:
            return jsonify({'error': 'Missing session_id or filename'}), 400
        
        # Obtener texto completo del PDF
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        text = pdf_processor.extract_text(filepath)
        
        # Evaluar con IA
        evaluation = ai_evaluator.evaluate_text(text)
        
        # Obtener el nombre del estudiante desde los datos de la request
        student_name = data.get('student_name', 'Estudiante')
        
        # Crear documento Google Docs
        doc_result = docs_manager.create_feedback_document(student_name, evaluation)
        
        # Extraer doc_id e URL del resultado
        if isinstance(doc_result, dict):
            doc_id = doc_result.get('document_id')
            doc_url = doc_result.get('document_url')
        else:
            # Fallback para compatibilidad
            doc_id = doc_result
            doc_url = f'https://docs.google.com/document/d/{doc_id}/edit'
        
        return jsonify({
            'success': True,
            'evaluation': evaluation,
            'google_doc_id': doc_id,
            'google_doc_url': doc_url
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/approve-feedback', methods=['POST'])
def approve_feedback():
    """Aprobar retroalimentación del docente"""
    try:
        data = request.json
        doc_id = data.get('doc_id')
        session_id = data.get('session_id')
        approved = data.get('approved', False)
        
        if approved:
            # Generar reporte final
            final_feedback = docs_manager.get_document_content(doc_id)
            report = report_generator.generate_final_report(final_feedback, session_id)
            
            return jsonify({
                'success': True,
                'message': 'Feedback approved',
                'final_report': report
            })
        else:
            try:
                # Obtener feedback corregido y re-evaluar
                corrected_feedback = docs_manager.get_document_content(doc_id)
                print(f"🔍 [DEBUG] Feedback corregido recibido: {type(corrected_feedback)}")
                
                new_evaluation = ai_evaluator.re_evaluate_with_corrections(corrected_feedback)
                print(f"🔍 [DEBUG] Nueva evaluación generada: {type(new_evaluation)}")
                
                # Actualizar documento
                docs_manager.update_document(doc_id, str(new_evaluation))
            except Exception as e:
                print(f"❌ [ERROR] Error en re-evaluación: {str(e)}")
                import traceback
                traceback.print_exc()
                return jsonify({'error': f'Error in re-evaluation: {str(e)}'}), 500
            
            return jsonify({
                'success': True,
                'message': 'Feedback updated with corrections',
                'updated_evaluation': {
                    'puntaje_total': new_evaluation.get('puntaje_total', 0),
                    'timestamp': new_evaluation.get('timestamp'),
                    'type': new_evaluation.get('type', 'correction_iteration')
                }
            })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/sessions/<session_id>/status', methods=['GET'])
def get_session_status(session_id):
    """Obtener estado de una sesión"""
    try:
        # Implementar lógica de estado de sesión
        return jsonify({
            'session_id': session_id,
            'status': 'active',
            'message': 'Session found'
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/feedback-helper/<doc_id>')
def feedback_helper(doc_id):
    """Página intermedia para mostrar contenido de retroalimentación y crear Google Docs"""
    try:
        student_name = request.args.get('student', 'Estudiante')
        
        if os.getenv('DEV_MODE') == 'true':
            # Generar URL para crear Google Docs
            doc_title = f"EDHack IA - Retroalimentación - {student_name}"
            google_docs_url = f"https://docs.google.com/document/create?title={doc_title.replace(' ', '%20')}"
            
            content = f"""
            <html>
            <head>
                <title>Retroalimentación EDHack IA - {student_name}</title>
                <style>
                    body {{ 
                        font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; 
                        margin: 0; 
                        padding: 20px; 
                        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                        min-height: 100vh;
                    }}
                    .container {{
                        max-width: 800px;
                        margin: 0 auto;
                        background: white;
                        padding: 30px;
                        border-radius: 12px;
                        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
                    }}
                    .header {{
                        text-align: center;
                        margin-bottom: 30px;
                        color: #333;
                    }}
                    .buttons {{
                        text-align: center;
                        margin: 20px 0;
                    }}
                    .btn {{
                        display: inline-block;
                        padding: 12px 24px;
                        margin: 0 10px;
                        border: none;
                        border-radius: 6px;
                        font-size: 16px;
                        font-weight: bold;
                        text-decoration: none;
                        cursor: pointer;
                        transition: all 0.3s ease;
                    }}
                    .btn-primary {{
                        background: #4285f4;
                        color: white;
                    }}
                    .btn-primary:hover {{
                        background: #3367d6;
                        transform: translateY(-2px);
                    }}
                    .btn-secondary {{
                        background: #34a853;
                        color: white;
                    }}
                    .btn-secondary:hover {{
                        background: #137333;
                    }}
                    .content {{
                        background: #f8f9fa;
                        padding: 20px;
                        border-radius: 8px;
                        border: 2px solid #e9ecef;
                        margin: 20px 0;
                    }}
                    pre {{
                        background: white;
                        padding: 20px;
                        border-radius: 6px;
                        border: 1px solid #ddd;
                        white-space: pre-wrap;
                        font-family: 'Courier New', monospace;
                        font-size: 14px;
                        line-height: 1.5;
                        max-height: 400px;
                        overflow-y: auto;
                    }}
                    .steps {{
                        background: #e3f2fd;
                        padding: 20px;
                        border-radius: 8px;
                        margin: 20px 0;
                        border-left: 4px solid #2196f3;
                    }}
                    .step {{
                        margin: 10px 0;
                        font-weight: 500;
                    }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>📝 Retroalimentación Generada</h1>
                        <h2>Estudiante: {student_name}</h2>
                        <p>La IA ha generado una evaluación completa lista para usar</p>
                    </div>
                    
                    <div class="steps">
                        <h3>📋 Instrucciones:</h3>
                        <div class="step">1. Haz clic en "📋 Copiar Contenido" para copiar la evaluación</div>
                        <div class="step">2. Haz clic en "📄 Crear Google Docs" para abrir un nuevo documento</div>
                        <div class="step">3. Pega el contenido (Ctrl+V) en el documento de Google Docs</div>
                        <div class="step">4. ¡Edita y personaliza según necesites!</div>
                    </div>
                    
                    <div class="buttons">
                        <button class="btn btn-primary" onclick="copyContent()">📋 Copiar Contenido</button>
                        <a href="{google_docs_url}" target="_blank" class="btn btn-secondary">📄 Crear Google Docs</a>
                    </div>
                    
                    <div class="content">
                        <h3>Vista previa del contenido:</h3>
                        <pre id="feedback-content">📝 RETROALIMENTACIÓN AUTOMÁTICA EDHack IA

ESTUDIANTE: {student_name}
FECHA: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
PUNTAJE TOTAL: 83.2/100 puntos

=== EVALUACIÓN DETALLADA ===

ORTOGRAFÍA: 88 puntos (Peso: 20%)
Comentario: Muy buen uso de las reglas ortográficas. Se observa dominio de acentuación y signos de puntuación.

GRAMÁTICA: 85 puntos (Peso: 20%)
Comentario: Estructura gramatical adecuada con oraciones bien formadas. Buen uso de tiempos verbales.

COHERENCIA: 90 puntos (Peso: 25%)
Comentario: Las ideas se presentan de manera lógica y fluida. La historia tiene un hilo conductor claro.

COHESIÓN: 80 puntos (Peso: 10%)
Comentario: Buena conexión entre oraciones y párrafos. Uso apropiado de conectores.

VOCABULARIO: 82 puntos (Peso: 10%)
Comentario: Vocabulario variado y apropiado para el nivel. Uso creativo de adjetivos descriptivos.

ESTRUCTURA: 81 puntos (Peso: 10%)
Comentario: Estructura narrativa clara con inicio, desarrollo y desenlace bien definidos.

=== COMENTARIO GENERAL ===
Excelente trabajo narrativo que muestra creatividad y dominio de las habilidades de escritura. El cuento presenta una historia entretenida con personajes bien desarrollados.

=== FORTALEZAS ===
• Creatividad en el desarrollo de la historia
• Uso apropiado del lenguaje descriptivo
• Estructura narrativa coherente
• Buen manejo de la ortografía y gramática

=== ÁREAS DE MEJORA ===
• Podría ampliar algunos diálogos entre personajes
• Desarrollar más detalles del escenario
• Incluir más elementos descriptivos del ambiente

=== INSTRUCCIONES PARA EL DOCENTE ===
1. Revise la evaluación automática generada por la IA
2. Agregue sus comentarios y correcciones personalizadas
3. Modifique los puntajes si considera necesario
4. Use el botón "Solicitar nueva iteración" en la interfaz para generar una versión mejorada
5. Comparta el documento con el estudiante para retroalimentación

---
Documento generado automáticamente por EDHack IA
Sistema de Evaluación Automática de Escritura</pre>
                    </div>
                </div>
                
                <script>
                function copyContent() {{
                    const content = document.getElementById('feedback-content');
                    navigator.clipboard.writeText(content.textContent).then(function() {{
                        alert('✅ ¡Contenido copiado al portapapeles!\\n\\nAhora haz clic en "Crear Google Docs" y pega el contenido (Ctrl+V).');
                    }});
                }}
                </script>
            </body>
            </html>
            """
            return content
        else:
            return jsonify({{'error': 'Not available in production mode'}}), 404
    except Exception as e:
        return jsonify({{'error': str(e)}}), 500

def generate_session_id():
    """Generar ID único para la sesión"""
    import uuid
    return str(uuid.uuid4())

def secure_filename(filename):
    """Asegurar nombre de archivo"""
    import re
    filename = re.sub(r'[^a-zA-Z0-9._-]', '', filename)
    return filename

if __name__ == '__main__':
    # Crear directorio de uploads si no existe
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    # Para producción en Railway/Render
    port = int(os.environ.get('PORT', 5000))
    debug_mode = os.environ.get('FLASK_ENV') == 'development'
    app.run(host='0.0.0.0', port=port, debug=debug_mode)