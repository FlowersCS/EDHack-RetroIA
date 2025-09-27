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
            # Generar contenido de retroalimentación
            feedback_content = self._generate_feedback_content(student_name, evaluation_data)
            
            # Para demostración, crear una página intermedia con el contenido
            doc_id = f"demo_{student_name.replace(' ', '_').lower()}"
            
            # URL a nuestra página intermedia que mostrará el contenido y un botón para crear Google Docs
            doc_url = f"http://localhost:5000/api/feedback-helper/{doc_id}?student={student_name.replace(' ', '%20')}"
            
            print(f"📝 [MODO DEV] Documento de feedback creado para {student_name}")
            print(f"🔗 [MODO DEV] URL de Google Docs: {doc_url}")
            print("✅ [MODO DEV] Esta URL creará un nuevo documento de Google Docs")
            print("\n" + "="*60)
            print("📋 CONTENIDO PARA COPIAR AL DOCUMENTO:")
            print("="*60)
            print(feedback_content)
            print("="*60)
            print("ℹ️  Copia este contenido y pégalo en el documento de Google Docs que se abrirá")
            print("="*60)
            
            return {
                'document_id': doc_id,
                'document_url': doc_url,
                'status': 'created_dev_mode'
            }
        else:
            # Aquí iría la implementación real con OAuth
            raise NotImplementedError("OAuth implementation needed for production mode")
    
    def _generate_feedback_content(self, student_name: str, evaluation_data: Dict[str, Any]) -> str:
        """Generar contenido de retroalimentación formateado"""
        content = f"""
📝 RETROALIMENTACIÓN AUTOMÁTICA EDHack IA

ESTUDIANTE: {student_name}
FECHA: {evaluation_data.get('timestamp', 'N/A')}
PUNTAJE TOTAL: {evaluation_data.get('puntaje_total', 'N/A')}/100

=== EVALUACIÓN DETALLADA ===
"""
        
        # Agregar criterios de evaluación
        if 'criterios' in evaluation_data:
            for criterio, data in evaluation_data['criterios'].items():
                content += f"""
{criterio.upper()}: {data.get('puntaje', 'N/A')} puntos (Peso: {data.get('peso', 'N/A')}%)
Comentario: {data.get('comentario', 'Sin comentario')}
"""
        
        # Agregar comentario general
        if 'comentario_general' in evaluation_data:
            content += f"""
=== COMENTARIO GENERAL ===
{evaluation_data['comentario_general']}
"""
        
        # Agregar fortalezas
        if 'fortalezas' in evaluation_data:
            content += "\n=== FORTALEZAS ===\n"
            for fortaleza in evaluation_data['fortalezas']:
                content += f"• {fortaleza}\n"
        
        # Agregar áreas de mejora
        if 'areas_mejora' in evaluation_data:
            content += "\n=== ÁREAS DE MEJORA ===\n"
            for area in evaluation_data['areas_mejora']:
                content += f"• {area}\n"
        
        content += """
=== INSTRUCCIONES PARA EL DOCENTE ===
1. Revise la evaluación automática
2. Agregue sus comentarios y correcciones
3. Modifique los puntajes si es necesario
4. Use el botón "Solicitar nueva iteración" en la interfaz para generar una versión mejorada

---
Documento generado automáticamente por EDHack IA
"""
        
        return content
    
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