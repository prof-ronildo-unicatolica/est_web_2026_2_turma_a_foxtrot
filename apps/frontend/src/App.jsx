import { Routes, Route, Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import ProfessorProfile from './components/ProfessorProfile'
import DisciplinasList from './components/DisciplinasList'
import StacksTable from './components/StacksTable'
import ImageAndCarousel from './components/ImageAndCarousel'
import Sidebar from './components/Sidebar'
import VideoComponent from './components/VideoComponent'
import InteractiveExamples from './components/InteractiveExamples'
import AuthForm from './components/AuthForm'

function HomePage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const [filtros, setFiltros] = useState({
  cidade: '',
  checkin: '',
  checkout: '',
  adultos: 1,
  criancas: 0,
  estrelas: '',
  })

  const [mostrarResultados, setMostrarResultados] = useState(false)

  const [hotelSelecionado, setHotelSelecionado] = useState(null)

  const hoteis = [
    {
      id: 1,
      nome: 'Hotel Praia Azul',
      estrelas: 4,
      preco: 200,
      avaliacao: 4.5,
      comodidades: ['Wi-Fi', 'Piscina', 'Estacionamento'],
      quartos: [
        {
          numero: 101,
          tipo: 'Casal',
          preco: 200,
          capacidade: 'Até 2 adultos e 1 criança',
        },
        {
          numero: 102,
          tipo: 'Família',
          preco: 320,
          capacidade: 'Até 4 adultos e 2 crianças',
        },
      ],
    },
    {
      id: 2,
      nome: 'Vila dos Ventos Resort',
      estrelas: 5,
      preco: 400,
      avaliacao: 4.8,
      comodidades: ['Wi-Fi', 'Piscina', 'Academia', 'Restaurante'],
      quartos: [
        {
          numero: 201,
          tipo: 'Casal Luxo',
          preco: 400,
          capacidade: 'Até 2 adultos e 2 crianças',
        },
        {
          numero: 202,
          tipo: 'Família Premium',
          preco: 550,
          capacidade: 'Até 4 adultos e 2 crianças',
        },
      ],
    },
  ]

  const hoteisFiltrados = hoteis.filter((hotel) => {
    if (!filtros.estrelas) {
      return true
    }

    return hotel.estrelas === Number(filtros.estrelas)
  })

  useEffect(() => {
    fetch('http://localhost:8000/api/v1/sobre')
      .then((res) => {
        if (!res.ok) {
          throw new Error('Falha ao se conectar com a API')
        }
        return res.json()
      })
      .then((json) => {
        setData(json)
        setLoading(false)
      })
      .catch((err) => {
        setError(err.message)
        setLoading(false)
      })
  }, [])

  function handleFiltroChange(event) {
  const { name, value } = event.target

  setFiltros({
    ...filtros,
    [name]: value,
  })
  }

  function handleBuscarHoteis(event) {
    event.preventDefault()

    console.log('Filtros da busca:', filtros)

    setMostrarResultados(true)
  }

  return (
    <div className="bg-light min-vh-100 pb-5">
      {/* Navbar de Exemplo */}
      <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4 sticky-top">
        <div className="container">
          <a className="navbar-brand d-flex align-items-center" href="#">
            <span className="fs-4 fw-bold text-primary">Rede Hoteleira</span>
            <span className="ms-2 badge bg-secondary text-wrap small">Estágio II</span>
          </a>
          <button className="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
            <span className="navbar-toggler-icon"></span>
          </button>
          <div className="collapse navbar-collapse" id="navbarNav">
            <ul className="navbar-nav me-auto">
              <li className="nav-item">
                <a className="nav-link active" href="#">Home</a>
              </li>
              <li className="nav-item">
                <a className="nav-link" href="#tutorial-components">Tutorial</a>
              </li>
            </ul>
            <div className="d-flex align-items-center gap-2">
              <Link
                to="/login"
                className="btn btn-outline-primary btn-sm px-3"
              >
                Login
              </Link>
              <button className="btn btn-primary btn-sm px-3" type="button">
                Perfil
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Cabecalho Principal */}
      <div className="container">
        <header className="mb-5 p-4 bg-white rounded shadow-sm">
          <div className="row align-items-center">
            <div className="col-md-8">
              <h1 className="display-5 text-primary fw-bold">Sistemas de Informação - Estágio II</h1>
              <p className="lead text-secondary mb-0">Projeto Monorepo Base (Boilerplate de Inicialização)</p>
            </div>
            <div className="col-md-4 text-md-end mt-3 mt-md-0">
              <div className="d-flex justify-content-md-end gap-2">
                <button className="btn btn-sm btn-outline-secondary" onClick={() => window.location.reload()}>
                  Recarregar Dados
                </button>
              </div>
            </div>
          </div>
          <hr className="my-4" />
          <div className="row g-3">
            <div className="col-md-3 col-sm-6">
              <strong>Equipe:</strong> <span className="text-secondary ms-1">Foxtrot</span>
            </div>
            <div className="col-md-3 col-sm-6">
              <strong>Professor:</strong> <span className="text-secondary ms-1">{data?.professor?.nome || 'Ronildo Silva'}</span>
            </div>
            <div className="col-md-3 col-sm-6">
              <strong>Ano:</strong> <span className="text-secondary ms-1">{data?.ano || '2026'}</span>
            </div>
            <div className="col-md-3 col-sm-6">
              <strong>Semestre:</strong> <span className="text-secondary ms-1">{data?.semestre || '2'}</span>
            </div>
          </div>
        </header>

        {loading && (
          <div className="text-center my-5 py-5">
            <div className="spinner-border text-primary" role="status">
              <span className="visually-hidden">Carregando dados da API...</span>
            </div>
            <p className="mt-3 text-secondary">Buscando informações do servidor backend...</p>
          </div>
        )}

        {error && (
          <div className="alert alert-danger shadow-sm p-4" role="alert">
            <h4 className="alert-heading fw-bold">Erro de Conexão com o Backend!</h4>
            <p>Não foi possível obter os dados da API em <code>http://localhost:8000/api/v1/sobre</code>.</p>
            <p className="mb-0">Verifique se o backend está rodando e se os bancos de dados foram inicializados com sucesso.</p>
            <hr />
            <p className="mb-0 small text-muted">Detalhe do erro: {error}</p>
          </div>
        )}

        {!loading && !error && data && (
          <div className="row g-4">
            {/* Sidebar Lateral */}
            <div className="col-md-3">
              <Sidebar />
            </div>

            {/* Conteúdo Principal */}
            {/* Conteúdo Principal */}
<div className="col-md-9" id="buscar-hoteis">

  <div className="card shadow-sm">
    <div className="card-body p-4">
      <h2 className="h4 text-primary fw-bold mb-4">
        Buscar Hotéis
      </h2>

      <form onSubmit={handleBuscarHoteis}>
        <div className="row g-3">

          <div className="col-md-4">
            <label htmlFor="cidade" className="form-label">
              Cidade
            </label>
            
            <select
              id="cidade"
              name="cidade"
              className="form-select"
              value={filtros.cidade}
              onChange={handleFiltroChange}
            >
              <option value="">Selecione uma cidade</option>
              <option value="fortaleza">Fortaleza</option>
              <option value="quixada">Quixadá</option>
              <option value="caninde">Canindé</option>
            </select>
          </div>

          <div className="col-md-4">
            <label htmlFor="checkin" className="form-label">
              Check-in
            </label>

            <input
              type="date"
              id="checkin"
              name="checkin"
              className="form-control"
              value={filtros.checkin}
              onChange={handleFiltroChange}
            />

          </div>

          <div className="col-md-4">
            <label htmlFor="checkout" className="form-label">
              Check-out
            </label>
            <input
              type="date"
              id="checkout"
              name="checkout"
              className="form-control"
              value={filtros.checkout}
              onChange={handleFiltroChange}
            />
          </div>

          <div className="col-md-4">
            <label htmlFor="adultos" className="form-label">
              Adultos
            </label>
            <input
              type="number"
              id="adultos"
              name="adultos"
              min="1"
              className="form-control"
              value={filtros.adultos}
              onChange={handleFiltroChange}
            />
          </div>

          <div className="col-md-4">
            <label htmlFor="criancas" className="form-label">
              Crianças
            </label>
            <input
              type="number"
              id="criancas"
              name="criancas"
              min="0"
              className="form-control"
              value={filtros.criancas}
              onChange={handleFiltroChange}
            />
          </div>

          <div className="col-md-4">
            <label htmlFor="estrelas" className="form-label">
              Estrelas
            </label>

            <select
              id="estrelas"
              name="estrelas"
              className="form-select"
              value={filtros.estrelas}
              onChange={handleFiltroChange}
            >
              <option value="">Todas as categorias</option>
              <option value="1">⭐ 1 estrela</option>
              <option value="2">⭐⭐ 2 estrelas</option>
              <option value="3">⭐⭐⭐ 3 estrelas</option>
              <option value="4">⭐⭐⭐⭐ 4 estrelas</option>
              <option value="5">⭐⭐⭐⭐⭐ 5 estrelas</option>
            </select>
          </div>

          <div className="col-md-4 d-flex align-items-end">
            <button
              type="submit"
              className="btn btn-primary w-100"
            >
              Buscar Hotéis
            </button>
          </div>

        </div>
      </form>
    </div>
    {mostrarResultados && (
    <div className="mt-4">
      <h3 className="h5 text-primary fw-bold mb-3 ms-3">
        HOTÉIS ENCONTRADOS
      </h3>
          {hoteisFiltrados.map((hotel) => (
      <div key={hotel.id} className="card shadow-sm mb-3">
        <div className="card-body">
          <h4 className="h5 mb-2">
            {hotel.nome}
          </h4>

          <p className="mb-2">
            {'⭐'.repeat(hotel.estrelas)}
          </p>

          <p className="mb-3">
            Diária a partir de{' '}
            <strong>
              R$ {hotel.preco.toFixed(2).replace('.', ',')}
            </strong>
          </p>

          <button
            type="button"
            className="btn btn-outline-primary"
            onClick={() => setHotelSelecionado(hotel)}
          >
            Ver Detalhes do Hotel
          </button>
        </div>
      </div>
    ))}
      
        {hotelSelecionado && (
          <div className="card shadow-sm mt-4">
            <div className="card-body p-4">
              <h2 className="h4 text-primary fw-bold mb-2">
                {hotelSelecionado.nome}
              </h2>

              <p className="mb-2">
                {'⭐'.repeat(hotelSelecionado.estrelas)}
              </p>

              <p className="mb-3">
                Avaliação média: <strong>{hotelSelecionado.avaliacao} / 5</strong>
              </p>

              <h3 className="h6 fw-bold">
                Comodidades
              </h3>

              <div className="mb-4">
                {hotelSelecionado.comodidades.map((comodidade) => (
                  <span
                    key={comodidade}
                    className="badge bg-secondary me-2 mb-2"
                  >
                    {comodidade}
                  </span>
                ))}
              </div>

              <h3 className="h5 text-primary fw-bold mb-3">
                Quartos disponíveis
              </h3>

              {hotelSelecionado.quartos.map((quarto) => (
                <div
                  key={quarto.numero}
                  className="border rounded p-3 mb-3"
                >
                  <h4 className="h6 fw-bold">
                    Quarto {quarto.numero} - {quarto.tipo}
                  </h4>

                  <p className="mb-1">
                    {quarto.capacidade}
                  </p>

                  <p className="mb-3">
                    Diária: <strong>
                      R$ {quarto.preco.toFixed(2).replace('.', ',')}
                    </strong>
                  </p>

                  <button
                    type="button"
                    className="btn btn-primary"
                  >
                    Reservar
                  </button>
                </div>
              ))}
            </div>
          </div>
    )}  

    </div>
  )}
  </div>
</div>
          </div>
        )}

        <footer className="mt-5 py-4 border-top text-center text-muted">
          <p className="mb-0">
            &copy; {new Date().getFullYear()} - Disciplina de Estágio II. Desenvolvido pela Equipe Foxtrot.
          </p>
        </footer>
      </div>
    </div>
  )
}
export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<AuthForm />} />
    </Routes>
  )
}