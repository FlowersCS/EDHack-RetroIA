import os
import json
from datetime import datetime
import random

class AIEvaluator:
    """Clase para evaluar textos usando simulación para desarrollo"""
    
    def __init__(self):
        # Modo de desarrollo - no necesita API key real
        print("🔧 AIEvaluator en modo desarrollo - sin API real")
        
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
        """Evaluar texto completo con IA simulada"""
        try:
            print(f"🤖 Evaluando texto de {len(text.split())} palabras...")
            
            # Simular evaluación basada en características del texto
            word_count = len(text.split())
            sentence_count = text.count('.') + text.count('!') + text.count('?')
            
            # Generar puntajes realistas basados en el contenido
            evaluation = {
                'criterios': {
                    'ortografia': {
                        'puntaje': min(95, 80 + random.randint(0, 15)),
                        'comentario': 'Muy buen uso de las reglas ortográficas. Se observa dominio de acentuación y signos de puntuación.',
                        'peso': 20
                    },
                    'gramatica': {
                        'puntaje': min(90, 75 + random.randint(0, 15)),
                        'comentario': 'Estructura gramatical adecuada con oraciones bien formadas. Buen uso de tiempos verbales.',
                        'peso': 20
                    },
                    'coherencia': {
                        'puntaje': min(85, 70 + random.randint(0, 15)),
                        'comentario': 'Las ideas se presentan de manera lógica y fluida. La historia tiene un hilo conductor claro.',
                        'peso': 25
                    },
                    'cohesion': {
                        'puntaje': min(80, 65 + random.randint(0, 15)),
                        'comentario': 'Buena conexión entre oraciones y párrafos. Uso apropiado de conectores.',
                        'peso': 10
                    },
                    'vocabulario': {
                        'puntaje': min(85, 70 + random.randint(0, 15)),
                        'comentario': 'Vocabulario variado y apropiado para el nivel. Uso creativo de adjetivos descriptivos.',
                        'peso': 10
                    },
                    'estructura': {
                        'puntaje': min(80, 65 + random.randint(0, 15)),
                        'comentario': 'Estructura narrativa clara con inicio, desarrollo y desenlace bien definidos.',
                        'peso': 10
                    }
                },
                'puntaje_total': 0,
                'comentario_general': 'Excelente trabajo narrativo que muestra creatividad y dominio de las habilidades de escritura. El cuento presenta una historia entretenida con personajes bien desarrollados.',
                'fortalezas': [
                    'Creatividad en el desarrollo de la historia',
                    'Uso apropiado del lenguaje descriptivo',
                    'Estructura narrativa coherente'
                ],
                'areas_mejora': [
                    'Podría ampliar algunos diálogos entre personajes',
                    'Desarrollar más detalles del escenario'
                ],
                'timestamp': datetime.now().isoformat(),
                'original_text_length': len(text),
                'word_count': word_count,
                'sentence_count': sentence_count
            }
            
            # Calcular puntaje total ponderado
            total = 0
            for criterio, data in evaluation['criterios'].items():
                total += data['puntaje'] * data['peso'] / 100
            evaluation['puntaje_total'] = round(total, 1)
            
            print(f"✅ Evaluación completada - Puntaje total: {evaluation['puntaje_total']}/100")
            return evaluation
            
        except Exception as e:
            raise Exception(f"Error evaluating text with AI: {str(e)}")
    
    def re_evaluate_with_corrections(self, corrected_feedback):
        """Re-evaluar considerando correcciones del docente"""
        try:
            print("🔄 Re-evaluando con correcciones del docente...")
            
            # Simular re-evaluación mejorada
            evaluation = {
                'criterios': {
                    'ortografia': {
                        'puntaje': 90,
                        'comentario': 'Mejorado significativamente tras las correcciones del docente.',
                        'peso': 20
                    },
                    'gramatica': {
                        'puntaje': 88,
                        'comentario': 'Las correcciones han fortalecido la estructura gramatical.',
                        'peso': 20
                    },
                    'coherencia': {
                        'puntaje': 92,
                        'comentario': 'Excelente integración de las sugerencias de coherencia.',
                        'peso': 25
                    },
                    'cohesion': {
                        'puntaje': 85,
                        'comentario': 'Mayor fluidez tras incorporar las correcciones.',
                        'peso': 10
                    },
                    'vocabulario': {
                        'puntaje': 87,
                        'comentario': 'Vocabulario enriquecido con las sugerencias.',
                        'peso': 10
                    },
                    'estructura': {
                        'puntaje': 89,
                        'comentario': 'Estructura mejorada considerablemente.',
                        'peso': 10
                    }
                },
                'puntaje_total': 89.5,
                'comentario_general': 'Excelente progreso tras incorporar las correcciones del docente.',
                'timestamp': datetime.now().isoformat(),
                'type': 'correction_iteration'
            }
            
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