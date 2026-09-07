import { useState } from 'react'

export default function AuthForm() {
  const [modo, setModo] = useState('login')

  const [login, setLogin] = useState({
  email: '',
  senha: '',
  })

  const [cadastro, setCadastro] = useState({
    nome: '',
    email: '',
    senha: '',
    confirmarSenha: '',
  })

  const [mensagem, setMensagem] = useState('')

  const [tipoMensagem, setTipoMensagem] = useState('')

  function handleCadastroSubmit(event) {
    event.preventDefault()

    if (
      !cadastro.nome ||
      !cadastro.email ||
      !cadastro.senha ||
      !cadastro.confirmarSenha
    ) {
      setMensagem('Preencha todos os campos.')
      setTipoMensagem('erro')
      return
    }

    if (cadastro.senha !== cadastro.confirmarSenha) {
      setMensagem('As senhas não coincidem.')
      setTipoMensagem('erro')
      return
    }

    setMensagem('Cadastro preenchido corretamente.')
    setTipoMensagem('sucesso')
  }

  function handleLoginSubmit(event) {
    event.preventDefault()

    if (!login.email || !login.senha) {
      setMensagem('Preencha e-mail e senha.')
      setTipoMensagem('erro')
      return
    }

    if (!login.email.includes('@')) {
      setMensagem('Digite um e-mail válido.')
      setTipoMensagem('erro')
      return
    }

    setMensagem('Login preenchido corretamente.')
    setTipoMensagem('sucesso')
  }

  return (
    <div className="card shadow-sm">
      <div className="card-body p-4">
        <h2 className="h4 text-primary fw-bold mb-4">
          {modo === 'login' ? 'Login' : 'Cadastro'}
        </h2>

        <div className="btn-group w-100 mb-4">
          <button
            type="button"
            className={`btn ${
              modo === 'login'
                ? 'btn-primary'
                : 'btn-outline-primary'
            }`}
            onClick={() => setModo('login')}
          >
            Login
          </button>

          <button
            type="button"
            className={`btn ${
              modo === 'cadastro'
                ? 'btn-primary'
                : 'btn-outline-primary'
            }`}
            onClick={() => setModo('cadastro')}
          >
            Cadastro
          </button>
        </div>

       {modo === 'login' && (
        <form onSubmit={handleLoginSubmit}>
          <div className="mb-3">
            <label htmlFor="emailLogin" className="form-label">
              E-mail
            </label>

            <input
              type="email"
              id="emailLogin"
              className="form-control"
              placeholder="Digite seu e-mail"
              value={login.email}
              onChange={(event) =>
              setLogin({
                ...login,
                email: event.target.value,
              })
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
            value={login.senha}
            onChange={(event) =>
              setLogin({
                ...login,
                senha: event.target.value,
              })
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

      {mensagem && (
        <div
          className={`alert ${
            tipoMensagem === 'sucesso'
              ? 'alert-success'
              : 'alert-danger'
          }`}
          role="alert"
        >
          {mensagem}
        </div>
      )}

      {modo === 'cadastro' && (
        <form onSubmit={handleCadastroSubmit}>
          <div className="mb-3">
            <label htmlFor="nomeCadastro" className="form-label">
              Nome
            </label>

            <input
            type="text"
            id="nomeCadastro"
            className="form-control"
            placeholder="Digite seu nome"
            value={cadastro.nome}
            onChange={(event) =>
              setCadastro({
                ...cadastro,
                nome: event.target.value,
              })
            }
          />
          </div>

          <div className="mb-3">
            <label htmlFor="emailCadastro" className="form-label">
              E-mail
            </label>

            <input
            type="email"
            id="emailCadastro"
            className="form-control"
            placeholder="Digite seu e-mail"
            value={cadastro.email}
            onChange={(event) =>
              setCadastro({
                ...cadastro,
                email: event.target.value,
              })
            }
          />
          </div>

          <div className="mb-3">
            <label htmlFor="senhaCadastro" className="form-label">
              Senha
            </label>

            <input
            type="password"
            id="senhaCadastro"
            className="form-control"
            placeholder="Digite sua senha"
            value={cadastro.senha}
            onChange={(event) =>
              setCadastro({
                ...cadastro,
                senha: event.target.value,
              })
            }
          />
          </div>

          <div className="mb-3">
            <label htmlFor="confirmarSenhaCadastro" className="form-label">
              Confirmar Senha
            </label>

            <input
            type="password"
            id="confirmarSenhaCadastro"
            className="form-control"
            placeholder="Confirme sua senha"
            value={cadastro.confirmarSenha}
            onChange={(event) =>
              setCadastro({
                ...cadastro,
                confirmarSenha: event.target.value,
              })
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
      
      </div>
    </div>
  )
}