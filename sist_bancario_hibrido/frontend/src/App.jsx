import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import LoginPage from './pages/LoginPage';
import RecuperarPasswordPage from './pages/RecuperarPasswordPage';
import ResetPasswordPage from './pages/ResetPasswordPage';
import CuentaPage from './pages/CuentaPage';
import RegistroPage from './pages/RegistroPage'

function App() {
  return (
    <BrowserRouter>
      <Routes>

        {/* Ruta principal: Login */}
        <Route path="/" element={<LoginPage />} />

        <Route path="/registro" element={<RegistroPage />} />

        {/* Ruta para pedir el correo de recuperación */}
        <Route path="/recuperar-password" element={<RecuperarPasswordPage />} />

        {/* Ruta donde aterriza el usuario desde el link del correo */}
        <Route path="/reset-password" element={<ResetPasswordPage />} />

        {/* Dashboard principal */}
        <Route path="/cuenta" element={<CuentaPage />} />

        {/* Redirección por si escriben cualquier otra ruta que no exista */}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;