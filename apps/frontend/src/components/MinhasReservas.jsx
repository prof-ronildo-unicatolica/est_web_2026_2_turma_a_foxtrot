
import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import {
  listarReservas,
  cancelarReserva,
} from '../services/reservas'
import { buscarHoteis } from '../services/api'

const coresStatus = {
  Pendente: 'bg-warning text-dark',
  Confirmada: 'bg-success',
  Cancelada: 'bg-danger',
}

function formatarData(data) {
  if (!data) return 'Não informado'

  const [ano, mes, dia] = String(data).slice(0, 10).split('-')

  if (!ano || !mes || !dia) return String(data)

  return `${dia}/${mes}/${ano}`
}

function formatarMoeda(valor) {
  if (valor === null || valor === undefined || valor === '') {
    return 'A confirmar'
  }

  const numero = Number(valor)

  if (!Number.isFinite(numero)) return 'A confirmar'

  return numero.toLocaleString('pt-BR', {
    style: 'currency',
    currency: 'BRL',
  })
}

function obterDataLocal() {
  const agora = new Date()

  const ano = agora.getFullYear()
  const mes = String(agora.getMonth() + 1).padStart(2, '0')
  const dia = String(agora.getDate()).padStart(2, '0')

  return `${ano}-${mes}-${dia}`
}

// Sprint 8: prazo gratuito de dois dias antes do check-in.
function calcularPrazoCancelamento(reserva) {
  if (reserva.tarifa_tipo !== 'flexivel') return null

  const data = String(reserva.data_checkin || '').slice(0, 10)

  if (!/^\d{4}-\d{2}-\d{2}$/.test(data)) return null

  const [ano, mes, dia] = data.split('-').map(Number)

  const checkin = new Date(Date.UTC(ano, mes - 1, dia))

  if (
    checkin.getUTCFullYear() !== ano ||
    checkin.getUTCMonth() !== mes - 1 ||
    checkin.getUTCDate() !== dia
  ) {
    return null
  }

  checkin.setUTCDate(checkin.getUTCDate() - 2)

  return checkin.toISOString().slice(0, 10)
}

function calcularMultaExibida(reserva, quarto) {
  if (reserva.status === 'Cancelada') {
    return {
      valor: reserva.valor_multa_cancelamento,
      descricao: 'Multa registrada após o cancelamento.',
    }
  }

  if (reserva.tarifa_tipo === 'nao_reembolsavel') {
    return {
      valor: reserva.valor_total,
      descricao: 'Estimativa: 100% do valor da reserva.',
    }
  }

  const prazo = calcularPrazoCancelamento(reserva)
  const hoje = obterDataLocal()

  if (reserva.tarifa_tipo === 'flexivel' && prazo) {
    if (hoje <= prazo) {
      return {
        valor: 0,
        descricao: 'Estimativa: cancelamento gratuito dentro do prazo.',
      }
    }

    if (quarto?.preco_diaria != null) {
      return {
        valor: quarto.preco_diaria,
        descricao: 'Estimativa: multa equivalente a uma diária.',
      }
    }
  }

  return {
    valor: null,
    descricao: 'Valor a confirmar com a API de cancelamento.',
  }
}

