import google.generativeai as genai
import os
import json
from datetime import datetime

class AIEvaluator:
    """Clase para evaluar textos usando la API de Gemini"""
    
    def __init__(self):
        # Configurar API de Gemini
        api_key = os.getenv('GEMINI_API_KEY')
        if not api_key:
            raise ValueError("GEMINI_API_KEY environment variable not set")
        
        genai.configure(api_key=api_key)
        # Usar la API disponible en la versión 0.2.2
        self.model_name = 'models/text-bison-001'
        
        # Criterios de evaluación hardcodeados para MVP
        self.evaluation_criteria = {
            'ortografia': {
                'peso': 20,
                'descripcion': 'Uso correcto de las reglas ortográficas'
            },
            'gramatica': {
                'peso': 20,
                'descripcion': 'Estructura gramatical y sintaxis correcta, ademas utiliza recursos ortograficos que le dan sentido a su texto'
            },
            'coherencia': {
                'peso': 25,
                'descripcion': 'Lógica, flujo de ideas y además, escribe su cuento organizando sus ideas de manera coherente y cohesionada'
            },
            'cohesion': {
                'peso': 10,
                'descripcion': 'Conexión entre párrafos y oraciones'
            },
            'vocabulario': {
                'peso': 10,
                'descripcion': 'Riqueza y precisión del vocabulario'
            },
            'estructura': {
                'peso': 10,
                'descripcion': 'Organización del texto (introducción, desarrollo, conclusión)'
            }
        }
    
    def evaluate_text(self, text):
        """Evaluar texto completo con IA"""
        try:
            prompt = self._build_evaluation_prompt(text)
            response = genai.generate_text(
                model=self.model_name,
                prompt=prompt,
                temperature=0.3,
                max_output_tokens=2000
            )
            
            # Procesar respuesta
            evaluation = self._parse_ai_response(response.result)
            evaluation['timestamp'] = datetime.now().isoformat()
            evaluation['original_text_length'] = len(text)
            evaluation['word_count'] = len(text.split())
            
            return evaluation
            
        except Exception as e:
            raise Exception(f"Error evaluating text with AI: {str(e)}")
    
    def re_evaluate_with_corrections(self, corrected_feedback):
        """Re-evaluar considerando correcciones del docente"""
        try:
            prompt = self._build_re_evaluation_prompt(corrected_feedback)
            response = genai.generate_text(
                model=self.model_name,
                prompt=prompt,
                temperature=0.3,
                max_output_tokens=2000
            )
            
            evaluation = self._parse_ai_response(response.result)
            evaluation['timestamp'] = datetime.now().isoformat()
            evaluation['type'] = 'correction_iteration'
            
            return evaluation
            
        except Exception as e:
            raise Exception(f"Error re-evaluating with corrections: {str(e)}")
    
    def _build_evaluation_prompt(self, text):
        """Construir prompt de evaluación principal"""
        criteria_text = "\n".join([
            f"- {criterio.upper()}: {info['descripcion']} (Peso: {info['peso']}%)"
            for criterio, info in self.evaluation_criteria.items()
        ])
        
        prompt = f"""
Eres un experto evaluador de textos académicos. Analiza el siguiente texto de un estudiante y proporciona una evaluación detallada.

CRITERIOS DE EVALUACIÓN:
{criteria_text}

TEXTO A EVALUAR:
{text}

INSTRUCCIONES:
1. Analiza el texto según cada criterio mencionado
2. Asigna una puntuación de 0-100 para cada criterio
3. Calcula la puntuación total ponderada
4. Proporciona comentarios específicos y constructivos
5. Sugiere al menos 3 áreas de mejora concretas
6. Identifica al menos 2 fortalezas del texto

FORMATO DE RESPUESTA (responder exactamente en este formato JSON):
{{
    "puntuacion_total": [0-100],
    "criterios": {{
        "ortografia": {{
            "puntuacion": [0-100],
            "comentario": "comentario específico",
            "ejemplos": ["ejemplo1", "ejemplo2"]
        }},
        "gramatica": {{
            "puntuacion": [0-100],
            "comentario": "comentario específico",
            "ejemplos": ["ejemplo1", "ejemplo2"]
        }},
        "coherencia": {{
            "puntuacion": [0-100],
            "comentario": "comentario específico",
            "ejemplos": ["ejemplo1", "ejemplo2"]
        }},
        "cohesion": {{
            "puntuacion": [0-100],
            "comentario": "comentario específico",
            "ejemplos": ["ejemplo1", "ejemplo2"]
        }},
        "vocabulario": {{
            "puntuacion": [0-100],
            "comentario": "comentario específico",
            "ejemplos": ["ejemplo1", "ejemplo2"]
        }},
        "estructura": {{
            "puntuacion": [0-100],
            "comentario": "comentario específico",
            "ejemplos": ["ejemplo1", "ejemplo2"]
        }}
    }},
    "fortalezas": ["fortaleza1", "fortaleza2"],
    "areas_mejora": ["mejora1", "mejora2", "mejora3"],
    "comentario_general": "comentario general constructivo",
    "nivel_sugerido": "Principiante/Intermedio/Avanzado"
}}
"""
        return prompt
    
    def _build_re_evaluation_prompt(self, corrected_feedback):
        """Construir prompt para re-evaluación con correcciones del docente"""
        prompt = f"""
Un docente ha revisado y corregido la retroalimentación anterior. Analiza las correcciones del docente y genera una nueva evaluación mejorada.

RETROALIMENTACIÓN CORREGIDA POR EL DOCENTE:
{corrected_feedback}

INSTRUCCIONES:
1. Incorpora las correcciones y sugerencias del docente
2. Mantén el mismo formato JSON de respuesta
3. Ajusta las puntuaciones si es necesario según las correcciones
4. Mejora los comentarios considerando la perspectiva del docente
5. Mantén un tono constructivo y pedagógico

Responde en el mismo formato JSON que la evaluación original.
"""
        return prompt
    
    def _parse_ai_response(self, response_text):
        """Parsear respuesta de IA y convertir a formato estructurado"""
        try:
            # Intentar parsear como JSON
            # Limpiar la respuesta de posibles caracteres extra
            cleaned_response = response_text.strip()
            
            # Buscar el JSON en la respuesta
            start_idx = cleaned_response.find('{')
            end_idx = cleaned_response.rfind('}') + 1
            
            if start_idx != -1 and end_idx != -1:
                json_str = cleaned_response[start_idx:end_idx]
                evaluation = json.loads(json_str)
                
                # Validar estructura mínima
                if 'puntuacion_total' in evaluation and 'criterios' in evaluation:
                    return evaluation
            
            # Si no se puede parsear como JSON, crear estructura básica
            return self._create_fallback_evaluation(response_text)
            
        except json.JSONDecodeError:
            return self._create_fallback_evaluation(response_text)
    
    def _create_fallback_evaluation(self, raw_response):
        """Crear evaluación básica si no se puede parsear la respuesta de IA"""
        return {
            'puntuacion_total': 75,  # Puntuación por defecto
            'criterios': {
                criterio: {
                    'puntuacion': 75,
                    'comentario': 'Evaluación automática - revisar manualmente',
                    'ejemplos': []
                }
                for criterio in self.evaluation_criteria.keys()
            },
            'fortalezas': ['Texto legible', 'Estructura básica presente'],
            'areas_mejora': ['Revisar evaluación manualmente', 'Proporcionar feedback específico'],
            'comentario_general': f'Respuesta de IA no pudo ser procesada correctamente. Respuesta original: {raw_response[:200]}...',
            'nivel_sugerido': 'Intermedio',
            'error': 'AI response parsing failed'
        }
    
    def get_evaluation_summary(self, evaluation):
        """Generar resumen de evaluación para mostrar al usuario"""
        if not evaluation:
            return "No hay evaluación disponible"
        
        total_score = evaluation.get('puntuacion_total', 0)
        level = evaluation.get('nivel_sugerido', 'No determinado')
        
        # Determinar calificación general
        if total_score >= 90:
            grade = "Excelente"
        elif total_score >= 80:
            grade = "Muy Bueno"
        elif total_score >= 70:
            grade = "Bueno"
        elif total_score >= 60:
            grade = "Regular"
        else:
            grade = "Necesita Mejora"
        
        summary = f"""
RESUMEN DE EVALUACIÓN
====================
Puntuación Total: {total_score}/100 ({grade})
Nivel Sugerido: {level}

FORTALEZAS:
{chr(10).join(['• ' + f for f in evaluation.get('fortalezas', [])])}

ÁREAS DE MEJORA:
{chr(10).join(['• ' + a for a in evaluation.get('areas_mejora', [])])}

COMENTARIO GENERAL:
{evaluation.get('comentario_general', 'Sin comentarios adicionales')}
"""
        return summary