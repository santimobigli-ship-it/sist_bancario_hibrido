import { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { resetearPassword } from '../services/api';
import './LoginPage.css'; // Reutilizamos el estilo del login

export default function ResetPasswordPage() {
  const navigate = useNavigate();
  const [searchParams] = useSearchParams();
  
  // Extraemos el token de la URL (?token=...)
  const token = searchParams.get('token');

  // Estados del formulario
  const [passwordNueva, setPasswordNueva] = useState('');
  const [passwordConfirmacion, setPasswordConfirmacion] = useState('');
  
  // Estados de control de la UI
  const [cargando, setCargando] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');
  const [tokenValido, setTokenValido] = useState(true);

  // Verificamos si la URL tiene el token al cargar la página
  useEffect(() => {
    if (!token) {
      setTokenValido(false);
      setErrorMsg('Enlace de recuperación inválido o inexistente. Por favor, solicita uno nuevo.');
    }
  }, [token]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');

    // 1. Validaciones previas en el Frontend (Best Practice)
    if (passwordNueva.length < 6) {
      setErrorMsg('La contraseña debe tener al menos 6 caracteres.');
      return;
    }

    if (passwordNueva !== passwordConfirmacion) {
      setErrorMsg('Las contraseñas no coinciden. Verifícalas e intenta nuevamente.');
      return;
    }

    setCargando(true);

    try {
      // 2. Llamada a la API enviando el esquema esperado
      const respuesta = await resetearPassword({
        token: token,
        password_nueva: passwordNueva,
        password_confirmacion: passwordConfirmacion,
      });

      // 3. Mostramos mensaje de éxito
      setSuccessMsg(respuesta.mensaje || 'Contraseña actualizada correctamente.');

      // 4. Redirección diferida para que el usuario lea el mensaje
      setTimeout(() => {
        navigate('/'); // Redirigimos al Login
      }, 3000);

    } catch (err) {
      console.error('Error al resetear contraseña:', err);

      let mensaje = 'No se pudo restablecer la contraseña. Intenta nuevamente.';
      const detail = err.response?.data?.detail;

      // Transformamos los errores del backend para mostrarlos limpios
      if (typeof detail === 'string') {
        mensaje = detail; // Ejemplo: Token expirado o inválido
      } else if (Array.isArray(detail)) {
        mensaje = 'Revisa que los datos ingresados sean correctos.';
      }

      setErrorMsg(mensaje);
    } finally {
      setCargando(false);
    }
  };

  // Renderizado temprano si no hay token en la URL
  if (!tokenValido) {
    return (
      <div className="login-container">
        <div className="login-card">
          <div className="login-brand">
            🏛️ Banco<span>Híbrido</span>
          </div>
          <h1 className="login-title" style={{ color: '#dc2626' }}>Enlace Inválido</h1>
          <div className="error-banner">{errorMsg}</div>
          <div className="login-links" style={{ marginTop: '20px' }}>
            <Link to="/recuperar-password">Volver a solicitar recuperación</Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="login-container">
      <div className="login-card">
        {/* Marca / Logo */}
        <div className="login-brand">
          🏛️ Banco<span>Híbrido</span>
        </div>

        <h1 className="login-title">Nueva Contraseña</h1>
        <p className="login-subtitle">
          Ingresa y confirma tu nueva contraseña de acceso.
        </p>

        {/* Banners de feedback */}
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
            ✅ {successMsg} Redirigiendo al inicio de sesión...
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="passwordNueva">Nueva Contraseña</label>
            <input
              id="passwordNueva"
              type="password"
              className="form-input"
              placeholder="Mínimo 6 caracteres"
              value={passwordNueva}
              onChange={(e) => setPasswordNueva(e.target.value)}
              minLength={6}
              required
              disabled={!!successMsg || cargando} // Bloqueamos si ya tuvo éxito
            />
          </div>

          <div className="form-group">
            <label htmlFor="passwordConfirmacion">Confirmar Contraseña</label>
            <input
              id="passwordConfirmacion"
              type="password"
              className="form-input"
              placeholder="Repite tu nueva contraseña"
              value={passwordConfirmacion}
              onChange={(e) => setPasswordConfirmacion(e.target.value)}
              minLength={6}
              required
              disabled={!!successMsg || cargando}
            />
          </div>

          <button 
            type="submit" 
            className="btn-primary" 
            disabled={cargando || !!successMsg}
          >
            {cargando ? 'Actualizando...' : 'Restablecer Contraseña'}
          </button>
        </form>

        <div className="login-links">
          <Link to="/">Cancelar y volver al Login</Link>
        </div>
      </div>
    </div>
  );
}