export default function MinhasReservas() {
  const [reservasExibidas, setReservasExibidas] = useState([])
  const [carregando, setCarregando] = useState(true)
  const [erro, setErro] = useState('')
  const [erroAcao, setErroAcao] = useState('')
  const [sucesso, setSucesso] = useState('')
  const [cancelandoId, setCancelandoId] = useState(null)
  const [quartosPorId, setQuartosPorId] = useState({})

  useEffect(() => {
    let ativo = true
    const token = localStorage.getItem('access_token')

    if (!token) {
      setErro('Faça login para visualizar suas reservas.')
      setCarregando(false)
      return
    }

    async function carregarReservas() {
      try {
        const dados = await listarReservas(token)

        if (ativo) {
          setReservasExibidas(Array.isArray(dados) ? dados : [])
        }
      } catch (falha) {
        if (ativo) {
          setErro(falha.message || 'Erro ao carregar reservas.')
        }
      } finally {
        if (ativo) {
          setCarregando(false)
        }
      }
    }

    carregarReservas()

    return () => {
      ativo = false
    }
  }, [])

  useEffect(() => {
    let ativo = true

    async function carregarDetalhesQuartos() {
      try {
        const hoteis = await buscarHoteis()
        const mapa = {}

        for (const hotel of Array.isArray(hoteis) ? hoteis : []) {
          for (const quarto of hotel.quartos ?? []) {
            mapa[quarto.id] = {
              hotel: hotel.nome,
              numero: quarto.numero,
              tipo: quarto.tipo,
              preco_diaria: quarto.preco_diaria,
            }
          }
        }

        if (ativo) {
          setQuartosPorId(mapa)
        }
      } catch (falha) {
        console.error('Erro ao buscar detalhes dos quartos:', falha)
      }
    }

    carregarDetalhesQuartos()

    return () => {
      ativo = false
    }
  }, [])

  async function handleCancelar(reserva, multa) {
    const token = localStorage.getItem('access_token')

    setErroAcao('')
    setSucesso('')

    if (!token) {
      setErroAcao('Sua sessão expirou. Faça login novamente.')
      return
    }

    if (cancelandoId !== null) return

    const valorMulta = multa.valor == null
      ? 'a confirmar pela API'
      : formatarMoeda(multa.valor)

    const confirmou = window.confirm(
      `Deseja realmente cancelar a reserva?\n\n` +
      `Reserva: ${reserva.id}\n` +
      `Multa estimada: ${valorMulta}\n\n` +
      `O valor definitivo será calculado pelo servidor.\n` +
      `Esta ação poderá ser irreversível.`
    )

    if (!confirmou) return

    setCancelandoId(reserva.id)

    try {
      await cancelarReserva(reserva.id, token)

      try {
        const atualizadas = await listarReservas(token)

        const lista = Array.isArray(atualizadas)
          ? atualizadas
          : []

        setReservasExibidas(lista)

        const atual = lista.find(
          (item) => item.id === reserva.id
        )

        if (atual?.status === 'Cancelada') {
          setSucesso('Reserva cancelada com sucesso.')
        } else {
          setSucesso(
            'Solicitação enviada. Consulte o status atualizado da reserva.'
          )
        }
      } catch {
        setSucesso(
          'Solicitação enviada, mas não foi possível atualizar a lista. ' +
          'Recarregue a página para consultar o resultado.'
        )
      }
    } catch (falha) {
      setErroAcao(
        falha.message || 'Não foi possível solicitar o cancelamento.'
      )
    } finally {
      setCancelandoId(null)
    }
  }

  return (
    <div className="bg-light min-vh-100 py-5">
      <div className="container">
        <div className="card shadow-sm">
          <div className="card-body p-4">
            <Link
              to="/"
              className="btn btn-outline-primary mb-4"
            >
              ← Voltar para a Home
            </Link>

            <h2 className="h4 text-primary fw-bold mb-3">
              Minhas Reservas
            </h2>

            <p className="text-muted mb-4">
              Acompanhe suas reservas, consulte as condições
              e solicite cancelamentos.
            </p>

            {erroAcao && (
              <div className="alert alert-danger" role="alert">
                {erroAcao}
              </div>
            )}

            {sucesso && (
              <div className="alert alert-success" role="status">
                {sucesso}
              </div>
            )}

            {carregando ? (
              <div className="text-center py-4">
                <div
                  className="spinner-border text-primary"
                  role="status"
                >
                  <span className="visually-hidden">
                    Carregando...
                  </span>
                </div>

                <p className="mt-2">
                  Carregando suas reservas...
                </p>
              </div>
            ) : erro ? (
              <div className="alert alert-danger" role="alert">
                {erro}
              </div>
            ) : reservasExibidas.length === 0 ? (
              <div className="alert alert-info">
                Você ainda não possui reservas.
              </div>
            ) : (
              <div className="row g-3">
                {reservasExibidas.map((reserva) => {
                  const quarto = quartosPorId[reserva.quarto_id]

                  const prazo = calcularPrazoCancelamento(reserva)
                  const multa = calcularMultaExibida(reserva, quarto)

                  const podeSolicitar = [
                    'Confirmada',
                    'Pendente',
                  ].includes(reserva.status)

                  return (
                    <div key={reserva.id} className="col-12">
                      <div className="card shadow-sm">
                        <div className="card-body">
                          <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
                            <h3 className="h5 text-primary fw-bold mb-0">
                              {quarto?.hotel || 'Reserva de hospedagem'}
                            </h3>

                            <span
                              className={`badge ${
                                coresStatus[reserva.status] ||
                                'bg-secondary'
                              }`}
                            >
                              {reserva.status}
                            </span>
                          </div>

                          <p className="mb-2">
                            <strong>Reserva:</strong> #{reserva.id}
                          </p>

                          <p className="mb-2">
                            <strong>Quarto:</strong>{' '}
                            {quarto
                              ? `${quarto.numero} — ${quarto.tipo}`
                              : `ID: ${reserva.quarto_id}`}
                          </p>

                          <p className="mb-2">
                            <strong>Check-in:</strong>{' '}
                            {formatarData(reserva.data_checkin)}
                          </p>

                          <p className="mb-2">
                            <strong>Check-out:</strong>{' '}
                            {formatarData(reserva.data_checkout)}
                          </p>

                          <p className="mb-2">
                            <strong>Valor total:</strong>{' '}
                            {formatarMoeda(reserva.valor_total)}
                          </p>

                          <hr />

                          <h4 className="h6 fw-bold">
                            Condições de cancelamento
                          </h4>

                          <p className="mb-2">
                            <strong>Tarifa:</strong>{' '}
                            {reserva.tarifa_tipo === 'nao_reembolsavel'
                              ? 'Não reembolsável'
                              : 'Flexível'}
                          </p>

                          <p className="mb-2">
                            <strong>Prazo sem multa:</strong>{' '}
                            {reserva.tarifa_tipo === 'nao_reembolsavel'
                              ? 'Não disponível para esta tarifa'
                              : prazo
                                ? formatarData(prazo)
                                : 'A confirmar'}
                          </p>

                          <p className="mb-1">
                            <strong>
                              {reserva.status === 'Cancelada'
                                ? 'Multa aplicada:'
                                : 'Multa prevista:'}
                            </strong>{' '}
                            {multa.valor == null
                              ? 'A confirmar'
                              : formatarMoeda(multa.valor)}
                          </p>

                          <p className="text-muted small mb-3">
                            {multa.descricao}
                          </p>

                          {podeSolicitar && (
                            <button
                              type="button"
                              className="btn btn-outline-danger"
                              disabled={cancelandoId !== null}
                              onClick={() =>
                                handleCancelar(reserva, multa)
                              }
                            >
                              {cancelandoId === reserva.id
                                ? 'Solicitando cancelamento...'
                                : 'Cancelar Reserva'}
                            </button>
                          )}

                          {reserva.status === 'Cancelada' && (
                            <p className="text-danger fw-semibold mb-0">
                              Esta reserva já foi cancelada.
                            </p>
                          )}
                        </div>
                      </div>
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
