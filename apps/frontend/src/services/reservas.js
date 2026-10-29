
const API_URL = 'http://localhost:8000/api/v1'

export async function listarReservas(token) {
  const resposta = await fetch(`${API_URL}/reservas`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!resposta.ok) {
    throw new Error('Não foi possível carregar suas reservas.')
  }

  return resposta.json()
}

export async function buscarReservaPorId(id, token) {
  const resposta = await fetch(`${API_URL}/reservas/${encodeURIComponent(id)}`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  if (!resposta.ok) {
    throw new Error('Não foi possível consultar a reserva.')
  }

  return resposta.json()
}
export async function criarReserva(dadosReserva, token) {
  const resposta = await fetch(`${API_URL}/reservas`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(dadosReserva),
  });

  if (!resposta.ok) {
    throw new Error('Não foi possível enviar a reserva para processamento.');
  }

  return resposta.json();
}