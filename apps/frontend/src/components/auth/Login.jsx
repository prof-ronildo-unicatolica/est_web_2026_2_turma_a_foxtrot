import { useState } from 'react'

const API_URL = 'https://symmetrical-space-barnacle-q7jpp49qvqvwc9446-8000.app.github.dev/api/v1'

export default function Login({ onLogin, onCancel }) {
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [erro, setErro] = useState('')
  const [carregando, setCarregando] = useState(false)

  async function handleSubmit(event) {
    event.preventDefault()
    setErro('')
    setCarregando(true)

    try {
      const response = await fetch(`${API_URL}/auth/login`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          email,
          senha,
        }),
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'E-mail ou senha incorretos')
      }

      localStorage.setItem('access_token', data.access_token)

      onLogin(data.access_token)
    } catch (error) {
      setErro(error.message)
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="container py-5">
      <div className="row justify-content-center">
        <div className="col-md-6 col-lg-5">
          <div className="card shadow-sm">
            <div className="card-body p-4">
              <h2 className="text-center text-primary mb-4">
                Entrar
              </h2>

              {erro && (
                <div className="alert alert-danger" role="alert">
                  {erro}
                </div>
              )}

              <form onSubmit={handleSubmit}>
                <div className="mb-3">
                  <label htmlFor="email" className="form-label">
                    E-mail
                  </label>

                  <input
                    id="email"
                    type="email"
                    className="form-control"
                    value={email}
                    onChange={(event) => setEmail(event.target.value)}
                    placeholder="seu@email.com"
                    required
                  />
                </div>

                <div className="mb-3">
                  <label htmlFor="senha" className="form-label">
                    Senha
                  </label>

                  <input
                    id="senha"
                    type="password"
                    className="form-control"
                    value={senha}
                    onChange={(event) => setSenha(event.target.value)}
                    placeholder="Sua senha"
                    required
                  />
                </div>

                <button
                  type="submit"
                  className="btn btn-primary w-100"
                  disabled={carregando}
                >
                  {carregando ? 'Entrando...' : 'Entrar'}
                </button>
              </form>

              <button
                type="button"
                className="btn btn-link w-100 mt-2"
                onClick={onCancel}
              >
                Voltar
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}
