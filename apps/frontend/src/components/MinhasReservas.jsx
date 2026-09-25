
import { Link } from 'react-router-dom'
import { useState } from 'react'

// Dados simulados para desenvolver a interface
const reservas = [
  {
    id: 1,
    hotel: 'Hotel Praia Azul',
    quarto: 'Casal',
    checkin: '10/10/2026',
    checkout: '13/10/2026',
    status: 'Pendente',
  },
  {
    id: 2,
    hotel: 'Vila dos Ventos Resort',
    quarto: 'Casal Luxo',
    checkin: '15/11/2026',
    checkout: '18/11/2026',
    status: 'Confirmada',
  },
  {
    id: 3,
    hotel: 'Hotel Praia Azul',
    quarto: 'Família',
    checkin: '20/10/2026',
    checkout: '23/10/2026',
    status: 'Cancelada',
  },
]

const coresStatus = {
  Pendente: 'bg-warning text-dark',
  Confirmada: 'bg-success',
  Cancelada: 'bg-danger',
}

export default function MinhasReservas() {

    const [reservasExibidas, setReservasExibidas] = useState(reservas)
    const [carregando, setCarregando] = useState(false)
    const [erro, setErro] = useState('')

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
                            {reserva.hotel}
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
                          <strong>Quarto:</strong> {reserva.quarto}
                        </p>

                        <p className="mb-2">
                          <strong>Check-in:</strong> {reserva.checkin}
                        </p>

                        <p className="mb-0">
                          <strong>Check-out:</strong> {reserva.checkout}
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
