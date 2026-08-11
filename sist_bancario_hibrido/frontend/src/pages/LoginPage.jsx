import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { loginUsuario } from '../services/api';
import './LoginPage.css';

export default function LoginPage() {
  const navigate = useNavigate();

  // Estados para capturar los datos del usuario
  const [identificador, setIdentificador] = useState('');
  const [password, setPassword] = useState('');

  // Estados de control de la interfaz
  const [cargando, setCargando] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');

  // Función que maneja el envío del formulario
  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setCargando(true);

    try {
      // 1. Enviar credenciales al backend FastAPI
      const respuesta = await loginUsuario({
        email: identificador,
        password: password,
      });

      // 2. Si la respuesta es exitosa, guardamos el número de cuenta
      if (respuesta && respuesta.cuenta) {
        localStorage.setItem('numero_cuenta', respuesta.cuenta);
      }

      if (respuesta.titular) {
          localStorage.setItem('titular_cuenta', respuesta.titular);
        }
      

      // 3. Redirigimos al Dashboard
      navigate('/cuenta');

    } catch (err) {
      // === AQUÍ SÍ EXISTE LA VARIABLE 'err' ===
      console.error('Error en login:', err);

      let mensaje = 'Error de conexión. Verifica tus credenciales e intenta nuevamente.';
      const detail = err.response?.data?.detail;

      // Transformamos cualquier tipo de error de FastAPI en un TEXTO plano para React
      if (typeof detail === 'string') {
        mensaje = detail; // 401: "Email o contraseña incorrectos."
      } else if (Array.isArray(detail)) {
        mensaje = 'Formato del Email invalido, por favor ingrese un email valido.';}

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

        <h1 className="login-title">Iniciar Sesión</h1>
        <p className="login-subtitle">Accede de forma segura a tu banca híbrida</p>

        {/* Banner de error dinámico */}
        {errorMsg && <div className="error-banner">{errorMsg}</div>}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="identificador">Correo Electrónico</label>
            <input
              id="identificador"
              type="text"
              className="form-input"
              placeholder="ejemplo@banco.com"
              value={identificador}
              onChange={(e) => setIdentificador(e.target.value)}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña</label>
            <input
              id="password"
              type="password"
              className="form-input"
              placeholder="••••••••••••"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={cargando}>
            {cargando ? 'Verificando...' : 'Iniciar Sesión'}
          </button>
        </form>

        {/* Enlaces de navegación rápida */}
        <div className="login-links">
          <Link to="/recuperar-password">¿Olvidaste tu contraseña?</Link>
          <Link to="/registro">¿No tienes cuenta aún? Regístrate</Link>
        </div>
      </div>
    </div>
  );
}
