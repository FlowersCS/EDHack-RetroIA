// Tests del frontend (Jest/React Testing Library)
// Para implementar cuando se necesiten tests frontend

import { render, screen } from '@testing-library/react';
import App from '../src/App';

// Placeholder para tests del frontend
describe('App Component', () => {
  test('renders EDHack IA title', () => {
    render(<App />);
    const titleElement = screen.getByText(/EDHack IA/i);
    expect(titleElement).toBeInTheDocument();
  });
});