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
app.config['UPLOAD_FOLDER'] = '../uploads'
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
            # Obtener feedback corregido y re-evaluar
            corrected_feedback = docs_manager.get_document_content(doc_id)
            new_evaluation = ai_evaluator.re_evaluate_with_corrections(corrected_feedback)
            
            # Actualizar documento
            docs_manager.update_document(doc_id, new_evaluation)
            
            return jsonify({
                'success': True,
                'message': 'Feedback updated with corrections',
                'updated_evaluation': new_evaluation
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

@app.route('/api/preview-doc/<doc_id>')
def preview_document(doc_id):
    """Previsualizar documento en modo desarrollo"""
    if os.getenv('DEV_MODE') == 'true':
        # Generar contenido simulado del documento
        content = f"""
        <html>
        <head><title>Documento EDHack IA - {doc_id}</title></head>
        <body style="font-family: Arial, sans-serif; margin: 40px; line-height: 1.6;">
            <h1>📝 Documento de Retroalimentación</h1>
            <p><strong>Documento ID:</strong> {doc_id}</p>
            <p><strong>Modo:</strong> Desarrollo (Simulado)</p>
            
            <h2>📊 Evaluación Automática</h2>
            <p>Este es un documento simulado para desarrollo. En producción, aquí aparecería el contenido real generado por la IA con la evaluación detallada del texto del estudiante.</p>
            
            <h3>Instrucciones para el Docente:</h3>
            <ul>
                <li>Revise la evaluación automática</li>
                <li>Agregue sus comentarios y correcciones</li>
                <li>Use el botón "Solicitar nueva iteración" en la interfaz</li>
            </ul>
            
            <div style="background: #f0f0f0; padding: 20px; margin: 20px 0; border-left: 4px solid #007bff;">
                <h4>💡 Nota de Desarrollo</h4>
                <p>En modo de desarrollo no se conecta a Google Docs real. Este es un contenido simulado para pruebas.</p>
            </div>
        </body>
        </html>
        """
        return content
    else:
        return redirect(f'https://docs.google.com/document/d/{doc_id}/edit')

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