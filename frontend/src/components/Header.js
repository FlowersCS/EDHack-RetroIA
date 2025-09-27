import React from 'react';
import { Typography, Box, Chip } from '@mui/material';
import { School, AutoAwesome, CheckCircle, Error } from '@mui/icons-material';

const Header = ({ status }) => {
  const getStatusInfo = (status) => {
    switch (status) {
      case 'ready':
        return { label: 'Listo', color: 'default', icon: <School /> };
      case 'processing':
        return { label: 'Procesando', color: 'warning', icon: <AutoAwesome /> };
      case 'completed':
        return { label: 'Completado', color: 'success', icon: <CheckCircle /> };
      case 'error':
        return { label: 'Error', color: 'error', icon: <Error /> };
      default:
        return { label: 'Listo', color: 'default', icon: <School /> };
    }
  };

  const statusInfo = getStatusInfo(status);

  return (
    <Box className="header">
      <Typography variant="h2" component="h1" gutterBottom>
        📝 EDHack IA
      </Typography>
      <Typography variant="h6" color="textSecondary">
        Sistema de Evaluación Automática de Escritura
        <Chip 
          icon={statusInfo.icon}
          label={statusInfo.label}
          color={statusInfo.color}
          variant="outlined"
          style={{ marginLeft: '15px' }}
        />
      </Typography>
    </Box>
  );
};

export default Header;