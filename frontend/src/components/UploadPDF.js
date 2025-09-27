import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { 
  Box, 
  Typography, 
  Button, 
  Paper, 
  Alert,
  CircularProgress,
  LinearProgress
} from '@mui/material';
import { CloudUpload, PictureAsPdf, CheckCircle } from '@mui/icons-material';
import axios from 'axios';

const UploadPDF = ({ sessionData, updateSessionData, goToStep }) => {
  const [uploadStatus, setUploadStatus] = useState('idle'); // idle, uploading, success, error
  const [error, setError] = useState('');
  const [uploadProgress, setUploadProgress] = useState(0);

  const onDrop = useCallback(async (acceptedFiles) => {
    const file = acceptedFiles[0];
    
    if (!file) return;

    // Validaciones básicas
    if (file.type !== 'application/pdf') {
      setError('Por favor, selecciona un archivo PDF válido.');
      return;
    }

    if (file.size > 16 * 1024 * 1024) { // 16MB
      setError('El archivo es demasiado grande. Máximo 16MB permitido.');
      return;
    }

    setError('');
    setUploadStatus('uploading');
    setUploadProgress(0);
    updateSessionData({ status: 'processing' });

    try {
      const formData = new FormData();
      formData.append('file', file);

      const response = await axios.post('/api/upload-pdf', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
        onUploadProgress: (progressEvent) => {
          const percentCompleted = Math.round(
            (progressEvent.loaded * 100) / progressEvent.total
          );
          setUploadProgress(percentCompleted);
        },
      });

      if (response.data.success) {
        setUploadStatus('success');
        updateSessionData({
          sessionId: response.data.session_id,
          filename: response.data.filename,
          textPreview: response.data.text_preview,
          status: 'ready'
        });
        
        // Avanzar automáticamente al siguiente paso después de 2 segundos
        setTimeout(() => {
          goToStep(2);
        }, 2000);
        
      } else {
        throw new Error(response.data.error || 'Error desconocido');
      }

    } catch (err) {
      console.error('Error uploading file:', err);
      setUploadStatus('error');
      setError(err.response?.data?.error || 'Error al subir el archivo. Inténtalo de nuevo.');
      updateSessionData({ status: 'error' });
    }
  }, [updateSessionData, goToStep]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf']
    },
    multiple: false,
    disabled: uploadStatus === 'uploading'
  });

  const renderUploadArea = () => {
    if (uploadStatus === 'success') {
      return (
        <Box textAlign="center" p={4}>
          <CheckCircle color="success" sx={{ fontSize: 60, mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            ¡Archivo subido exitosamente!
          </Typography>
          <Typography variant="body2" color="textSecondary">
            Redirigiendo a la evaluación...
          </Typography>
        </Box>
      );
    }

    if (uploadStatus === 'uploading') {
      return (
        <Box textAlign="center" p={4}>
          <CircularProgress size={60} sx={{ mb: 2 }} />
          <Typography variant="h6" gutterBottom>
            Subiendo archivo...
          </Typography>
          <Box sx={{ width: '100%', mt: 2 }}>
            <LinearProgress variant="determinate" value={uploadProgress} />
            <Typography variant="body2" color="textSecondary" sx={{ mt: 1 }}>
              {uploadProgress}% completado
            </Typography>
          </Box>
        </Box>
      );
    }

    return (
      <Box
        {...getRootProps()}
        sx={{
          border: '2px dashed',
          borderColor: isDragActive ? 'primary.main' : 'grey.400',
          borderRadius: 2,
          p: 4,
          textAlign: 'center',
          cursor: 'pointer',
          backgroundColor: isDragActive ? 'action.hover' : 'background.paper',
          transition: 'all 0.3s ease',
          '&:hover': {
            borderColor: 'primary.main',
            backgroundColor: 'action.hover'
          }
        }}
      >
        <input {...getInputProps()} />
        <CloudUpload sx={{ fontSize: 60, color: 'primary.main', mb: 2 }} />
        
        {isDragActive ? (
          <Typography variant="h6">
            Suelta el archivo aquí...
          </Typography>
        ) : (
          <>
            <Typography variant="h6" gutterBottom>
              Arrastra tu archivo PDF aquí
            </Typography>
            <Typography variant="body2" color="textSecondary" gutterBottom>
              o haz clic para seleccionar
            </Typography>
            <Button variant="outlined" sx={{ mt: 2 }}>
              Seleccionar PDF
            </Button>
          </>
        )}
        
        <Typography variant="caption" display="block" sx={{ mt: 2, color: 'text.secondary' }}>
          Formatos soportados: PDF | Tamaño máximo: 16MB
        </Typography>
      </Box>
    );
  };

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        📄 Subir Texto del Estudiante
      </Typography>
      
      <Typography variant="body1" paragraph color="textSecondary">
        Sube el archivo PDF con el texto escrito por el estudiante para comenzar la evaluación automática.
      </Typography>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }}>
          {error}
        </Alert>
      )}

      <Paper elevation={2} sx={{ mb: 3 }}>
        {renderUploadArea()}
      </Paper>

      {sessionData.textPreview && (
        <Paper elevation={1} sx={{ p: 3, backgroundColor: 'grey.50' }}>
          <Typography variant="h6" gutterBottom>
            <PictureAsPdf color="error" sx={{ mr: 1, verticalAlign: 'middle' }} />
            Vista previa del texto extraído:
          </Typography>
          <Typography 
            variant="body2" 
            sx={{ 
              fontFamily: 'monospace',
              backgroundColor: 'white',
              p: 2,
              borderRadius: 1,
              border: '1px solid',
              borderColor: 'grey.300',
              maxHeight: 200,
              overflow: 'auto'
            }}
          >
            {sessionData.textPreview}
          </Typography>
        </Paper>
      )}

      {uploadStatus === 'success' && (
        <Box textAlign="center" sx={{ mt: 3 }}>
          <Button 
            variant="contained" 
            onClick={() => goToStep(2)}
            size="large"
          >
            Continuar con la Evaluación
          </Button>
        </Box>
      )}
    </Box>
  );
};

export default UploadPDF;