import os
from typing import Dict, Any

class GoogleDocsManager:
    """Clase para gestionar documentos de Google Docs - Versión de desarrollo sin OAuth"""
    
    def __init__(self):
        self.dev_mode = os.getenv('DEV_MODE', 'true').lower() == 'true'
        if self.dev_mode:
            print("⚠️  GoogleDocsManager iniciado en modo desarrollo - OAuth deshabilitado")
        
    def create_feedback_document(self, student_name: str, evaluation_data: Dict[str, Any]) -> Dict[str, str]:
        """Crear documento de feedback en Google Docs (simulado en desarrollo)"""
        if self.dev_mode:
            # Simular creación de documento
            doc_id = f"dev_doc_{student_name.replace(' ', '_').lower()}"
            # En desarrollo, usar una URL local simulada
            doc_url = f"http://localhost:5000/api/preview-doc/{doc_id}"
            
            print(f"📝 [MODO DEV] Documento de feedback creado para {student_name}")
            print(f"🔗 [MODO DEV] URL simulada: {doc_url}")
            
            # Mostrar contenido que se habría incluido
            print("\n📋 Contenido del documento:")
            print(f"Estudiante: {student_name}")
            print(f"Fecha: {evaluation_data.get('timestamp', 'N/A')}")
            print(f"Puntuación total: {evaluation_data.get('total_score', 'N/A')}/100")
            
            if 'scores' in evaluation_data:
                print("\nDetalles por criterio:")
                for criterion, score in evaluation_data['scores'].items():
                    print(f"  - {criterion}: {score}")
            
            if 'feedback' in evaluation_data:
                print(f"\nComentarios: {evaluation_data['feedback'][:200]}...")
            
            return {
                'document_id': doc_id,
                'document_url': doc_url,
                'status': 'created_dev_mode'
            }
        else:
            # Aquí iría la implementación real con OAuth
            raise NotImplementedError("OAuth implementation needed for production mode")
    
    def update_document_permissions(self, document_id: str, email: str = None) -> bool:
        """Actualizar permisos del documento (simulado en desarrollo)"""
        if self.dev_mode:
            print(f"🔐 [MODO DEV] Permisos actualizados para documento {document_id}")
            if email:
                print(f"📧 [MODO DEV] Acceso concedido a: {email}")
            return True
        else:
            raise NotImplementedError("OAuth implementation needed for production mode")
    
    def get_document_content(self, document_id: str) -> str:
        """Obtener contenido del documento (simulado en desarrollo)"""
        if self.dev_mode:
            print(f"📖 [MODO DEV] Obteniendo contenido del documento {document_id}")
            return f"[CONTENIDO SIMULADO] Documento ID: {document_id} - Correcciones del docente aplicadas"
        else:
            raise NotImplementedError("OAuth implementation needed for production mode")
    
    def update_document(self, document_id: str, new_content: str) -> bool:
        """Actualizar contenido del documento (simulado en desarrollo)"""
        if self.dev_mode:
            print(f"✏️  [MODO DEV] Actualizando documento {document_id}")
            print(f"📝 [MODO DEV] Nuevo contenido (primeros 200 chars): {new_content[:200]}...")
            return True
        else:
            raise NotImplementedError("OAuth implementation needed for production mode")