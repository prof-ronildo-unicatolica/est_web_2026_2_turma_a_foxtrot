import React, { useState, useEffect } from 'react';
import { criarReserva, buscarReservaPorId } from '../services/reservas';

export default function CheckoutReserva({ quartoId, token }) {
  const [dataCheckin, setDataCheckin] = useState('');
  const [dataCheckout, setDataCheckout] = useState('');
  const [adultos, setAdultos] = useState(1);
  const [tarifa, setTarifa] = useState('flexivel');
  
  const [status, setStatus] = useState('idle');
  const [mensagemErro, setMensagemErro] = useState('');
  const [reservaId, setReservaId] = useState(null);
  const [statusFinal, setStatusFinal] = useState('');

  // Lógica de Polling: Consulta o backend a cada 2 segundos
  useEffect(() => {
    let intervalId;

    const consultarStatus = async () => {
      try {
        const dadosReserva = await buscarReservaPorId(reservaId, token);
        console.log('Estado atual no backend:', dadosReserva.status);

        if (dadosReserva.status !== 'Pendente') {
          setStatusFinal(dadosReserva.status);
          setStatus('success');
          clearInterval(intervalId);
        }
      } catch (erro) {
        console.error(erro);
        setMensagemErro('Erro ao verificar o estado da reserva.');
        setStatus('error');
        clearInterval(intervalId);
      }
    };

    if (reservaId && status === 'loading') {
      intervalId = setInterval(consultarStatus, 2000);
    }

    return () => clearInterval(intervalId); // Limpa o intervalo ao desmontar o componente
  }, [reservaId, status, token]);

  const handleSubmeter = async (e) => {
    e.preventDefault();
    setStatus('loading');
    setMensagemErro('');
    setReservaId(null);

    const payload = {
      quarto_id: quartoId,
      data_checkin: dataCheckin,
      data_checkout: dataCheckout,
      quantidade_adultos: parseInt(adultos, 10),
      idades_criancas: [],
      early_checkin: false,
      late_checkout: false,
      necessita_berco: false,
      tarifa_tipo: tarifa,
      servicos_adicionais_ids: []
    };

    try {
      const resposta = await criarReserva(payload, token);
      setReservaId(resposta.id); // Guardamos o ID recebido para disparar o useEffect (polling)
    } catch (erro) {
      setMensagemErro(erro.message);
      setStatus('error');
    }
  };

  return (
    <div className="checkout-container" style={{ padding: '20px', border: '1px solid #ccc', borderRadius: '8px', maxWidth: '500px', margin: '0 auto' }}>
      <h2>Finalizar Reserva</h2>
      
      {status === 'error' && <p style={{ color: 'red', fontWeight: 'bold' }}>{mensagemErro}</p>}
      
      {status === 'success' && (
        <div style={{ padding: '15px', backgroundColor: statusFinal === 'Cancelada' ? '#f8d7da' : '#d4edda', color: statusFinal === 'Cancelada' ? '#721c24' : '#155724', borderRadius: '5px' }}>
          <h3>Processo Concluído!</h3>
          <p>O estado final da sua reserva é: <strong>{statusFinal}</strong></p>
        </div>
      )}

      {status !== 'success' && (
        <form onSubmit={handleSubmeter} style={{ display: 'flex', flexDirection: 'column', gap: '15px' }}>
          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Data de Check-in:</label>
            <input type="date" required value={dataCheckin} onChange={(e) => setDataCheckin(e.target.value)} style={{ width: '100%', padding: '8px' }} />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Data de Check-out:</label>
            <input type="date" required value={dataCheckout} onChange={(e) => setDataCheckout(e.target.value)} style={{ width: '100%', padding: '8px' }} />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Quantidade de Adultos:</label>
            <input type="number" min="1" required value={adultos} onChange={(e) => setAdultos(e.target.value)} style={{ width: '100%', padding: '8px' }} />
          </div>

          <div>
            <label style={{ display: 'block', marginBottom: '5px' }}>Tipo de Tarifa:</label>
            <select value={tarifa} onChange={(e) => setTarifa(e.target.value)} style={{ width: '100%', padding: '8px' }}>
              <option value="flexivel">Flexível</option>
              <option value="nao_reembolsavel">Não Reembolsável</option>
            </select>
          </div>

          <button type="submit" disabled={status === 'loading'} style={{ padding: '10px', backgroundColor: '#0056b3', color: 'white', border: 'none', borderRadius: '4px', cursor: status === 'loading' ? 'not-allowed' : 'pointer' }}>
            {status === 'loading' ? 'A Processar no Backend...' : 'Confirmar Reserva'}
          </button>
        </form>
      )}
    </div>
  );
}