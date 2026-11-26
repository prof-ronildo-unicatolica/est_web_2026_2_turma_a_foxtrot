
const API_URL = 'http://localhost:8000/api/v1'

export async function criarAvaliacao(dadosAvaliacao, token) {
  if (!token) {
    throw new Error('Faça login para avaliar sua estadia.')
  }

  const resposta = await fetch(`${API_URL}/avaliacoes`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify({
      reserva_id: dadosAvaliacao.reserva_id,
      nota: Number(dadosAvaliacao.nota),
      comentario: dadosAvaliacao.comentario?.trim() || null,
    }),
  })

  const dados = await resposta.json().catch(() => null)

  if (!resposta.ok) {
    const detalhe = dados?.detail

    const mensagem =
      typeof detalhe === 'string'
        ? detalhe
        : 'Não foi possível registrar sua avaliação.'

    if (resposta.status === 401) {
      throw new Error('Sua sessão expirou. Faça login novamente.')
    }

    throw new Error(mensagem)
  }

  return dados
}
