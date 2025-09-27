from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import json
from datetime import datetime

class GoogleDocsManager:
    """Clase para gestionar documentos de Google Docs"""
    
    # Scopes necesarios para crear y editar documentos
    SCOPES = [
        'https://www.googleapis.com/auth/documents',
        'https://www.googleapis.com/auth/drive.file'
    ]
    
    def __init__(self):
        self.creds = None
        self.docs_service = None
        self.drive_service = None
        self._authenticate()
    
    def _authenticate(self):
        """Autenticar con Google APIs"""
        # Cargar credenciales existentes
        token_path = '../config/token.json'
        credentials_path = '../config/credentials.json'
        
        if os.path.exists(token_path):
            self.creds = Credentials.from_authorized_user_file(token_path, self.SCOPES)
        
        # Si no hay credenciales válidas, solicitar autorización
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(credentials_path):
                    raise FileNotFoundError(
                        f"Credentials file not found at {credentials_path}. "
                        "Please download from Google Cloud Console and place it there."
                    )
                
                flow = InstalledAppFlow.from_client_secrets_file(
                    credentials_path, self.SCOPES)
                self.creds = flow.run_local_server(port=0)
            
            # Guardar credenciales para próximas ejecuciones
            os.makedirs(os.path.dirname(token_path), exist_ok=True)
            with open(token_path, 'w') as token:
                token.write(self.creds.to_json())
        
        # Construir servicios de API
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)
    
    def create_feedback_document(self, evaluation, session_id):
        """Crear documento de Google Docs con retroalimentación"""
        try:
            # Crear título del documento
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
            title = f"Retroalimentación EDHack - {session_id[:8]} - {timestamp}"
            
            # Crear documento
            document = {
                'title': title
            }
            
            doc = self.docs_service.documents().create(body=document).execute()
            doc_id = doc.get('documentId')
            
            # Agregar contenido al documento
            content = self._format_evaluation_for_docs(evaluation)
            self._insert_content_to_document(doc_id, content)
            
            # Hacer el documento editable para cualquiera con el enlace (MVP - sin seguridad robusta)
            self._make_document_editable(doc_id)
            
            return doc_id
            
        except Exception as e:
            raise Exception(f"Error creating Google Docs document: {str(e)}")
    
    def _format_evaluation_for_docs(self, evaluation):
        """Formatear evaluación para documento de Google Docs"""
        content = []
        
        # Título principal
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': 'RETROALIMENTACIÓN AUTOMÁTICA - EDHack IA\n\n'
            }
        })
        
        # Puntuación total
        total_score = evaluation.get('puntuacion_total', 0)
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': f'PUNTUACIÓN TOTAL: {total_score}/100\n'
            }
        })
        
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': f'NIVEL SUGERIDO: {evaluation.get("nivel_sugerido", "No determinado")}\n\n'
            }
        })
        
        # Criterios detallados
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': 'EVALUACIÓN POR CRITERIOS:\n'
            }
        })
        
        criterios = evaluation.get('criterios', {})
        for criterio, datos in criterios.items():
            puntuacion = datos.get('puntuacion', 0)
            comentario = datos.get('comentario', 'Sin comentario')
            ejemplos = datos.get('ejemplos', [])
            
            content.append({
                'insertText': {
                    'location': {'index': 1},
                    'text': f'\n{criterio.upper()}: {puntuacion}/100\n'
                }
            })
            
            content.append({
                'insertText': {
                    'location': {'index': 1},
                    'text': f'Comentario: {comentario}\n'
                }
            })
            
            if ejemplos:
                content.append({
                    'insertText': {
                        'location': {'index': 1},
                        'text': f'Ejemplos: {", ".join(ejemplos)}\n'
                    }
                })
        
        # Fortalezas
        fortalezas = evaluation.get('fortalezas', [])
        if fortalezas:
            content.append({
                'insertText': {
                    'location': {'index': 1},
                    'text': '\nFORTALEZAS IDENTIFICADAS:\n'
                }
            })
            
            for fortaleza in fortalezas:
                content.append({
                    'insertText': {
                        'location': {'index': 1},
                        'text': f'• {fortaleza}\n'
                    }
                })
        
        # Áreas de mejora
        areas_mejora = evaluation.get('areas_mejora', [])
        if areas_mejora:
            content.append({
                'insertText': {
                    'location': {'index': 1},
                    'text': '\nÁREAS DE MEJORA:\n'
                }
            })
            
            for area in areas_mejora:
                content.append({
                    'insertText': {
                        'location': {'index': 1},
                        'text': f'• {area}\n'
                    }
                })
        
        # Comentario general
        comentario_general = evaluation.get('comentario_general', '')
        if comentario_general:
            content.append({
                'insertText': {
                    'location': {'index': 1},
                    'text': f'\nCOMENTARIO GENERAL:\n{comentario_general}\n\n'
                }
            })
        
        # Instrucciones para el docente
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': '--- INSTRUCCIONES PARA EL DOCENTE ---\n'
            }
        })
        
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': 'Por favor, revise esta retroalimentación y haga las correcciones necesarias.\n'
            }
        })
        
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': 'Una vez que haya terminado de editar, use el sistema para aprobar o solicitar una nueva iteración.\n\n'
            }
        })
        
        content.append({
            'insertText': {
                'location': {'index': 1},
                'text': f'Timestamp: {evaluation.get("timestamp", datetime.now().isoformat())}\n'
            }
        })
        
        return content
    
    def _insert_content_to_document(self, doc_id, content_requests):
        """Insertar contenido en documento de Google Docs"""
        try:
            # Ejecutar todas las inserciones en orden inverso para mantener las posiciones correctas
            for request in reversed(content_requests):
                self.docs_service.documents().batchUpdate(
                    documentId=doc_id,
                    body={'requests': [request]}
                ).execute()
        except Exception as e:
            raise Exception(f"Error inserting content to document: {str(e)}")
    
    def _make_document_editable(self, doc_id):
        """Hacer documento editable para cualquiera con el enlace (MVP only)"""
        try:
            # Configurar permisos para que cualquiera con el enlace pueda editar
            permission = {
                'type': 'anyone',
                'role': 'writer'
            }
            
            self.drive_service.permissions().create(
                fileId=doc_id,
                body=permission
            ).execute()
            
        except Exception as e:
            print(f"Warning: Could not set document permissions: {str(e)}")
            # No fallar si no se pueden configurar permisos
    
    def get_document_content(self, doc_id):
        """Obtener contenido actual del documento"""
        try:
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
            # Extraer texto del documento
            text_content = ""
            content = document.get('body', {}).get('content', [])
            
            for element in content:
                if 'paragraph' in element:
                    paragraph = element['paragraph']
                    for text_run in paragraph.get('elements', []):
                        if 'textRun' in text_run:
                            text_content += text_run['textRun']['content']
            
            return text_content
            
        except Exception as e:
            raise Exception(f"Error getting document content: {str(e)}")
    
    def update_document(self, doc_id, new_evaluation):
        """Actualizar documento con nueva evaluación"""
        try:
            # Obtener documento actual
            document = self.docs_service.documents().get(documentId=doc_id).execute()
            
            # Agregar separador y nueva evaluación
            separator = f"\n\n--- NUEVA ITERACIÓN ({datetime.now().strftime('%Y-%m-%d %H:%M')}) ---\n\n"
            
            requests = [{
                'insertText': {
                    'location': {'index': len(document.get('body', {}).get('content', []))},
                    'text': separator
                }
            }]
            
            # Agregar nueva evaluación
            new_content = self._format_evaluation_for_docs(new_evaluation)
            requests.extend(new_content)
            
            # Aplicar cambios
            self.docs_service.documents().batchUpdate(
                documentId=doc_id,
                body={'requests': requests}
            ).execute()
            
        except Exception as e:
            raise Exception(f"Error updating document: {str(e)}")
    
    def get_document_url(self, doc_id):
        """Obtener URL pública del documento"""
        return f"https://docs.google.com/document/d/{doc_id}/edit"
    
    def list_user_documents(self, query="EDHack"):
        """Listar documentos del usuario (para debugging/testing)"""
        try:
            results = self.drive_service.files().list(
                q=f"name contains '{query}' and mimeType='application/vnd.google-apps.document'",
                pageSize=10,
                fields="nextPageToken, files(id, name, createdTime, modifiedTime)"
            ).execute()
            
            return results.get('files', [])
            
        except Exception as e:
            raise Exception(f"Error listing documents: {str(e)}")