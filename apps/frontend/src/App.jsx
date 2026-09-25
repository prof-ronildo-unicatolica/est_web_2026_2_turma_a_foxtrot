import { Routes, Route, Link } from 'react-router-dom'
import { useEffect, useState } from 'react'
import Sidebar from './components/Sidebar'
import AuthForm from './components/AuthForm'
import MinhasReservas from './components/MinhasReservas'

import {
  buscarCidades,
  buscarHoteis,
  buscarSobre,
} from './services/api'

function HomePage() {
  const [data, setData] = useState(null)
  const [error, setError] = useState(null)
  const [loading, setLoading] = useState(true)

  const [cidades, setCidades] = useState([])
  const [loadingCidades, setLoadingCidades] = useState(true)
  const [erroCidades, setErroCidades] = useState(null)

  const [filtros, setFiltros] = useState({
    cidade: '',
    checkin: '',
    checkout: '',
    adultos: 1,
    criancas: 0,
    estrelas: '',
  })

  const [mostrarResultados, setMostrarResultados] = useState(false)

  const [hoteis, setHoteis] = useState([])
  const [loadingHoteis, setLoadingHoteis] = useState(false)
  const [erroHoteis, setErroHoteis] = useState(null)

  const [hotelSelecionado, setHotelSelecionado] = useState(null)

  // =========================================================
  // CARREGAR INFORMAÇÕES DO SISTEMA
  // =========================================================

  useEffect(() => {
    async function carregarDados() {
      try {
        setLoading(true)
        setError(null)

        const json = await buscarSobre()

        setData(json)
      } catch (err) {
        console.error(
          'Erro ao carregar informações do sistema:',
          err
        )

        setError(err.message)
      } finally {
        setLoading(false)
      }
    }

    carregarDados()
  }, [])

  // =========================================================
  // CARREGAR CIDADES DA API
  // =========================================================

  useEffect(() => {
    async function carregarCidades() {
      try {
        setLoadingCidades(true)
        setErroCidades(null)

        const json = await buscarCidades()

        console.log(
          'Cidades recebidas da API:',
          json
        )

        setCidades(Array.isArray(json) ? json : [])
      } catch (err) {
        console.error(
          'Erro ao carregar cidades:',
          err
        )

        setErroCidades(err.message)
        setCidades([])
      } finally {
        setLoadingCidades(false)
      }
    }

    carregarCidades()
  }, [])

  // =========================================================
  // ALTERAÇÃO DOS FILTROS
  // =========================================================

  function handleFiltroChange(event) {
    const { name, value } = event.target

    setFiltros((estadoAnterior) => ({
      ...estadoAnterior,
      [name]: value,
    }))
  }

  // =========================================================
  // BUSCAR HOTÉIS
  // =========================================================

  async function handleBuscarHoteis(event) {
    event.preventDefault()

    setMostrarResultados(true)
    setLoadingHoteis(true)
    setErroHoteis(null)
    setHoteis([])
    setHotelSelecionado(null)

    try {
      console.log(
        'Buscando hotéis para cidade:',
        filtros.cidade || 'todas'
      )

      const json = await buscarHoteis(
        filtros.cidade
      )

      console.log(
        'Hotéis recebidos da API:',
        json
      )

      setHoteis(
        Array.isArray(json) ? json : []
      )
    } catch (err) {
      console.error(
        'Erro ao buscar hotéis:',
        err
      )

      setErroHoteis(err.message)
      setHoteis([])
    } finally {
      setLoadingHoteis(false)
    }
  }

  // =========================================================
  // FILTRO DE ESTRELAS
  // =========================================================

  const hoteisFiltrados = hoteis.filter(
    (hotel) => {
      if (!filtros.estrelas) {
        return true
      }

      return (
        Number(hotel.categoria_estrelas) ===
        Number(filtros.estrelas)
      )
    }
  )

  return (
    <div className="bg-light min-vh-100 pb-5">

      {/* =====================================================
          NAVBAR
      ====================================================== */}

      <nav className="navbar navbar-expand-lg navbar-dark bg-dark shadow-sm mb-4 sticky-top">
        <div className="container">

          <Link
            className="navbar-brand d-flex align-items-center"
            to="/"
          >
            <span className="fs-4 fw-bold text-primary">
              Rede Hoteleira
            </span>

            <span className="ms-2 badge bg-secondary text-wrap small">
              Estágio II
            </span>
          </Link>

          <button
            className="navbar-toggler"
            type="button"
            data-bs-toggle="collapse"
            data-bs-target="#navbarNav"
            aria-controls="navbarNav"
            aria-expanded="false"
            aria-label="Abrir menu"
          >
            <span className="navbar-toggler-icon"></span>
          </button>

          <div
            className="collapse navbar-collapse"
            id="navbarNav"
          >
            <ul className="navbar-nav me-auto">

              <li className="nav-item">
                <Link
                  className="nav-link active"
                  to="/"
                >
                  Início
                </Link>
              </li>

              <li className="nav-item">
                <a
                  className="nav-link"
                  href="#buscar-hoteis"
                >
                  Buscar Hotéis
                </a>
              </li>

            </ul>

            <div className="d-flex align-items-center gap-2">

              <Link
                to="/login"
                className="btn btn-outline-primary btn-sm px-3"
              >
                Login
              </Link>

              <button
                className="btn btn-primary btn-sm px-3"
                type="button"
              >
                Perfil
              </button>

            </div>
          </div>
        </div>
      </nav>

      {/* =====================================================
          CONTEÚDO
      ====================================================== */}

      <div className="container">

        {/* CABEÇALHO */}

        <header className="mb-5 p-4 bg-white rounded shadow-sm">

          <div className="row align-items-center">

            <div className="col-md-8">

              <h1 className="display-5 text-primary fw-bold">
                Sistemas de Informação - Estágio II
              </h1>

              <p className="lead text-secondary mb-0">
                Projeto Monorepo Base
              </p>

            </div>

            <div className="col-md-4 text-md-end mt-3 mt-md-0">

              <button
                className="btn btn-sm btn-outline-secondary"
                onClick={() =>
                  window.location.reload()
                }
              >
                Recarregar Dados
              </button>

            </div>

          </div>

          <hr className="my-4" />

          <div className="row g-3">

            <div className="col-md-3 col-sm-6">
              <strong>Equipe:</strong>{' '}
              <span className="text-secondary ms-1">
                Foxtrot
              </span>
            </div>

            <div className="col-md-3 col-sm-6">
              <strong>Professor:</strong>{' '}
              <span className="text-secondary ms-1">
                {data?.professor?.nome ||
                  'Ronildo Silva'}
              </span>
            </div>

            <div className="col-md-3 col-sm-6">
              <strong>Ano:</strong>{' '}
              <span className="text-secondary ms-1">
                {data?.ano || '2026'}
              </span>
            </div>

            <div className="col-md-3 col-sm-6">
              <strong>Semestre:</strong>{' '}
              <span className="text-secondary ms-1">
                {data?.semestre || '2'}
              </span>
            </div>

          </div>

        </header>

        {/* ERRO DO BACKEND */}

        {error && (
          <div className="alert alert-danger shadow-sm">
            <strong>
              Erro de conexão com o backend:
            </strong>{' '}
            {error}
          </div>
        )}

        {/* =====================================================
            BUSCAR HOTÉIS
        ====================================================== */}

        <div className="row g-4">

          {/* SIDEBAR */}

          <div className="col-md-3">
            <Sidebar />
          </div>

          {/* CONTEÚDO */}

          <div
            className="col-md-9"
            id="buscar-hoteis"
          >

            <div className="card shadow-sm">

              <div className="card-body p-4">

                <h2 className="h4 text-primary fw-bold mb-4">
                  Buscar Hotéis
                </h2>

                <form
                  onSubmit={handleBuscarHoteis}
                >

                  <div className="row g-3">

                    {/* CIDADE */}

                    <div className="col-md-4">

                      <label
                        htmlFor="cidade"
                        className="form-label"
                      >
                        Cidade
                      </label>

                      <select
                        id="cidade"
                        name="cidade"
                        className="form-select"
                        value={filtros.cidade}
                        onChange={handleFiltroChange}
                        disabled={loadingCidades}
                      >

                        <option value="">
                          Todas as cidades
                        </option>

                        {cidades.map(
                          (cidade) => (
                            <option
                              key={cidade.id}
                              value={cidade.id}
                            >
                              {cidade.nome}
                            </option>
                          )
                        )}

                      </select>

                      {loadingCidades && (
                        <div className="form-text">
                          Carregando cidades...
                        </div>
                      )}

                      {erroCidades && (
                        <div className="text-danger small mt-2">
                          {erroCidades}
                        </div>
                      )}

                    </div>

                    {/* CHECK-IN */}

                    <div className="col-md-4">

                      <label
                        htmlFor="checkin"
                        className="form-label"
                      >
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

                    {/* CHECK-OUT */}

                    <div className="col-md-4">

                      <label
                        htmlFor="checkout"
                        className="form-label"
                      >
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

                    {/* ADULTOS */}

                    <div className="col-md-4">

                      <label
                        htmlFor="adultos"
                        className="form-label"
                      >
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

                    {/* CRIANÇAS */}

                    <div className="col-md-4">

                      <label
                        htmlFor="criancas"
                        className="form-label"
                      >
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

                    {/* ESTRELAS */}

                    <div className="col-md-4">

                      <label
                        htmlFor="estrelas"
                        className="form-label"
                      >
                        Estrelas
                      </label>

                      <select
                        id="estrelas"
                        name="estrelas"
                        className="form-select"
                        value={filtros.estrelas}
                        onChange={handleFiltroChange}
                      >

                        <option value="">
                          Todas as categorias
                        </option>

                        <option value="1">
                          ⭐ 1 estrela
                        </option>

                        <option value="2">
                          ⭐⭐ 2 estrelas
                        </option>

                        <option value="3">
                          ⭐⭐⭐ 3 estrelas
                        </option>

                        <option value="4">
                          ⭐⭐⭐⭐ 4 estrelas
                        </option>

                        <option value="5">
                          ⭐⭐⭐⭐⭐ 5 estrelas
                        </option>

                      </select>

                    </div>

                  </div>

                  <button
                    type="submit"
                    className="btn btn-primary mt-4 px-4"
                    disabled={loadingHoteis}
                  >
                    {loadingHoteis
                      ? 'Buscando...'
                      : 'Buscar hotéis'}
                  </button>

                </form>

              </div>
            </div>

            {/* =================================================
                RESULTADOS
            ================================================== */}

            {mostrarResultados && (

              <div className="mt-4">

                <div className="card shadow-sm">

                  <div className="card-body p-4">

                    <h3 className="h5 text-primary fw-bold mb-4">
                      Hotéis encontrados
                    </h3>

                    {/* LOADING */}

                    {loadingHoteis && (
                      <div className="text-center py-4">

                        <div
                          className="spinner-border text-primary"
                          role="status"
                        >
                          <span className="visually-hidden">
                            Buscando hotéis...
                          </span>
                        </div>

                        <p className="mt-2 text-secondary">
                          Buscando hotéis...
                        </p>

                      </div>
                    )}

                    {/* ERRO */}

                    {erroHoteis && (
                      <div className="alert alert-danger">
                        {erroHoteis}
                      </div>
                    )}

                    {/* NENHUM HOTEL */}

                    {!loadingHoteis &&
                      !erroHoteis &&
                      hoteisFiltrados.length === 0 && (
                        <div className="alert alert-warning">
                          Nenhum hotel encontrado
                          para os filtros
                          selecionados.
                        </div>
                      )}

                    {/* HOTÉIS */}

                    {!loadingHoteis &&
                      !erroHoteis &&
                      hoteisFiltrados.length > 0 && (

                        <div className="row g-3">

                          {hoteisFiltrados.map(
                            (hotel) => (

                              <div
                                className="col-md-6"
                                key={hotel.id}
                              >

                                <div className="card h-100 border">

                                  <div className="card-body">

                                    <h4 className="h5 fw-bold">
                                      {hotel.nome}
                                    </h4>

                                    <p className="mb-2">

                                      <span className="badge bg-primary">
                                        {'⭐'.repeat(
                                          Number(
                                            hotel.categoria_estrelas
                                          ) || 0
                                        )}
                                      </span>

                                    </p>

                                    <p className="mb-2">
                                      <strong>
                                        Categoria:
                                      </strong>{' '}
                                      {
                                        hotel.categoria_estrelas
                                      }{' '}
                                      estrelas
                                    </p>

                                    {hotel.cidade && (
                                      <p className="text-secondary mb-3">
                                        <strong>
                                          Cidade:
                                        </strong>{' '}
                                        {
                                          hotel.cidade.nome
                                        }
                                      </p>
                                    )}

                                    <button
                                      type="button"
                                      className="btn btn-outline-primary"
                                      onClick={() =>
                                        setHotelSelecionado(
                                          hotel
                                        )
                                      }
                                    >
                                      Ver detalhes
                                    </button>

                                  </div>

                                </div>

                              </div>

                            )
                          )}

                        </div>

                      )}

                  </div>

                </div>

              </div>

            )}

            {/* =================================================
                DETALHES DO HOTEL
            ================================================== */}

            {hotelSelecionado && (

              <div className="card shadow-sm mt-4">

                <div className="card-body p-4">

                  <div className="d-flex justify-content-between align-items-center mb-3">

                    <h2 className="h4 text-primary fw-bold mb-0">
                      {hotelSelecionado.nome}
                    </h2>

                    <button
                      type="button"
                      className="btn btn-sm btn-outline-secondary"
                      onClick={() =>
                        setHotelSelecionado(null)
                      }
                    >
                      Fechar
                    </button>

                  </div>

                  <p className="mb-2">
                    <span className="badge bg-primary">
                      {'⭐'.repeat(
                        Number(
                          hotelSelecionado.categoria_estrelas
                        ) || 0
                      )}
                    </span>
                  </p>

                  {hotelSelecionado.cidade && (
                    <p className="text-secondary">
                      <strong>
                        Cidade:
                      </strong>{' '}
                      {
                        hotelSelecionado.cidade.nome
                      }
                    </p>
                  )}

                  <p className="mb-0">
                    <strong>ID:</strong>{' '}
                    {hotelSelecionado.id}
                  </p>

                </div>

              </div>

            )}

          </div>

        </div>

        {/* RODAPÉ */}

        <footer className="text-center text-secondary mt-5 py-4">
          © 2026 - Disciplina de Estágio II.
          Desenvolvido pela Equipe Foxtrot.
        </footer>

      </div>

    </div>
  )
}

// =============================================================
// APP
// =============================================================

export default function App() {
  return (
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route path="/login" element={<AuthForm />} />
      <Route path="/minhas-reservas" element={<MinhasReservas />} /> 
    </Routes>
  )
}