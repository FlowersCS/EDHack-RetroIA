import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import Header from './components/Header';
import UploadPDF from './components/UploadPDF';
import EvaluationProcess from './components/EvaluationProcess';
import TeacherReview from './components/TeacherReview';
import FinalReports from './components/FinalReports';
import StepIndicator from './components/StepIndicator';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function App() {
  const [currentStep, setCurrentStep] = useState(1);
  const [sessionData, setSessionData] = useState({
    sessionId: null,
    filename: null,
    evaluationResult: null,
    googleDocId: null,
    googleDocUrl: null,
    finalReports: null,
    status: 'ready' // ready, processing, completed, error
  });

  const steps = [
    { number: 1, title: 'Subir PDF', component: 'upload' },
    { number: 2, title: 'Evaluación IA', component: 'evaluation' },
    { number: 3, title: 'Revisión Docente', component: 'review' },
    { number: 4, title: 'Reportes Finales', component: 'reports' }
  ];

  const updateSessionData = (newData) => {
    setSessionData(prevData => ({ ...prevData, ...newData }));
  };

  const goToStep = (stepNumber) => {
    setCurrentStep(stepNumber);
  };

  const renderCurrentComponent = () => {
    switch (currentStep) {
      case 1:
        return (
          <UploadPDF 
            sessionData={sessionData}
            updateSessionData={updateSessionData}
            goToStep={goToStep}
          />
        );
      case 2:
        return (
          <EvaluationProcess 
            sessionData={sessionData}
            updateSessionData={updateSessionData}
            goToStep={goToStep}
          />
        );
      case 3:
        return (
          <TeacherReview 
            sessionData={sessionData}
            updateSessionData={updateSessionData}
            goToStep={goToStep}
          />
        );
      case 4:
        return (
          <FinalReports 
            sessionData={sessionData}
            updateSessionData={updateSessionData}
            goToStep={goToStep}
          />
        );
      default:
        return <UploadPDF sessionData={sessionData} updateSessionData={updateSessionData} goToStep={goToStep} />;
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <div className="app-container">
        <Header status={sessionData.status} />
        
        <div className="main-content">
          <StepIndicator 
            steps={steps} 
            currentStep={currentStep} 
            sessionData={sessionData}
          />
          
          <div className="card">
            {renderCurrentComponent()}
          </div>
        </div>
      </div>
    </ThemeProvider>
  );
}

export default App;