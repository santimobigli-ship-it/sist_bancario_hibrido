import axios from 'axios';

// 1. Instancia base de Axios
// Leemos la URL desde la variable de entorno de Vite
const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || 'http://localhost:8000',
  headers: {
    'Content-Type': 'application/json',
  },
});

// ==========================================
// SERVICIOS DE AUTENTICACIÓN Y CUENTAS
// ==========================================

export const loginUsuario = async (credenciales) => {
  const response = await api.post('/cuentas/login', credenciales);
  return response.data;
};

export const registrarCuenta = async (datosCuenta) => {
  const response = await api.post('/cuentas', datosCuenta);
  return response.data;
};

export const solicitarRecuperacionPassword = async (email) => {
  const response = await api.post('/cuentas/recuperar-password', { email });
  return response.data;
};

export const resetearPassword = async (datosReset) => {
  const response = await api.put('/cuentas/reset-password', datosReset);
  return response.data;
};

// ==========================================
// SERVICIOS DE OPERACIONES Y SALDOS
// ==========================================

export const obtenerDatosCuenta = async (numeroCuenta) => {
  const response = await api.get(`/transacciones/${numeroCuenta}`);
  return response.data;
};

export const realizarTransaccion = async (datosTransaccion) => {
  const response = await api.post('/transacciones', datosTransaccion);
  return response.data;
};

export default api;