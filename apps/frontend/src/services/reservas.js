
const API_URL = 'http://localhost:8000/api/v1'

async function lerResposta(resposta) {
  return resposta.json().catch(() => null)
}

function mensagemErro(dados, mensagemPadrao) {
  const detalhe = dados?.detail ?? dados?.mensagem ?? dados?.message

  if (typeof detalhe === 'string') {
    return detalhe
  }

  return mensagemPadrao
}

export async function listarReservas(token) {
  const resposta = await fetch(`${API_URL}/reservas`, {
    headers: {
      Authorization: `Bearer ${token}`,
    },
  })

  const dados = await lerResposta(resposta)

  if (!resposta.ok) {
    throw new Error(
      mensagemErro(dados, 'Não foi possível carregar suas reservas.')
    )
  }

  return dados
}

export async function buscarReservaPorId(id, token) {
  const resposta = await fetch(
    `${API_URL}/reservas/${encodeURIComponent(id)}`,
    {
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  const dados = await lerResposta(resposta)

  if (!resposta.ok) {
    throw new Error(
      mensagemErro(dados, 'Não foi possível consultar a reserva.')
    )
  }

  return dados
}

export async function criarReserva(dadosReserva, token) {
  const resposta = await fetch(`${API_URL}/reservas`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
      Authorization: `Bearer ${token}`,
    },
    body: JSON.stringify(dadosReserva),
  })

  const dados = await lerResposta(resposta)

  if (!resposta.ok) {
    throw new Error(
      mensagemErro(
        dados,
        'Não foi possível enviar a reserva para processamento.'
      )
    )
  }

  return dados
}

export async function cancelarReserva(id, token) {
  const resposta = await fetch(
    `${API_URL}/reservas/${encodeURIComponent(id)}/cancelar`,
    {
      method: 'POST',
      headers: {
        Authorization: `Bearer ${token}`,
      },
    }
  )

  const dados = await lerResposta(resposta)

  if (!resposta.ok) {
    if (resposta.status === 404 || resposta.status === 405) {
      throw new Error(
        'Cancelamento indisponível ou reserva não encontrada. ' +
        'Confirme se a API de cancelamento já foi integrada.'
      )
    }

    throw new Error(
      mensagemErro(dados, 'Não foi possível cancelar a reserva.')
    )
  }

  return dados
}
