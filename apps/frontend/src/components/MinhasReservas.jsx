
import { Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import { listarReservas } from '../services/reservas'
import { buscarHoteis } from '../services/api'





const coresStatus = {
  Pendente: 'bg-warning text-dark',
  Confirmada: 'bg-success',
  Cancelada: 'bg-danger',
}

export default function MinhasReservas() {


    const [reservasExibidas, setReservasExibidas] = useState([])
    const [carregando, setCarregando] = useState(true)
    const [erro, setErro] = useState('')
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
            setReservasExibidas(dados)
          }
        } catch (erro) {
          if (ativo) {
            setErro(erro.message || 'Erro ao carregar reservas.')
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

          for (const hotel of hoteis) {
            for (const quarto of hotel.quartos ?? []) {
              mapa[quarto.id] = {
                hotel: hotel.nome,
                numero: quarto.numero,
                tipo: quarto.tipo
              }
            }
          }

          if (ativo) {
            setQuartosPorId(mapa)
          }
        } catch (erro) {
          console.error('Erro ao buscar detalhes dos quartos:', erro)
        }
      }

      carregarDetalhesQuartos()

      return () => {
        ativo = false
      }
    }, [])



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
              Acompanhe suas reservas e consulte o status
              de suas hospedagens.
            </p>

            {carregando ? (

            <div className="text-center py-4">
                <div className="spinner-border text-primary" role="status">
                <span className="visually-hidden">Carregando...</span>
                </div>
                <p className="mt-2">Carregando suas reservas...</p>
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

                {reservasExibidas.map((reserva) => (
                  <div
                    key={reserva.id}
                    className="col-12"
                  >
                    <div className="card shadow-sm">
                      <div className="card-body">

                        <div className="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
                         <h3 className="h5 text-primary fw-bold mb-0">
                          {quartosPorId[reserva.quarto_id]?.hotel || 'Reserva de hospedagem'}
                        </h3>

                          <span
                            className={`badge ${coresStatus[reserva.status]}`}
                          >
                            {reserva.status}
                          </span>
                        </div>

                        <p className="mb-2">
                          <strong>Reserva:</strong> #{reserva.id}
                        </p>


                        <p className="mb-2">
                          <strong>Quarto:</strong>{' '}
                          {quartosPorId[reserva.quarto_id]
                            ? `${quartosPorId[reserva.quarto_id].numero} — ${quartosPorId[reserva.quarto_id].tipo}`
                            : `ID: ${reserva.quarto_id}`}
                        </p>


                        <p className="mb-2">
                          <strong>Check-in:</strong>{' '}
                          {reserva.data_checkin?.split('-').reverse().join('/')}
                        </p>



                        <p className="mb-0">
                          <strong>Check-out:</strong>{' '}
                          {reserva.data_checkout?.split('-').reverse().join('/')}
                        </p>


                        <p className="mb-0 mt-2">
                          <strong>Valor total:</strong>{' '}
                          {Number(reserva.valor_total).toLocaleString('pt-BR', {
                            style: 'currency',
                            currency: 'BRL'
                          })}
                        </p>



                      </div>
                    </div>
                  </div>
                ))}

              </div>
            )}

          </div>
        </div>

      </div>
    </div>
  )
}
