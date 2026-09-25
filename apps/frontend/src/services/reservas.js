
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