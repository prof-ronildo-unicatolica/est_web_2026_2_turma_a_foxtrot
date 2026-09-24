const API_URL = 'http://localhost:8000/api/v1'

function obterHeaders() {
  const token = localStorage.getItem('access_token')

  const headers = {
    Accept: 'application/json',
  }

  if (token) {
    headers.Authorization = `Bearer ${token}`
  }

  return headers
}

async function tratarResposta(resposta, mensagemPadrao) {
  if (!resposta.ok) {
    const erro = await resposta.json().catch(() => ({}))

    throw new Error(
      erro.detail || mensagemPadrao
    )
  }

  return resposta.json()
}

export async function buscarCidades() {
  const resposta = await fetch(
    `${API_URL}/cidades`,
    {
      method: 'GET',
      headers: obterHeaders(),
    }
  )

  return tratarResposta(
    resposta,
    'Não foi possível carregar as cidades.'
  )
}

export async function buscarHoteis(cidadeId = '') {
  const parametros = new URLSearchParams()

  if (cidadeId) {
    parametros.append('cidade_id', cidadeId)
  }

  const url = parametros.toString()
    ? `${API_URL}/hoteis?${parametros.toString()}`
    : `${API_URL}/hoteis`

  const resposta = await fetch(
    url,
    {
      method: 'GET',
      headers: obterHeaders(),
    }
  )

  return tratarResposta(
    resposta,
    'Não foi possível buscar os hotéis.'
  )
}

export async function buscarSobre() {
  const resposta = await fetch(
    `${API_URL}/sobre`,
    {
      method: 'GET',
      headers: obterHeaders(),
    }
  )

  return tratarResposta(
    resposta,
    'Não foi possível carregar as informações do sistema.'
  )
}