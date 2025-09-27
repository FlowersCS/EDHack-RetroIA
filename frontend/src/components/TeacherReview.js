import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Alert,
  Card,
  CardContent,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  RadioGroup,
  FormControlLabel,
  Radio,
  TextField
} from '@mui/material';
import { 
  School, 
  CheckCircle, 
  Edit, 
  OpenInNew, 
  ThumbUp, 
  ThumbDown,
  Refresh 
} from '@mui/icons-material';
import axios from 'axios';

const TeacherReview = ({ sessionData, updateSessionData, goToStep }) => {
  const [reviewStatus, setReviewStatus] = useState('pending'); // pending, submitting, completed, error
  const [error, setError] = useState('');
  const [showReviewDialog, setShowReviewDialog] = useState(false);
  const [reviewDecision, setReviewDecision] = useState(''); // approve, revise
  const [reviewComments, setReviewComments] = useState('');

  const handleOpenReviewDialog = () => {
    setShowReviewDialog(true);
  };

  const handleCloseReviewDialog = () => {
    setShowReviewDialog(false);
    setReviewDecision('');
    setReviewComments('');
  };

  const handleSubmitReview = async () => {
    if (!reviewDecision) {
      setError('Por favor, selecciona una opción de revisión.');
      return;
    }

    setReviewStatus('submitting');
    setError('');
    updateSessionData({ status: 'processing' });

    try {
      const response = await axios.post('/api/approve-feedback', {
        doc_id: sessionData.googleDocId,
        session_id: sessionData.sessionId,
        approved: reviewDecision === 'approve',
        comments: reviewComments
      });

      if (response.data.success) {
        if (reviewDecision === 'approve') {
          // Retroalimentación aprobada - generar reportes finales
          updateSessionData({
            finalReports: response.data.final_report,
            status: 'completed'
          });
          setReviewStatus('completed');
          handleCloseReviewDialog();
          
          // Avanzar al paso final
          setTimeout(() => {
            goToStep(4);
          }, 2000);
          
        } else {
          // Retroalimentación necesita correcciones - actualizar evaluación
          updateSessionData({
            evaluationResult: response.data.updated_evaluation,
            status: 'ready'
          });
          setReviewStatus('pending');
          handleCloseReviewDialog();
          
          // Mostrar mensaje de que se ha actualizado
          setError('');
          alert('El documento ha sido actualizado con las correcciones. Por favor, revísalo nuevamente.');
        }
      } else {
        throw new Error(response.data.error || 'Error en la revisión');
      }

    } catch (err) {
      console.error('Error during review:', err);
      setReviewStatus('error');
      setError(err.response?.data?.error || 'Error durante la revisión. Inténtalo de nuevo.');
      updateSessionData({ status: 'error' });
    }
  };

  const renderInstructions = () => (
    <Card elevation={1} sx={{ mb: 3, backgroundColor: 'info.50' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          <School color="primary" sx={{ mr: 1, verticalAlign: 'middle' }} />
          Instrucciones para el Docente
        </Typography>
        <Typography variant="body2" paragraph>
          1. <strong>Revisa el documento:</strong> Abre el documento Google Docs generado automáticamente
        </Typography>
        <Typography variant="body2" paragraph>
          2. <strong>Edita si es necesario:</strong> Corrige comentarios, ajusta puntuaciones, o añade observaciones
        </Typography>
        <Typography variant="body2" paragraph>
          3. <strong>Toma una decisión:</strong> Aprueba la retroalimentación o solicita una nueva iteración con IA
        </Typography>
        <Typography variant="body2">
          4. <strong>Genera reportes:</strong> Una vez aprobada, se crearán reportes personalizados para estudiante, familia y docente
        </Typography>
      </CardContent>
    </Card>
  );

  const renderDocumentAccess = () => (
    <Card elevation={2} sx={{ mb: 3 }}>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          📄 Documento de Retroalimentación
        </Typography>
        <Typography variant="body2" paragraph color="textSecondary">
          El documento Google Docs contiene la evaluación detallada generada por IA. 
          Puedes editarlo directamente para hacer correcciones o añadir comentarios adicionales.
        </Typography>
        
        {sessionData.googleDocUrl ? (
          <Button 
            variant="contained" 
            startIcon={<OpenInNew />}
            onClick={() => window.open(sessionData.googleDocUrl, '_blank')}
            size="large"
            sx={{ mr: 2 }}
          >
            Abrir Documento Google Docs
          </Button>
        ) : (
          <Alert severity="warning">
            No se pudo generar el enlace al documento. Revisa la configuración de Google Docs.
          </Alert>
        )}
        
        <Button 
          variant="outlined" 
          startIcon={<Edit />}
          onClick={handleOpenReviewDialog}
          size="large"
        >
          Revisar y Decidir
        </Button>
      </CardContent>
    </Card>
  );

  const renderReviewDialog = () => (
    <Dialog open={showReviewDialog} onClose={handleCloseReviewDialog} maxWidth="md" fullWidth>
      <DialogTitle>
        🎓 Revisión Docente de la Retroalimentación
      </DialogTitle>
      <DialogContent>
        <Typography variant="body1" paragraph>
          Después de revisar el documento Google Docs, ¿qué deseas hacer con la retroalimentación?
        </Typography>
        
        <RadioGroup 
          value={reviewDecision} 
          onChange={(e) => setReviewDecision(e.target.value)}
        >
          <FormControlLabel 
            value="approve" 
            control={<Radio />} 
            label={
              <Box>
                <Typography variant="subtitle2">
                  <ThumbUp sx={{ mr: 1, verticalAlign: 'middle', color: 'success.main' }} />
                  Aprobar retroalimentación
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  La retroalimentación está lista. Generar reportes finales para estudiante, familia y docente.
                </Typography>
              </Box>
            }
          />
          <FormControlLabel 
            value="revise" 
            control={<Radio />} 
            label={
              <Box>
                <Typography variant="subtitle2">
                  <Refresh sx={{ mr: 1, verticalAlign: 'middle', color: 'warning.main' }} />
                  Solicitar nueva iteración con IA
                </Typography>
                <Typography variant="body2" color="textSecondary">
                  Hay correcciones en el documento. La IA debe generar una nueva versión considerando los cambios.
                </Typography>
              </Box>
            }
          />
        </RadioGroup>
        
        <TextField
          label="Comentarios adicionales (opcional)"
          multiline
          rows={3}
          fullWidth
          value={reviewComments}
          onChange={(e) => setReviewComments(e.target.value)}
          sx={{ mt: 3 }}
          placeholder="Añade comentarios sobre las correcciones realizadas o instrucciones específicas..."
        />
      </DialogContent>
      <DialogActions>
        <Button onClick={handleCloseReviewDialog}>
          Cancelar
        </Button>
        <Button 
          onClick={handleSubmitReview} 
          variant="contained"
          disabled={!reviewDecision || reviewStatus === 'submitting'}
        >
          {reviewStatus === 'submitting' ? 'Procesando...' : 'Confirmar Decisión'}
        </Button>
      </DialogActions>
    </Dialog>
  );

  if (reviewStatus === 'completed') {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          🎓 Revisión Docente
        </Typography>
        
        <Alert severity="success" sx={{ mb: 3 }}>
          <CheckCircle sx={{ mr: 1 }} />
          ¡Retroalimentación aprobada exitosamente! Los reportes finales están siendo generados.
        </Alert>
        
        <Box textAlign="center" py={4}>
          <Typography variant="h6" gutterBottom>
            Redirigiendo a reportes finales...
          </Typography>
          <Button 
            variant="contained" 
            onClick={() => goToStep(4)}
            size="large"
          >
            Ver Reportes Finales
          </Button>
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        🎓 Revisión Docente
      </Typography>
      
      <Typography variant="body1" paragraph color="textSecondary">
        Es momento de que el docente revise la retroalimentación generada por IA y tome una decisión sobre su aprobación.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      {!sessionData.googleDocUrl && (
        <Alert severity="warning" sx={{ mb: 3 }}>
          No se encontró el documento de retroalimentación. Por favor, regresa al paso anterior para generar la evaluación.
        </Alert>
      )}

      {renderInstructions()}
      {renderDocumentAccess()}
      {renderReviewDialog()}

      {reviewStatus === 'submitting' && (
        <Alert severity="info" sx={{ mt: 3 }}>
          Procesando tu decisión... Por favor espera.
        </Alert>
      )}
    </Box>
  );
};

export default TeacherReview;