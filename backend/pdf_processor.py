import fitz  # PyMuPDF
import pdfplumber
import re

class PDFProcessor:
    """Clase para procesar y extraer texto de archivos PDF"""
    
    def __init__(self):
        self.supported_formats = ['.pdf']
    
    def extract_text(self, pdf_path):
        """
        Extraer texto de un archivo PDF
        Usa PyMuPDF como método principal y pdfplumber como fallback
        """
        try:
            # Método principal: PyMuPDF (más rápido)
            return self._extract_with_pymupdf(pdf_path)
        except Exception as e:
            print(f"PyMuPDF failed, trying pdfplumber: {e}")
            try:
                # Método fallback: pdfplumber (más robusto)
                return self._extract_with_pdfplumber(pdf_path)
            except Exception as e2:
                raise Exception(f"Both extraction methods failed: PyMuPDF: {e}, pdfplumber: {e2}")
    
    def _extract_with_pymupdf(self, pdf_path):
        """Extraer texto usando PyMuPDF"""
        text = ""
        doc = fitz.open(pdf_path)
        
        for page_num in range(len(doc)):
            page = doc[page_num]
            text += page.get_text()
            text += "\n\n"  # Separador entre páginas
        
        doc.close()
        return self._clean_text(text)
    
    def _extract_with_pdfplumber(self, pdf_path):
        """Extraer texto usando pdfplumber"""
        text = ""
        
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text += page_text
                    text += "\n\n"  # Separador entre páginas
        
        return self._clean_text(text)
    
    def _clean_text(self, text):
        """Limpiar y normalizar el texto extraído"""
        if not text:
            return ""
        
        # Eliminar espacios excesivos
        text = re.sub(r'\s+', ' ', text)
        
        # Eliminar saltos de línea excesivos
        text = re.sub(r'\n\s*\n\s*\n+', '\n\n', text)
        
        # Limpiar caracteres extraños comunes en PDFs
        text = text.replace('\x00', '')  # Null characters
        text = text.replace('\ufeff', '')  # BOM
        
        # Normalizar espacios
        text = text.strip()
        
        return text
    
    def get_pdf_info(self, pdf_path):
        """Obtener información básica del PDF"""
        try:
            doc = fitz.open(pdf_path)
            info = {
                'pages': len(doc),
                'title': doc.metadata.get('title', 'Sin título'),
                'author': doc.metadata.get('author', 'Desconocido'),
                'subject': doc.metadata.get('subject', ''),
                'creator': doc.metadata.get('creator', ''),
                'producer': doc.metadata.get('producer', ''),
                'creation_date': doc.metadata.get('creationDate', ''),
                'modification_date': doc.metadata.get('modDate', '')
            }
            doc.close()
            return info
        except Exception as e:
            return {'error': f'Could not extract PDF info: {str(e)}'}
    
    def validate_pdf(self, pdf_path):
        """Validar si el archivo PDF es válido y legible"""
        try:
            doc = fitz.open(pdf_path)
            
            # Verificar que tenga al menos una página
            if len(doc) == 0:
                doc.close()
                return False, "PDF vacío - no contiene páginas"
            
            # Verificar que se pueda extraer texto de al menos una página
            text_found = False
            for page_num in range(min(3, len(doc))):  # Verificar solo las primeras 3 páginas
                page = doc[page_num]
                text = page.get_text().strip()
                if text:
                    text_found = True
                    break
            
            doc.close()
            
            if not text_found:
                return False, "PDF no contiene texto extraíble - podría ser solo imágenes"
            
            return True, "PDF válido"
            
        except Exception as e:
            return False, f"Error al validar PDF: {str(e)}"
    
    def extract_text_by_pages(self, pdf_path):
        """Extraer texto página por página (útil para análisis detallado)"""
        try:
            pages_text = []
            doc = fitz.open(pdf_path)
            
            for page_num in range(len(doc)):
                page = doc[page_num]
                page_text = self._clean_text(page.get_text())
                pages_text.append({
                    'page_number': page_num + 1,
                    'text': page_text,
                    'word_count': len(page_text.split()) if page_text else 0
                })
            
            doc.close()
            return pages_text
            
        except Exception as e:
            raise Exception(f"Error extracting text by pages: {str(e)}")
    
    def get_text_statistics(self, text):
        """Obtener estadísticas básicas del texto extraído"""
        if not text:
            return {
                'characters': 0,
                'words': 0,
                'sentences': 0,
                'paragraphs': 0,
                'lines': 0
            }
        
        # Contar elementos
        characters = len(text)
        words = len(text.split())
        
        # Contar oraciones (aproximado)
        sentences = len(re.findall(r'[.!?]+', text))
        
        # Contar párrafos
        paragraphs = len([p for p in text.split('\n\n') if p.strip()])
        
        # Contar líneas
        lines = len([line for line in text.split('\n') if line.strip()])
        
        return {
            'characters': characters,
            'words': words,
            'sentences': sentences,
            'paragraphs': paragraphs,
            'lines': lines
        }