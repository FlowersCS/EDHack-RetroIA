import pytest
import tempfile
import os
from backend.app import app
from backend.pdf_processor import PDFProcessor
from backend.ai_evaluator import AIEvaluator

@pytest.fixture
def client():
    """Fixture para cliente de pruebas de Flask"""
    app.config['TESTING'] = True
    app.config['UPLOAD_FOLDER'] = tempfile.mkdtemp()
    
    with app.test_client() as client:
        with app.app_context():
            yield client

@pytest.fixture
def pdf_processor():
    """Fixture para PDFProcessor"""
    return PDFProcessor()

@pytest.fixture
def sample_pdf_path():
    """Fixture para ruta de PDF de muestra (mock)"""
    # En un test real, aquí crearías un PDF de muestra
    return None

class TestHealthCheck:
    """Tests para el endpoint de health check"""
    
    def test_health_check(self, client):
        """Test del endpoint de health check"""
        response = client.get('/api/health')
        assert response.status_code == 200
        data = response.get_json()
        assert data['status'] == 'ok'
        assert 'EDHack IA API is running' in data['message']

class TestPDFProcessor:
    """Tests para el procesador de PDFs"""
    
    def test_init(self, pdf_processor):
        """Test de inicialización del PDFProcessor"""
        assert pdf_processor.supported_formats == ['.pdf']
    
    def test_clean_text(self, pdf_processor):
        """Test de limpieza de texto"""
        dirty_text = "  Texto   con    espacios  \n\n\n\n  extras  "
        clean_text = pdf_processor._clean_text(dirty_text)
        assert clean_text == "Texto con espacios extras"
    
    def test_clean_text_empty(self, pdf_processor):
        """Test de limpieza de texto vacío"""
        assert pdf_processor._clean_text("") == ""
        assert pdf_processor._clean_text(None) == ""
    
    def test_get_text_statistics(self, pdf_processor):
        """Test de estadísticas de texto"""
        text = "Hola mundo. ¿Cómo estás? ¡Bien!\n\nEste es otro párrafo."
        stats = pdf_processor.get_text_statistics(text)
        
        assert stats['words'] > 0
        assert stats['characters'] > 0
        assert stats['sentences'] > 0
        assert stats['paragraphs'] > 0
    
    def test_get_text_statistics_empty(self, pdf_processor):
        """Test de estadísticas de texto vacío"""
        stats = pdf_processor.get_text_statistics("")
        expected = {
            'characters': 0,
            'words': 0,
            'sentences': 0,
            'paragraphs': 0,
            'lines': 0
        }
        assert stats == expected

class TestAIEvaluator:
    """Tests para el evaluador de IA"""
    
    def test_evaluation_criteria(self):
        """Test de criterios de evaluación hardcodeados"""
        # Skip si no hay API key configurada
        if not os.getenv('GEMINI_API_KEY'):
            pytest.skip("GEMINI_API_KEY not set")
        
        evaluator = AIEvaluator()
        
        # Verificar que los criterios están definidos
        assert 'ortografia' in evaluator.evaluation_criteria
        assert 'gramatica' in evaluator.evaluation_criteria
        assert 'coherencia' in evaluator.evaluation_criteria
        assert 'cohesion' in evaluator.evaluation_criteria
        assert 'vocabulario' in evaluator.evaluation_criteria
        assert 'estructura' in evaluator.evaluation_criteria
        
        # Verificar que todos tienen peso y descripción
        for criterio, info in evaluator.evaluation_criteria.items():
            assert 'peso' in info
            assert 'descripcion' in info
            assert isinstance(info['peso'], int)
            assert info['peso'] > 0
    
    def test_create_fallback_evaluation(self):
        """Test de evaluación de fallback"""
        if not os.getenv('GEMINI_API_KEY'):
            pytest.skip("GEMINI_API_KEY not set")
            
        evaluator = AIEvaluator()
        fallback = evaluator._create_fallback_evaluation("Test response")
        
        assert 'puntuacion_total' in fallback
        assert 'criterios' in fallback
        assert 'fortalezas' in fallback
        assert 'areas_mejora' in fallback
        assert 'comentario_general' in fallback
        assert 'nivel_sugerido' in fallback
        assert fallback['error'] == 'AI response parsing failed'

class TestFileUpload:
    """Tests para subida de archivos"""
    
    def test_upload_no_file(self, client):
        """Test de subida sin archivo"""
        response = client.post('/api/upload-pdf')
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'No file provided'
    
    def test_upload_empty_filename(self, client):
        """Test de subida con nombre de archivo vacío"""
        data = {'file': (tempfile.NamedTemporaryFile(), '')}
        response = client.post('/api/upload-pdf', data=data)
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'No file selected'

class TestEvaluationEndpoint:
    """Tests para el endpoint de evaluación"""
    
    def test_evaluate_missing_data(self, client):
        """Test de evaluación sin datos requeridos"""
        response = client.post('/api/evaluate', json={})
        assert response.status_code == 400
        data = response.get_json()
        assert data['error'] == 'Missing session_id or filename'
    
    def test_evaluate_with_session_and_filename(self, client):
        """Test de evaluación con session_id y filename válidos"""
        # Este test requeriría un archivo PDF real y configuración completa
        # Para MVP, lo dejamos como placeholder
        pass

class TestUtilityFunctions:
    """Tests para funciones utilitarias"""
    
    def test_secure_filename(self):
        """Test de función secure_filename"""
        from backend.app import secure_filename
        
        # Test casos normales
        assert secure_filename("test.pdf") == "test.pdf"
        assert secure_filename("Test_File-1.pdf") == "Test_File-1.pdf"
        
        # Test caracteres especiales
        result = secure_filename("test@#$%^&*().pdf")
        assert "@#$%^&*()" not in result
    
    def test_generate_session_id(self):
        """Test de generación de session ID"""
        from backend.app import generate_session_id
        
        session_id1 = generate_session_id()
        session_id2 = generate_session_id()
        
        # Los IDs deben ser únicos
        assert session_id1 != session_id2
        
        # Deben tener formato UUID
        import uuid
        try:
            uuid.UUID(session_id1)
            uuid.UUID(session_id2)
        except ValueError:
            pytest.fail("Generated session IDs are not valid UUIDs")

# Tests de integración (requieren configuración completa)
@pytest.mark.integration
class TestIntegration:
    """Tests de integración que requieren APIs externas configuradas"""
    
    @pytest.mark.skipif(not os.getenv('GEMINI_API_KEY'), reason="GEMINI_API_KEY not set")
    def test_full_evaluation_flow(self, client):
        """Test del flujo completo de evaluación"""
        # Este test requeriría:
        # 1. Un PDF de muestra
        # 2. API de Gemini configurada
        # 3. Google Docs API configurada
        # Para MVP, lo marcamos como placeholder
        pass
    
    def test_google_docs_integration(self):
        """Test de integración con Google Docs"""
        # Requiere credenciales de Google configuradas
        # Para MVP, lo marcamos como placeholder
        pass

if __name__ == '__main__':
    pytest.main([__file__])