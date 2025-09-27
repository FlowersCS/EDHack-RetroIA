import React, { useState, useEffect } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Alert,
  CircularProgress,
  Card,
  CardContent,
  Chip,
  Grid,
  LinearProgress
} from '@mui/material';
import { AutoAwesome, CheckCircle, Assignment, OpenInNew } from '@mui/icons-material';
import axios from 'axios';

const EvaluationProcess = ({ sessionData, updateSessionData, goToStep }) => {
  const [evaluationStatus, setEvaluationStatus] = useState('idle'); // idle, processing, completed, error
  const [error, setError] = useState('');
  const [progress, setProgress] = useState(0);

  useEffect(() => {
    // Si ya tenemos una evaluación, no la volvemos a hacer
    if (sessionData.evaluationResult) {
      setEvaluationStatus('completed');
      return;
    }

    // Si tenemos un filename pero no evaluación, iniciar automáticamente
    if (sessionData.filename && evaluationStatus === 'idle') {
      startEvaluation();
    }
  }, [sessionData.filename]);

  const startEvaluation = async () => {
    if (!sessionData.sessionId || !sessionData.filename) {
      setError('Faltan datos de la sesión. Por favor, sube el archivo nuevamente.');
      return;
    }

    setEvaluationStatus('processing');
    setError('');
    setProgress(0);
    updateSessionData({ status: 'processing' });

    // Simular progreso de evaluación
    const progressInterval = setInterval(() => {
      setProgress(prev => {
        if (prev >= 90) {
          clearInterval(progressInterval);
          return 90;
        }
        return prev + Math.random() * 15;
      });
    }, 1000);

    try {
      const response = await axios.post('/api/evaluate', {
        session_id: sessionData.sessionId,
        filename: sessionData.filename
      });

      clearInterval(progressInterval);
      setProgress(100);

      if (response.data.success) {
        setEvaluationStatus('completed');
        updateSessionData({
          evaluationResult: response.data.evaluation,
          googleDocId: response.data.google_doc_id,
          googleDocUrl: response.data.google_doc_url,
          status: 'ready'
        });
      } else {
        throw new Error(response.data.error || 'Error en la evaluación');
      }

    } catch (err) {
      clearInterval(progressInterval);
      console.error('Error during evaluation:', err);
      setEvaluationStatus('error');
      setError(err.response?.data?.error || 'Error durante la evaluación. Inténtalo de nuevo.');
      updateSessionData({ status: 'error' });
    }
  };

  const renderEvaluationSummary = () => {
    if (!sessionData.evaluationResult) return null;

    const evaluation = sessionData.evaluationResult;
    const totalScore = evaluation.puntuacion_total || 0;
    
    const getScoreColor = (score) => {
      if (score >= 90) return 'success';
      if (score >= 80) return 'info';
      if (score >= 70) return 'warning';
      return 'error';
    };

    const getScoreEmoji = (score) => {
      if (score >= 90) return '🌟';
      if (score >= 80) return '👍';
      if (score >= 70) return '✅';
      return '📚';
    };

    return (
      <Card elevation={2} sx={{ mb: 3 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <AutoAwesome color="primary" sx={{ mr: 1, verticalAlign: 'middle' }} />
            Resumen de Evaluación IA
          </Typography>
          
          <Grid container spacing={3}>
            <Grid item xs={12} md={4}>
              <Box textAlign="center">
                <Typography variant="h3" color={`${getScoreColor(totalScore)}.main`}>
                  {getScoreEmoji(totalScore)} {totalScore}
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Puntuación Total (de 100)
                </Typography>
                <Chip 
                  label={evaluation.nivel_sugerido || 'No determinado'} 
                  color={getScoreColor(totalScore)}
                  sx={{ mt: 1 }}
                />
              </Box>
            </Grid>
            
            <Grid item xs={12} md={8}>
              <Typography variant="subtitle2" gutterBottom>
                Fortalezas Identificadas:
              </Typography>
              {evaluation.fortalezas && evaluation.fortalezas.length > 0 ? (
                <ul style={{ margin: 0, paddingLeft: '20px' }}>
                  {evaluation.fortalezas.map((fortaleza, index) => (
                    <li key={index}>
                      <Typography variant="body2">{fortaleza}</Typography>
                    </li>
                  ))}
                </ul>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  No se identificaron fortalezas específicas
                </Typography>
              )}
              
              <Typography variant="subtitle2" sx={{ mt: 2 }} gutterBottom>
                Áreas de Mejora:
              </Typography>
              {evaluation.areas_mejora && evaluation.areas_mejora.length > 0 ? (
                <ul style={{ margin: 0, paddingLeft: '20px' }}>
                  {evaluation.areas_mejora.map((area, index) => (
                    <li key={index}>
                      <Typography variant="body2">{area}</Typography>
                    </li>
                  ))}
                </ul>
              ) : (
                <Typography variant="body2" color="textSecondary">
                  No se identificaron áreas específicas de mejora
                </Typography>
              )}
            </Grid>
          </Grid>
        </CardContent>
      </Card>
    );
  };

  const renderProcessingState = () => (
    <Box textAlign="center" py={6}>
      <CircularProgress size={80} sx={{ mb: 3 }} />
      <Typography variant="h5" gutterBottom>
        🤖 Evaluando con Inteligencia Artificial...
      </Typography>
      <Typography variant="body1" color="textSecondary" paragraph>
        Analizando ortografía, gramática, coherencia, cohesión, vocabulario y estructura.
      </Typography>
      
      <Box sx={{ width: '100%', maxWidth: 400, mx: 'auto', mt: 3 }}>
        <LinearProgress variant="determinate" value={progress} />
        <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
          {Math.round(progress)}% completado
        </Typography>
      </Box>
      
      <Typography variant="caption" display="block" sx={{ mt: 3, color: 'text.secondary' }}>
        Este proceso puede tomar entre 30 segundos y 2 minutos...
      </Typography>
    </Box>
  );

  if (evaluationStatus === 'processing') {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          🤖 Evaluación con IA
        </Typography>
        {renderProcessingState()}
      </Box>
    );
  }

  if (evaluationStatus === 'error') {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          🤖 Evaluación con IA
        </Typography>
        
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
        
        <Box textAlign="center">
          <Button 
            variant="contained" 
            onClick={startEvaluation}
            size="large"
          >
            Intentar de Nuevo
          </Button>
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🤖 Evaluación con IA
      </Typography>
      
      <Typography variant="body1" paragraph color="textSecondary">
        La inteligencia artificial ha completado el análisis del texto. A continuación se muestra el resumen de la evaluación.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {evaluationStatus === 'completed' && (
        <>
          <Alert severity="success" sx={{ mb: 3 }}>
            <CheckCircle sx={{ mr: 1 }} />
            ¡Evaluación completada exitosamente! Se ha creado un documento Google Docs editable para revisión docente.
          </Alert>

          {renderEvaluationSummary()}

          {sessionData.googleDocUrl && (
            <Card elevation={1} sx={{ mb: 3, backgroundColor: 'primary.50' }}>
              <CardContent>
                <Typography variant="h6" gutterBottom>
                  <Assignment color="primary" sx={{ mr: 1, verticalAlign: 'middle' }} />
                  Documento de Retroalimentación Creado
                </Typography>
                <Typography variant="body2" paragraph>
                  Se ha generado un documento Google Docs con la evaluación detallada. 
                  El docente puede revisarlo y editarlo según sea necesario.
                </Typography>
                <Button 
                  variant="outlined" 
                  startIcon={<OpenInNew />}
                  onClick={() => window.open(sessionData.googleDocUrl, '_blank')}
                  sx={{ mr: 2 }}
                >
                  Abrir Documento
                </Button>
              </CardContent>
            </Card>
          )}

          <Box textAlign="center" sx={{ mt: 4 }}>
            <Button 
              variant="contained" 
              onClick={() => goToStep(3)}
              size="large"
            >
              Continuar a Revisión Docente
            </Button>
          </Box>
        </>
      )}

      {evaluationStatus === 'idle' && (
        <Box textAlign="center" py={4}>
          <Typography variant="h6" gutterBottom>
            Lista para comenzar la evaluación
          </Typography>
          <Button 
            variant="contained" 
            onClick={startEvaluation}
            size="large"
            disabled={!sessionData.filename}
          >
            Iniciar Evaluación con IA
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default EvaluationProcess;