import { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registrarCuenta } from '../services/api';
import './LoginPage.css';

export default function RegistroPage() {
  const navigate = useNavigate();

  // Estado unificado para todos los campos del formulario
  const [formData, setFormData] = useState({
    numero_cuenta: '',
    titular: '',
    email: '',
    password: ''
  });

  // Estados de control
  const [cargando, setCargando] = useState(false);
  const [errorMsg, setErrorMsg] = useState('');
  const [successMsg, setSuccessMsg] = useState('');

  // Manejador genérico para actualizar el estado cuando el usuario escribe
  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData({
      ...formData,
      [name]: value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setErrorMsg('');
    setSuccessMsg('');
    setCargando(true);

    try {
      // 1. Enviamos los datos y CAPTURAMOS la respuesta del backend
      const respuesta = await registrarCuenta(formData);

      // 2. Auto-Login: Guardamos el número de cuenta generado en el navegador
      if (respuesta && respuesta.numero_cuenta) {
        localStorage.setItem('numero_cuenta', respuesta.numero_cuenta);
        localStorage.setItem('titular_cuenta', respuesta.titular);

      }

      // 3. Mostramos un mensaje de éxito adaptado
      setSuccessMsg('¡Cuenta creada exitosamente! Ingresando a tu banca...');

      // 4. Redirigimos directamente al Dashboard en lugar del Login
      setTimeout(() => {
        navigate('/cuenta');
      }, 2000);

    } catch (err) {
      console.error('Error en registro:', err);
      let mensaje = 'Ocurrió un error al intentar crear la cuenta.';
      const detail = err.response?.data?.detail;

      // Transformamos los errores de FastAPI
      if (typeof detail === 'string') {
        // HTTP 400: "El número de cuenta ya está registrado" o "El correo electrónico..."
        mensaje = detail; 
      } else if (Array.isArray(detail)) {
        // HTTP 422: Errores de validación de Pydantic
        mensaje = 'Por favor, revisa que todos los campos tengan un formato válido.';
      }

      setErrorMsg(mensaje);
    } finally {
      setCargando(false);
    }
  };

  return (
    <div className="login-container">
      <div className="login-card">
        <div className="login-brand">
          🏛️ Banco<span>Híbrido</span>
        </div>

        <h1 className="login-title">Crear Cuenta</h1>
        <p className="login-subtitle">Completa tus datos para unirte</p>

        {/* Banners dinámicos de respuesta */}
        {errorMsg && <div className="error-banner">{errorMsg}</div>}
        {successMsg && (
          <div className="error-banner" style={{ backgroundColor: '#ecfdf5', borderColor: '#a7f3d0', color: '#059669' }}>
            {successMsg}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="numero_cuenta">Número de Cuenta</label>
            <input
              id="numero_cuenta"
              name="numero_cuenta"
              type="text"
              className="form-input"
              placeholder="Ej. 12345678"
              maxLength="8"
              value={formData.numero_cuenta}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="titular">Nombre del Titular</label>
            <input
              id="titular"
              name="titular"
              type="text"
              className="form-input"
              placeholder="Nombre Completo"
              maxLength="100"
              value={formData.titular}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="email">Correo Electrónico</label>
            <input
              id="email"
              name="email"
              type="email"
              className="form-input"
              placeholder="ejemplo@banco.com"
              value={formData.email}
              onChange={handleChange}
              required
            />
          </div>

          <div className="form-group">
            <label htmlFor="password">Contraseña (Mínimo 6 caracteres)</label>
            <input
              id="password"
              name="password"
              type="password"
              className="form-input"
              placeholder="••••••••"
              minLength="6"
              value={formData.password}
              onChange={handleChange}
              required
            />
          </div>

          <button type="submit" className="btn-primary" disabled={cargando || successMsg !== ''}>
            {cargando ? 'Creando cuenta...' : 'Registrarse'}
          </button>
        </form>

        <div className="login-links">
          <Link to="/">¿Ya tienes una cuenta? Inicia sesión aquí</Link>
        </div>
      </div>
    </div>
  );
}