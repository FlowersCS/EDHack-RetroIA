import React, { useState } from 'react';
import { 
  Box, 
  Typography, 
  Button, 
  Alert,
  Card,
  CardContent,
  Tabs,
  Tab,
  Paper,
  Chip,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions
} from '@mui/material';
import { 
  CheckCircle, 
  Person, 
  People, 
  School,
  Download,
  Visibility,
  Share,
  RestartAlt
} from '@mui/icons-material';

const FinalReports = ({ sessionData, updateSessionData, goToStep }) => {
  const [activeTab, setActiveTab] = useState(0);
  const [previewDialog, setPreviewDialog] = useState({ open: false, content: '', title: '' });

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  const handlePreviewReport = (reportType) => {
    if (!sessionData.finalReports || !sessionData.finalReports[reportType]) {
      alert('Reporte no disponible');
      return;
    }

    const report = sessionData.finalReports[reportType];
    const titles = {
      'estudiante': '📝 Reporte para el Estudiante',
      'familia': '👨‍👩‍👧‍👦 Reporte para la Familia', 
      'docente': '🎓 Reporte Técnico para el Docente'
    };

    setPreviewDialog({
      open: true,
      content: report.content || 'Contenido no disponible',
      title: titles[reportType] || 'Reporte'
    });
  };

  const handleDownloadReport = (reportType) => {
    if (!sessionData.finalReports || !sessionData.finalReports[reportType]) {
      alert('Reporte no disponible para descarga');
      return;
    }

    const report = sessionData.finalReports[reportType];
    const content = report.content || 'Contenido no disponible';
    
    const element = document.createElement('a');
    const file = new Blob([content], { type: 'text/markdown' });
    element.href = URL.createObjectURL(file);
    element.download = `reporte_${reportType}_${sessionData.sessionId?.substring(0, 8) || 'edhack'}.md`;
    document.body.appendChild(element);
    element.click();
    document.body.removeChild(element);
  };

  const handleStartNew = () => {
    // Resetear toda la sesión
    updateSessionData({
      sessionId: null,
      filename: null,
      evaluationResult: null,
      googleDocId: null,
      googleDocUrl: null,
      finalReports: null,
      status: 'ready'
    });
    goToStep(1);
  };

  const renderReportCard = (reportType, icon, title, description, audience) => {
    const report = sessionData.finalReports?.[reportType];
    const isAvailable = report && !report.error;

    return (
      <Card elevation={2} sx={{ mb: 2 }}>
        <CardContent>
          <Box display="flex" alignItems="center" mb={2}>
            {icon}
            <Typography variant="h6" sx={{ ml: 1, flexGrow: 1 }}>
              {title}
            </Typography>
            {isAvailable ? (
              <Chip label="Disponible" color="success" size="small" />
            ) : (
              <Chip label="Error" color="error" size="small" />
            )}
          </Box>
          
          <Typography variant="body2" color="textSecondary" paragraph>
            {description}
          </Typography>
          
          {report?.error && (
            <Alert severity="error" sx={{ mb: 2 }}>
              Error: {report.error}
            </Alert>
          )}
          
          <Box display="flex" gap={1} flexWrap="wrap">
            <Button 
              variant="outlined" 
              startIcon={<Visibility />}
              onClick={() => handlePreviewReport(reportType)}
              disabled={!isAvailable}
              size="small"
            >
              Vista Previa
            </Button>
            <Button 
              variant="outlined" 
              startIcon={<Download />}
              onClick={() => handleDownloadReport(reportType)}
              disabled={!isAvailable}
              size="small"
            >
              Descargar
            </Button>
            <Button 
              variant="outlined" 
              startIcon={<Share />}
              disabled={!isAvailable}
              size="small"
            >
              Compartir
            </Button>
          </Box>
        </CardContent>
      </Card>
    );
  };

  const renderSummary = () => {
    const metadata = sessionData.finalReports?.metadata;
    const evaluation = sessionData.evaluationResult;

    return (
      <Card elevation={1} sx={{ mb: 3, backgroundColor: 'success.50' }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            <CheckCircle color="success" sx={{ mr: 1, verticalAlign: 'middle' }} />
            ¡Proceso Completado Exitosamente!
          </Typography>
          
          <Typography variant="body2" paragraph>
            La evaluación automática de escritura ha sido completada y validada por el docente. 
            Se han generado reportes personalizados para cada audiencia.
          </Typography>
          
          {metadata && (
            <Box sx={{ mt: 2 }}>
              <Typography variant="caption" display="block">
                <strong>Sesión:</strong> {metadata.session_id?.substring(0, 8) || 'N/A'}
              </Typography>
              <Typography variant="caption" display="block">
                <strong>Generado:</strong> {new Date(metadata.generated_at).toLocaleString('es-ES')}
              </Typography>
              <Typography variant="caption" display="block">
                <strong>Sistema:</strong> {metadata.system || 'EDHack IA MVP'}
              </Typography>
            </Box>
          )}
          
          {evaluation?.puntuacion_total && (
            <Box sx={{ mt: 2 }}>
              <Chip 
                label={`Puntuación Final: ${evaluation.puntuacion_total}/100`} 
                color="primary" 
                sx={{ mr: 1 }}
              />
              <Chip 
                label={`Nivel: ${evaluation.nivel_sugerido || 'No determinado'}`} 
                color="secondary" 
              />
            </Box>
          )}
        </CardContent>
      </Card>
    );
  };

  const renderPreviewDialog = () => (
    <Dialog 
      open={previewDialog.open} 
      onClose={() => setPreviewDialog({ open: false, content: '', title: '' })}
      maxWidth="md" 
      fullWidth
    >
      <DialogTitle>{previewDialog.title}</DialogTitle>
      <DialogContent>
        <Paper 
          elevation={0} 
          sx={{ 
            p: 2, 
            backgroundColor: 'grey.50',
            whiteSpace: 'pre-wrap',
            fontFamily: 'monospace',
            fontSize: '0.9rem',
            maxHeight: '60vh',
            overflow: 'auto'
          }}
        >
          {previewDialog.content}
        </Paper>
      </DialogContent>
      <DialogActions>
        <Button onClick={() => setPreviewDialog({ open: false, content: '', title: '' })}>
          Cerrar
        </Button>
      </DialogActions>
    </Dialog>
  );

  if (!sessionData.finalReports) {
    return (
      <Box>
        <Typography variant="h4" gutterBottom>
          📊 Reportes Finales
        </Typography>
        
        <Alert severity="warning" sx={{ mb: 3 }}>
          Los reportes finales no están disponibles. Por favor, completa el proceso de revisión docente primero.
        </Alert>
        
        <Box textAlign="center">
          <Button 
            variant="contained" 
            onClick={() => goToStep(3)}
            size="large"
          >
            Ir a Revisión Docente
          </Button>
        </Box>
      </Box>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        📊 Reportes Finales
      </Typography>
      
      <Typography variant="body1" paragraph color="textSecondary">
        El proceso de evaluación ha sido completado. Aquí están los reportes personalizados para cada audiencia.
      </Typography>

      {renderSummary()}

      <Typography variant="h5" gutterBottom sx={{ mt: 4 }}>
        Reportes Generados
      </Typography>

      {renderReportCard(
        'estudiante',
        <Person color="primary" />,
        'Reporte para el Estudiante',
        'Reporte motivacional dirigido al estudiante con lenguaje accesible y enfoque en el crecimiento.',
        'Estudiante'
      )}

      {renderReportCard(
        'familia', 
        <People color="secondary" />,
        'Reporte para la Familia',
        'Reporte informativo para padres y familiares con sugerencias de apoyo en casa.',
        'Familia'
      )}

      {renderReportCard(
        'docente',
        <School color="success" />,
        'Reporte Técnico para el Docente', 
        'Reporte técnico con datos detallados, estadísticas y recomendaciones pedagógicas.',
        'Docente'
      )}

      {renderPreviewDialog()}

      <Box textAlign="center" sx={{ mt: 4, pt: 3, borderTop: '1px solid', borderColor: 'divider' }}>
        <Typography variant="h6" gutterBottom>
          ¿Deseas evaluar otro texto?
        </Typography>
        <Button 
          variant="contained" 
          startIcon={<RestartAlt />}
          onClick={handleStartNew}
          size="large"
          color="secondary"
        >
          Iniciar Nueva Evaluación
        </Button>
      </Box>
    </Box>
  );
};

export default FinalReports;