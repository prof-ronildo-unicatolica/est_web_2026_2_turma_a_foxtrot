
import { useState } from 'react'

export default function AuthForm() {
  const [modo, setModo] = useState('login')

  const [email, setEmail] = useState('')
  const [senha, setSenha] = useState('')

  const [nome, setNome] = useState('')
  const [confirmarSenha, setConfirmarSenha] = useState('')

  const [mensagem, setMensagem] = useState('')

  // LOGIN
  async function handleLogin(event) {
    event.preventDefault()

    if (!email || !senha) {
      setMensagem('Preencha e-mail e senha.')
      return
    }

    try {
      const resposta = await fetch(
        'http://127.0.0.1:8000/api/v1/auth/login',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            email: email,
            senha: senha,
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

      localStorage.setItem('access_token', dados.access_token)

      setMensagem('Login realizado com sucesso!')
    } catch (erro) {
      setMensagem('Não foi possível conectar ao servidor.')
    }
  }

  // CADASTRO
  async function handleCadastro(event) {
    event.preventDefault()

    if (!nome || !email || !senha || !confirmarSenha) {
      setMensagem('Preencha todos os campos.')
      return
    }

    if (senha !== confirmarSenha) {
      setMensagem('As senhas não coincidem.')
      return
    }

    try {
      const resposta = await fetch(
        'http://127.0.0.1:8000/api/v1/auth/register',
        {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            nome: nome,
            email: email,
            senha: senha,
          }),
        }
      )

      const dados = await resposta.json()

      if (!resposta.ok) {
        setMensagem(dados.detail || 'Erro ao realizar cadastro.')
        return
      }

      setMensagem('Cadastro realizado com sucesso!')

      setNome('')
      setEmail('')
      setSenha('')
      setConfirmarSenha('')
    } catch (erro) {
      setMensagem('Não foi possível conectar ao servidor.')
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
              <label htmlFor="emailLogin" className="form-label">
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
              />
            </div>

            <div className="mb-3">
              <label htmlFor="senhaLogin" className="form-label">
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
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary w-100"
            >
              Entrar
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
              />
            </div>

            <button
              type="submit"
              className="btn btn-primary w-100"
            >
              Cadastrar
            </button>
          </form>
        )}

        {mensagem && (
          <div className="alert alert-info mt-3">
            {mensagem}
          </div>
        )}
      </div>
    </div>
  )
}