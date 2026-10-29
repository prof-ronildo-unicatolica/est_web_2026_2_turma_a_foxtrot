import { useState } from 'react'
import { useNavigate } from 'react-router-dom'

export default function AuthForm() {
  const navigate = useNavigate()

  const [modo, setModo] = useState('login')
  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')
  const [nome, setNome] = useState('')
  const [confirmarSenha, setConfirmarSenha] = useState('')
  const [mensagem, setMensagem] = useState('')
  const [carregando, setCarregando] = useState(false)

  async function handleLogin(event) {
    event.preventDefault()
    setMensagem('')

    if (!email || !senha) {
      setMensagem('Preencha e-mail e senha.')
      return
    }

    setCarregando(true)

    try {
      const resposta = await fetch(
        'http://127.0.0.1:8000/api/v1/auth/login',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email,
            senha,
          }),
        }
      )

      const dados = await resposta.json()

      if (!resposta.ok) {
        setMensagem(dados.detail || 'Erro ao fazer login.')
        return
      }

      if (!dados.access_token) {
        setMensagem('A API não retornou um token de acesso.')
        return
      }

      // Armazena o token de autenticação
      localStorage.setItem('access_token', dados.access_token)

      // Redireciona automaticamente para a página inicial
      navigate('/', { replace: true })
    } catch (erro) {
      console.error('Erro no login:', erro)
      setMensagem('Não foi possível conectar ao servidor.')
    } finally {
      setCarregando(false)
    }
  }

  async function handleCadastro(event) {
    event.preventDefault()
    setMensagem('')

    if (!nome || !email || !senha || !confirmarSenha) {
      setMensagem('Preencha todos os campos.')
      return
    }

    if (senha !== confirmarSenha) {
      setMensagem('As senhas não coincidem.')
      return
    }

    setCarregando(true)

    try {
      const resposta = await fetch(
        'http://127.0.0.1:8000/api/v1/auth/register',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            nome,
            email,
            senha,
          }),
        }
      )

      const dados = await resposta.json()

      if (!resposta.ok) {
        setMensagem(dados.detail || 'Erro ao realizar cadastro.')
        return
      }

      setMensagem('Cadastro realizado com sucesso! Faça login.')

      setNome('')
      setSenha('')
      setConfirmarSenha('')
      setModo('login')
    } catch (erro) {
      console.error('Erro no cadastro:', erro)
      setMensagem('Não foi possível conectar ao servidor.')
    } finally {
      setCarregando(false)
    }
  }

  return (
    <div className="card shadow-sm auth-hotelaria">
      <div className="card-body p-0">

        <h2 className="h4 text-primary fw-bold mb-4">
          {modo === 'login' ? 'Login' : 'Cadastro'}
        </h2>

        <div className="btn-group w-100 mb-4">
          <button
            type="button"
            className={
              modo === 'login'
                ? 'btn btn-primary'
                : 'btn btn-outline-primary'
            }
            onClick={() => {
              setModo('login')
              setMensagem('')
            }}
          >
            Login
          </button>

          <button
            type="button"
            className={
              modo === 'cadastro'
                ? 'btn btn-primary'
                : 'btn btn-outline-primary'
            }
            onClick={() => {
              setModo('cadastro')
              setMensagem('')
            }}
          >
            Cadastro
          </button>
        </div>

        {modo === 'login' && (
          <form onSubmit={handleLogin}>
            <div className="mb-3">
              <label
                htmlFor="emailLogin"
                className="form-label"
              >
                E-mail
              </label>

              <input
                type="email"
                id="emailLogin"
                className="form-control"
                placeholder="Digite seu e-mail"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                required
              />
            </div>

            <div className="mb-3">
              <label
                htmlFor="senhaLogin"
                className="form-label"
              >
                Senha
              </label>

              <input
                type="password"
                id="senhaLogin"
                className="form-control"
                placeholder="Digite sua senha"
                value={senha}
                onChange={(event) =>
                  setSenha(event.target.value)
                }
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
        )}

        {modo === 'cadastro' && (
          <form onSubmit={handleCadastro}>
            <div className="mb-3">
              <label
                htmlFor="nomeCadastro"
                className="form-label"
              >
                Nome
              </label>

              <input
                type="text"
                id="nomeCadastro"
                className="form-control"
                placeholder="Digite seu nome"
                value={nome}
                onChange={(event) =>
                  setNome(event.target.value)
                }
                required
              />
            </div>

            <div className="mb-3">
              <label
                htmlFor="emailCadastro"
                className="form-label"
              >
                E-mail
              </label>

              <input
                type="email"
                id="emailCadastro"
                className="form-control"
                placeholder="Digite seu e-mail"
                value={email}
                onChange={(event) =>
                  setEmail(event.target.value)
                }
                required
              />
            </div>

            <div className="mb-3">
              <label
                htmlFor="senhaCadastro"
                className="form-label"
              >
                Senha
              </label>

              <input
                type="password"
                id="senhaCadastro"
                className="form-control"
                placeholder="Digite sua senha"
                value={senha}
                onChange={(event) =>
                  setSenha(event.target.value)
                }
                required
              />
            </div>

            <div className="mb-3">
              <label
                htmlFor="confirmarSenhaCadastro"
                className="form-label"
              >
                Confirmar Senha
              </label>

              <input
                type="password"
                id="confirmarSenhaCadastro"
                className="form-control"
                placeholder="Confirme sua senha"
                value={confirmarSenha}
                onChange={(event) =>
                  setConfirmarSenha(event.target.value)
                }
                required
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary w-100"
              disabled={carregando}
            >
              {carregando ? 'Cadastrando...' : 'Cadastrar'}
            </button>
          </form>
        )}

        {mensagem && (
          <div className="alert alert-info mt-3" role="alert">
            {mensagem}
          </div>
        )}

      </div>
    </div>
  )
}