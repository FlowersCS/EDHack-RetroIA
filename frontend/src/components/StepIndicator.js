import React from 'react';
import { Box, Typography } from '@mui/material';
import { CheckCircle, RadioButtonUnchecked, PlayArrow } from '@mui/icons-material';

const StepIndicator = ({ steps, currentStep, sessionData }) => {
  const getStepStatus = (stepNumber) => {
    if (stepNumber < currentStep) return 'completed';
    if (stepNumber === currentStep) return 'active';
    return 'pending';
  };

  const getStepIcon = (stepNumber, status) => {
    if (status === 'completed') return <CheckCircle />;
    if (status === 'active') return <PlayArrow />;
    return <RadioButtonUnchecked />;
  };

  return (
    <Box className="step-indicator">
      {steps.map((step) => {
        const status = getStepStatus(step.number);
        
        return (
          <Box key={step.number} className={`step ${status}`}>
            <Box className="step-circle">
              {getStepIcon(step.number, status)}
            </Box>
            <Typography className="step-title" variant="caption">
              {step.title}
            </Typography>
          </Box>
        );
      })}
    </Box>
  );
};

export default StepIndicator;