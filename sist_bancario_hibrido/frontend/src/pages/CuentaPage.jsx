import { useState, useEffect, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { obtenerDatosCuenta, realizarTransaccion } from '../services/api';
import './CuentaPage.css';

export default function CuentaPage() {
  const navigate = useNavigate();
  const numeroCuenta = localStorage.getItem('numero_cuenta');
  const titularCuenta = localStorage.getItem('titular_cuenta') || 'Usuario';

  // Estados de datos
  const [transacciones, setTransacciones] = useState([]);
  const [saldoTotal, setSaldoTotal] = useState(0);

  // Estados del formulario de operación
  const [tipoOperacion, setTipoOperacion] = useState('D'); // 'D' (Depósito) o 'R' (Retiro)
  const [monto, setMonto] = useState('');

  // Estados de control de UI
  const [cargandoHistorial, setCargandoHistorial] = useState(true);
  const [cargandoEnvio, setCargandoEnvio] = useState(false);
  const [errorOperacion, setErrorOperacion] = useState('');

  // 1. Cargar historial de transacciones desde FastAPI
  const cargarHistorial = useCallback(async () => {
    if (!numeroCuenta) {
      navigate('/');
      return;
    }

    try {
      setCargandoHistorial(true);
      const data = await obtenerDatosCuenta(numeroCuenta);
      setTransacciones(data);

      // Calculamos el saldo acumulado basándonos en el historial de transacciones
      const saldoCalculado = data.reduce((acc, tx) => {
        const montoNum = parseFloat(tx.monto);
        return tx.tipo_operacion === 'D' ? acc + montoNum : acc - montoNum;
      }, 0);

      setSaldoTotal(saldoCalculado);
    } catch (err) {
      console.error('Error al cargar datos de la cuenta:', err);
    } finally {
      setCargandoHistorial(false);
    }
  }, [numeroCuenta, navigate]);

  useEffect(() => {
    cargarHistorial();
  }, [cargarHistorial]);

  // 2. Manejar la ejecución de una nueva transacción (Depósito / Retiro)
  const handleSubmitTransaccion = async (e) => {
    e.preventDefault();
    setErrorOperacion('');

    const montoNumerico = parseFloat(monto);
    if (isNaN(montoNumerico) || montoNumerico <= 0) {
      setErrorOperacion('Ingresa un monto válido mayor a 0.');
      return;
    }

    // Validación previa en frontend para retiros
    if (tipoOperacion === 'R' && montoNumerico > saldoTotal) {
      setErrorOperacion('Saldo insuficiente');
      return;
    }

    setCargandoEnvio(true);

    try {
      await realizarTransaccion({
        numero_cuenta: numeroCuenta,
        tipo_operacion: tipoOperacion,
        monto: montoNumerico,
      });

      setMonto('');
      // Recargamos el historial para traer la nueva transacción registrada
      await cargarHistorial();
    } catch (err) {
      console.error('Error al realizar transacción:', err);
      const detail = err.response?.data?.detail;

      if (typeof detail === 'string') {
        setErrorOperacion(detail);
      } else {
        setErrorOperacion('No se pudo procesar la operación.');
      }
    } finally {
      setCargandoEnvio(false);
    }
  };

  // 3. Función para cerrar sesión
  const handleLogout = () => {
    localStorage.removeItem('numero_cuenta');
    localStorage.removeItem('titular_cuenta'); 
    navigate('/');
  };

  // Utility Formatters (Internacionalización)
  const formatMoneda = (valor) => {
    return new Intl.NumberFormat('es-AR', {
      style: 'currency',
      currency: 'ARS',
      minimumFractionDigits: 2,
    }).format(valor);
  };

  const formatFecha = (fechaStr) => {
    const fecha = new Date(fechaStr);
    return new Intl.DateTimeFormat('es-ES', {
      day: '2-digit',
      month: 'short',
      year: 'numeric',
    }).format(fecha);
  };

  return (
    <div className="dashboard-container">
      {/* Header Superior */}
      <header className="dashboard-header">
        <div className="brand-logo">
          🏛️ Banco<span>Híbrido</span>
        </div>
        <div className="header-user-info">
          <div className="user-details">
            <div className="user-name">{titularCuenta}</div>
            <div className="account-number">Cuenta: {numeroCuenta || 'N/A'}</div>
          </div>
          <button className="btn-logout" onClick={handleLogout}>
            🚪 Cerrar Sesión
          </button>
        </div>
      </header>

      {/* Contenido Principal */}
      <main className="dashboard-content">
        {/* Columna Izquierda */}
        <section className="control-panel">
          {/* Card Saldo Actual */}
          <div className="balance-card">
            <div className="balance-label">Saldo Actual</div>
            <div className="balance-amount">{formatMoneda(saldoTotal)}</div>
            <span className="balance-tag">LÍMITE DIARIO DISPONIBLE</span>
          </div>

          {/* Card Operación Rápida */}
          <div className="operation-card">
            <h2 className="operation-title">Operación Rápida</h2>

            {/* Selector de Tipo de Operación */}
            <div className="operation-selector">
              <button
                type="button"
                className={`op-btn ${tipoOperacion === 'D' ? 'active deposit' : ''}`}
                onClick={() => {
                  setTipoOperacion('D');
                  setErrorOperacion('');
                }}
              >
                ● D - Depósito
              </button>
              <button
                type="button"
                className={`op-btn ${tipoOperacion === 'R' ? 'active withdrawal' : ''}`}
                onClick={() => {
                  setTipoOperacion('R');
                  setErrorOperacion('');
                }}
              >
                ● R - Retiro
              </button>
            </div>

            <form onSubmit={handleSubmitTransaccion}>
              <div className="form-group">
                <label htmlFor="monto">Monto ($)</label>
                <div className="input-symbol">
                  <span className="currency-prefix">$</span>
                  <input
                    id="monto"
                    type="number"
                    step="0.01"
                    min="0.01"
                    className="form-input amount-input"
                    placeholder="5.000,00"
                    value={monto}
                    onChange={(e) => {
                      setMonto(e.target.value);
                      setErrorOperacion('');
                    }}
                    required
                  />
                </div>
                {errorOperacion && (
                  <div className="op-error-text">
                    ⚠️ {errorOperacion}
                  </div>
                )}
              </div>

              <button
                type="submit"
                className="btn-primary"
                disabled={cargandoEnvio}
              >
                {cargandoEnvio ? 'Procesando...' : 'Confirmar Operación'}
              </button>
            </form>
          </div>
        </section>

        {/* Columna Derecha: Tabla de Historial */}
        <section className="history-card">
          <div className="history-header">
            <div>
              <h2 className="history-title">Últimas Transacciones</h2>
              <p className="history-subtitle">
                Historial de movimientos de tu cuenta híbrida
              </p>
            </div>
            <button className="history-icon-btn" title="Calendario / Filtro">
              📅
            </button>
          </div>

          {cargandoHistorial ? (
            <div className="empty-state">Cargando movimientos...</div>
          ) : transacciones.length === 0 ? (
            <div className="empty-state">
              No hay transacciones registradas en esta cuenta.
            </div>
          ) : (
            <table className="transactions-table">
              <thead>
                <tr>
                  <th>N° Transacción</th>
                  <th>Fecha</th>
                  <th>Tipo</th>
                  <th>Monto</th>
                </tr>
              </thead>
              <tbody>
                {transacciones.map((tx) => {
                  const esPositivo = tx.tipo_operacion === 'D';
                  const signo = esPositivo ? '+' : '-';
                  const montoNum = parseFloat(tx.monto);

                  return (
                    <tr key={tx.id_transaccion}>
                      <td className="tx-id">#{String(tx.id_transaccion).padStart(5, '0')}</td>
                      <td>{formatFecha(tx.fecha_operacion)}</td>
                      <td>
                        <span className={`badge-tipo ${tx.tipo_operacion}`}>
                          ● {tx.tipo_operacion === 'D' ? 'D - Depósito' : tx.tipo_operacion === 'R' ? 'R - Retiro' : 'P - Pago'}
                        </span>
                      </td>
                      <td className={`amount-cell ${esPositivo ? 'positive' : 'negative'}`}>
                        {signo}{formatMoneda(montoNum)}
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}
        </section>
      </main>
    </div>
  );
}