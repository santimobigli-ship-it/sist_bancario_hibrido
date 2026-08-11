import { useState } from 'react';
import { Link } from 'react-router-dom';
import { solicitarRecuperacionPassword } from '../services/api';
import './LoginPage.css'; // Reutilizamos los mismos estilos bancarios

export default function RecuperarPasswordPage() {
  const [email, setEmail] = useState('');
  const [cargando, setCargando] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setCargando(true);

    try {
      // 1. Llamamos a la API enviando el email
      const respuesta = await solicitarRecuperacionPassword(email);

      // 2. Mostramos el mensaje devuelto por el backend
      setSuccessMsg(
        respuesta.mensaje ||
          'Si el correo está registrado, recibirás un enlace de recuperación en breve.'
      );
      
      // Limpiamos el campo de email tras el envío exitoso
      setEmail('');
    } catch (err) {
      console.error('Error al solicitar recuperación:', err);

      let mensaje = 'Ocurrió un error al procesar la solicitud. Intenta nuevamente.';
      const detail = err.response?.data?.detail;

      if (typeof detail === 'string') {
        mensaje = detail;
      } else if (Array.isArray(detail)) {
        mensaje = 'Por favor, ingresa un correo electrónico válido.';
      }

      setErrorMsg(mensaje);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        {/* Marca / Logo */}
        <div className="login-brand">
          🏛️ Banco<span>Híbrido</span>
        </div>

        <h1 className="login-title">Recuperar Contraseña</h1>
        <p className="login-subtitle">
          Ingresa tu correo para recibir un enlace seguro de recuperación
        </p>

        {/* Banners dinámicos */}
        {errorMsg && <div className="error-banner">{errorMsg}</div>}
        {successMsg && (
          <div
            className="error-banner"
            style={{
              backgroundColor: '#ecfdf5',
              borderColor: '#a7f3d0',
              color: '#059669',
            }}
          >
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="email">Correo Electrónico</label>
            <input
              id="email"
              type="email"
              className="form-input"
              placeholder="ejemplo@banco.com"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={cargando}>
            {cargando ? 'Enviando...' : 'Enviar Enlace de Recuperación'}
          </button>
        </form>

        {/* Enlace de retorno */}
        <div className="login-links">
          <Link to="/">¿Recordaste tu contraseña? Inicia sesión aquí</Link>
        </div>
      </div>
    </div>
  );
}