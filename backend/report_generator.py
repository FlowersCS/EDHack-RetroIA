import json
from datetime import datetime
from jinja2 import Template

class ReportGenerator:
    """Clase para generar reportes finales personalizados"""
    
    def __init__(self):
        self.report_templates = {
            'estudiante': self._get_student_template(),
            'familia': self._get_family_template(),
            'docente': self._get_teacher_template()
        }
    
    def generate_final_report(self, final_feedback, session_id):
        """Generar reportes finales para todos los stakeholders"""
        try:
            # Extraer información relevante del feedback final
            report_data = self._extract_report_data(final_feedback, session_id)
            
            # Generar reportes para cada audiencia
            reports = {}
            for audience, template in self.report_templates.items():
                reports[audience] = self._generate_report_for_audience(template, report_data, audience)
            
            # Metadata del reporte
            reports['metadata'] = {
                'session_id': session_id,
                'generated_at': datetime.now().isoformat(),
                'version': '1.0',
                'system': 'EDHack IA MVP'
            }
            
            return reports
            
        except Exception as e:
            raise Exception(f"Error generating final report: {str(e)}")
    
    def _extract_report_data(self, feedback_text, session_id):
        """Extraer datos estructurados del feedback final"""
        # En un MVP, hacemos parsing simple del texto
        # En una versión completa, esto sería más sofisticado
        
        data = {
            'session_id': session_id,
            'timestamp': datetime.now(),
            'feedback_text': feedback_text,
            'word_count': len(feedback_text.split()),
            'character_count': len(feedback_text)
        }
        
        # Intentar extraer puntuación si está presente
        try:
            import re
            score_match = re.search(r'PUNTUACIÓN TOTAL:\s*(\d+)/100', feedback_text)
            if score_match:
                data['total_score'] = int(score_match.group(1))
            else:
                data['total_score'] = None
            
            # Extraer nivel si está presente
            level_match = re.search(r'NIVEL SUGERIDO:\s*([^\n]+)', feedback_text)
            if level_match:
                data['suggested_level'] = level_match.group(1).strip()
            else:
                data['suggested_level'] = 'No determinado'
            
            # Extraer fortalezas
            fortalezas_section = re.search(r'FORTALEZAS IDENTIFICADAS:(.*?)(?=ÁREAS DE MEJORA:|$)', feedback_text, re.DOTALL)
            if fortalezas_section:
                fortalezas_text = fortalezas_section.group(1)
                data['fortalezas'] = [line.strip().lstrip('•').strip() 
                                    for line in fortalezas_text.split('\n') 
                                    if line.strip() and '•' in line]
            else:
                data['fortalezas'] = []
            
            # Extraer áreas de mejora
            mejoras_section = re.search(r'ÁREAS DE MEJORA:(.*?)(?=COMENTARIO GENERAL:|$)', feedback_text, re.DOTALL)
            if mejoras_section:
                mejoras_text = mejoras_section.group(1)
                data['areas_mejora'] = [line.strip().lstrip('•').strip() 
                                      for line in mejoras_text.split('\n') 
                                      if line.strip() and '•' in line]
            else:
                data['areas_mejora'] = []
            
            # Extraer comentario general
            comentario_match = re.search(r'COMENTARIO GENERAL:\s*([^---]+)', feedback_text, re.DOTALL)
            if comentario_match:
                data['comentario_general'] = comentario_match.group(1).strip()
            else:
                data['comentario_general'] = 'Sin comentario general disponible'
                
        except Exception as e:
            print(f"Warning: Could not extract structured data from feedback: {e}")
            data.update({
                'total_score': None,
                'suggested_level': 'No determinado',
                'fortalezas': [],
                'areas_mejora': [],
                'comentario_general': 'Error al procesar feedback estructurado'
            })
        
        return data
    
    def _generate_report_for_audience(self, template, data, audience):
        """Generar reporte específico para una audiencia"""
        try:
            # Preparar datos específicos para la audiencia
            context = self._prepare_context_for_audience(data, audience)
            
            # Renderizar template
            jinja_template = Template(template)
            report_content = jinja_template.render(**context)
            
            return {
                'audience': audience,
                'content': report_content,
                'format': 'text/markdown',
                'generated_at': datetime.now().isoformat()
            }
            
        except Exception as e:
            return {
                'audience': audience,
                'content': f'Error generando reporte para {audience}: {str(e)}',
                'format': 'text/plain',
                'generated_at': datetime.now().isoformat(),
                'error': True
            }
    
    def _prepare_context_for_audience(self, data, audience):
        """Preparar contexto específico según la audiencia"""
        base_context = data.copy()
        
        # Formatear fecha de manera legible
        if isinstance(base_context.get('timestamp'), datetime):
            base_context['fecha_readable'] = base_context['timestamp'].strftime('%d de %B de %Y a las %H:%M')
        else:
            base_context['fecha_readable'] = 'Fecha no disponible'
        
        # Determinar calificación cualitativa
        score = base_context.get('total_score')
        if score is not None:
            if score >= 90:
                base_context['calificacion_cualitativa'] = 'Excelente'
                base_context['emoji_calificacion'] = '🌟'
            elif score >= 80:
                base_context['calificacion_cualitativa'] = 'Muy Bueno'
                base_context['emoji_calificacion'] = '👍'
            elif score >= 70:
                base_context['calificacion_cualitativa'] = 'Bueno'
                base_context['emoji_calificacion'] = '✅'
            elif score >= 60:
                base_context['calificacion_cualitativa'] = 'Regular'
                base_context['emoji_calificacion'] = '⚠️'
            else:
                base_context['calificacion_cualitativa'] = 'Necesita Mejora'
                base_context['emoji_calificacion'] = '📚'
        else:
            base_context['calificacion_cualitativa'] = 'No evaluado'
            base_context['emoji_calificacion'] = '❓'
        
        # Contexto específico por audiencia
        if audience == 'estudiante':
            base_context['saludo'] = '¡Hola!'
            base_context['tono'] = 'motivacional'
        elif audience == 'familia':
            base_context['saludo'] = 'Estimada familia'
            base_context['tono'] = 'informativo'
        elif audience == 'docente':
            base_context['saludo'] = 'Estimado/a docente'
            base_context['tono'] = 'técnico'
        
        return base_context
    
    def _get_student_template(self):
        """Template de reporte para estudiantes"""
        return """# 📝 Tu Evaluación de Escritura

{{ saludo }}, aquí tienes los resultados de tu evaluación:

## {{ emoji_calificacion }} Puntuación: {{ total_score if total_score else 'En proceso' }}/100
**Calificación: {{ calificacion_cualitativa }}**
**Nivel: {{ suggested_level }}**

---

## 🌟 ¡Tus Fortalezas!
{% if fortalezas %}
{% for fortaleza in fortalezas %}
- {{ fortaleza }}
{% endfor %}
{% else %}
- ¡Sigue trabajando para descubrir tus fortalezas!
{% endif %}

## 📚 Áreas para Crecer
{% if areas_mejora %}
{% for area in areas_mejora %}
- {{ area }}
{% endfor %}
{% else %}
- ¡Continúa practicando para mejorar!
{% endif %}

## 💭 Comentario Personal
{{ comentario_general }}

---

### 🎯 Próximos Pasos
1. **Celebra tus fortalezas** - ¡has hecho un buen trabajo!
2. **Enfócate en una mejora a la vez** - el progreso paso a paso es el mejor
3. **Practica regularmente** - la escritura mejora con la práctica constante
4. **Pide ayuda cuando la necesites** - tu docente está aquí para apoyarte

---
*Evaluación generada el {{ fecha_readable }}*
*Sistema EDHack IA - Versión MVP*
"""
    
    def _get_family_template(self):
        """Template de reporte para familias"""
        return """# 👨‍👩‍👧‍👦 Reporte de Evaluación de Escritura

{{ saludo }},

Les compartimos los resultados de la evaluación de escritura de su hijo/a:

## 📊 Resumen de Resultados
- **Puntuación Total:** {{ total_score if total_score else 'En evaluación' }}/100 ({{ calificacion_cualitativa }})
- **Nivel Sugerido:** {{ suggested_level }}
- **Fecha de Evaluación:** {{ fecha_readable }}

---

## ✅ Fortalezas Identificadas
{% if fortalezas %}
Su hijo/a demuestra competencias en:
{% for fortaleza in fortalezas %}
- {{ fortaleza }}
{% endfor %}
{% else %}
- Las fortalezas se están desarrollando progresivamente
{% endif %}

## 🎯 Oportunidades de Mejora
{% if areas_mejora %}
Las siguientes áreas pueden beneficiarse de apoyo adicional:
{% for area in areas_mejora %}
- {{ area }}
{% endfor %}
{% else %}
- Su hijo/a está en un buen camino de desarrollo
{% endif %}

## 📝 Evaluación Detallada
{{ comentario_general }}

---

## 🏠 Cómo Pueden Ayudar en Casa

### Actividades Recomendadas:
1. **Lectura diaria** - 15-20 minutos de lectura familiar
2. **Conversaciones** - Hablar sobre lo que leen juntos
3. **Escritura creativa** - Animar a escribir historias, diarios o cartas
4. **Juegos de palabras** - Crucigramas, sopas de letras, juegos de vocabulario

### Apoyo Emocional:
- Celebren los logros, por pequeños que sean
- Sean pacientes con las áreas de mejora
- Mantengan una actitud positiva hacia la escritura
- Consulten con el docente si tienen dudas

---

## 📞 Próximos Pasos
1. Revisen este reporte con su hijo/a
2. Contacten al docente si tienen preguntas
3. Implementen algunas actividades sugeridas
4. Programen una reunión si desean más detalles

---
*Para más información, no duden en contactar al docente de su hijo/a.*

*Evaluación generada el {{ fecha_readable }}*
*Sistema EDHack IA - Apoyo educativo familiar*
"""
    
    def _get_teacher_template(self):
        """Template de reporte para docentes"""
        return """# 🎓 Reporte Técnico de Evaluación

**ID de Sesión:** {{ session_id }}
**Fecha de Evaluación:** {{ fecha_readable }}

---

## 📈 Resumen Ejecutivo
- **Puntuación Total:** {{ total_score if total_score else 'Pendiente' }}/100
- **Nivel Determinado:** {{ suggested_level }}
- **Estado:** Evaluación completada y validada

---

## 🔍 Análisis Detallado

### Fortalezas Identificadas
{% if fortalezas %}
{% for fortaleza in fortalezas %}
- {{ fortaleza }}
{% endfor %}
{% else %}
- Requiere análisis adicional
{% endif %}

### Áreas de Intervención Pedagógica
{% if areas_mejora %}
{% for area in areas_mejora %}
- {{ area }}
{% endfor %}
{% else %}
- Continuar con el plan pedagógico actual
{% endif %}

### Evaluación Completa
{{ comentario_general }}

---

## 📋 Estadísticas del Texto
- **Palabras analizadas:** {{ word_count }}
- **Caracteres procesados:** {{ character_count }}
- **Modelo de IA:** Gemini Pro
- **Iteraciones de revisión:** Incluye validación docente

---

## 🎯 Recomendaciones Pedagógicas

### Inmediatas (1-2 semanas):
1. Refuerzo específico en áreas identificadas
2. Actividades diferenciadas según nivel
3. Seguimiento personalizado

### A Mediano Plazo (1 mes):
1. Integración de fortalezas en nuevos aprendizajes
2. Evaluación de progreso
3. Ajuste de estrategias si es necesario

### Estratégicas (trimestre):
1. Planificación de objetivos específicos
2. Coordinación con familia
3. Registro de evolución en portafolio

---

## 🔧 Datos Técnicos del Sistema
- **Versión del Sistema:** EDHack IA MVP v1.0
- **Algoritmo:** Gemini Pro con criterios pedagógicos
- **Confiabilidad:** Alta (validada por docente)
- **Fecha de Procesamiento:** {{ fecha_readable }}

---

## 📝 Notas para el Expediente
- Evaluación automática validada por docente
- Feedback iterativo aplicado
- Reportes generados para estudiante y familia
- Recomendaciones pedagógicas establecidas

---

*Este reporte es confidencial y de uso exclusivo educativo*
*Sistema EDHack IA - Herramienta de apoyo docente*
"""
    
    def export_report_to_file(self, report, filename=None):
        """Exportar reporte a archivo"""
        try:
            if not filename:
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                session_id = report.get('metadata', {}).get('session_id', 'unknown')[:8]
                filename = f"reporte_edhack_{session_id}_{timestamp}.json"
            
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(report, f, ensure_ascii=False, indent=2, default=str)
            
            return filename
            
        except Exception as e:
            raise Exception(f"Error exporting report to file: {str(e)}")
    
    def get_report_summary(self, reports):
        """Obtener resumen de todos los reportes generados"""
        if not reports or 'metadata' not in reports:
            return "No hay reportes disponibles"
        
        metadata = reports['metadata']
        session_id = metadata.get('session_id', 'unknown')
        generated_at = metadata.get('generated_at', 'unknown')
        
        audiences = [key for key in reports.keys() if key != 'metadata']
        
        summary = f"""
RESUMEN DE REPORTES GENERADOS
============================
Sesión: {session_id}
Generado: {generated_at}
Audiencias: {', '.join(audiences)}

Reportes disponibles:
"""
        
        for audience in audiences:
            if audience in reports:
                report = reports[audience]
                status = "✅ OK" if not report.get('error') else "❌ Error"
                summary += f"- {audience.title()}: {status}\n"
        
        return summary