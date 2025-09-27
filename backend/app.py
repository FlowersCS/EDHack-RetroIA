from flask import Flask, request, jsonify, redirect
from flask_cors import CORS
import os
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



@app.route('/api/get-feedback-content/<doc_id>')
def get_feedback_content(doc_id):
    """Obtener contenido de retroalimentación para copiar al documento"""
    try:
        # En modo desarrollo, mostrar página con contenido para copiar
        if os.getenv('DEV_MODE') == 'true':
            content = """
            <html>
            <head>
                <title>Contenido de Retroalimentación - EDHack IA</title>
                <style>
                    body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.6; }
                    .content { background: #f9f9f9; padding: 20px; border-radius: 8px; }
                    .copy-button { background: #4285f4; color: white; padding: 10px 20px; border: none; border-radius: 4px; cursor: pointer; margin: 10px 0; }
                    .copy-button:hover { background: #3367d6; }
                    pre { background: white; padding: 15px; border-radius: 4px; border: 1px solid #ddd; white-space: pre-wrap; }
                </style>
            </head>
            <body>
                <h1>📝 Contenido de Retroalimentación</h1>
                <p><strong>Instrucciones:</strong> Copia el contenido de abajo y pégalo en tu documento de Google Docs.</p>
                
                <button class="copy-button" onclick="copyContent()">📋 Copiar Contenido</button>
                
                <div class="content">
                    <pre id="feedback-content">Este contenido se generaría dinámicamente con la evaluación real del estudiante.
                    
📝 RETROALIMENTACIÓN AUTOMÁTICA EDHack IA

ESTUDIANTE: [Nombre del estudiante]
FECHA: [Fecha de evaluación]
PUNTAJE TOTAL: [X]/100 puntos

=== EVALUACIÓN DETALLADA ===

ORTOGRAFÍA: [X] puntos (Peso: 20%)
Comentario: [Comentario sobre ortografía]

GRAMÁTICA: [X] puntos (Peso: 20%)
Comentario: [Comentario sobre gramática]

COHERENCIA: [X] puntos (Peso: 25%)
Comentario: [Comentario sobre coherencia]

[... otros criterios ...]

=== COMENTARIO GENERAL ===
[Comentario general de la evaluación]

=== FORTALEZAS ===
• [Fortaleza 1]
• [Fortaleza 2]

=== ÁREAS DE MEJORA ===
• [Área de mejora 1]
• [Área de mejora 2]

=== INSTRUCCIONES PARA EL DOCENTE ===
1. Revise la evaluación automática
2. Agregue sus comentarios y correcciones
3. Modifique los puntajes si es necesario
4. Use el botón "Solicitar nueva iteración" en la interfaz

---
Documento generado automáticamente por EDHack IA</pre>
                </div>
                
                <script>
                function copyContent() {
                    const content = document.getElementById('feedback-content');
                    navigator.clipboard.writeText(content.textContent).then(function() {
                        alert('¡Contenido copiado al portapapeles! Ahora pégalo en Google Docs.');
                    });
                }
                </script>
            </body>
            </html>
            """
            return content
        else:
            return jsonify({'error': 'Not available in production mode'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

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