
import { useState } from 'react'

export default function FormularioAvaliacao({
  onEnviar,
  onCancelar,
  enviando = false,
}) {
  const [nota, setNota] = useState('')
  const [comentario, setComentario] = useState('')

  function handleSubmit(event) {
    event.preventDefault()

    const notaNumerica = Number(nota)

    if (!Number.isInteger(notaNumerica) ||
        notaNumerica < 1 ||
        notaNumerica > 5) {
      return
    }

    onEnviar({
      nota: notaNumerica,
      comentario: comentario.trim() || null,
    })
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="border rounded p-3 mt-3 bg-light"
    >
      <h4 className="h6 fw-bold mb-3">
        Avaliar Estadia
      </h4>

      <div className="mb-3">
        <label
          htmlFor="nota-avaliacao"
          className="form-label"
        >
          Nota da hospedagem
        </label>

        <select
          id="nota-avaliacao"
          className="form-select"
          value={nota}
          onChange={(event) => setNota(event.target.value)}
          disabled={enviando}
          required
        >
          <option value="">Selecione uma nota</option>
          <option value="1">⭐ 1 estrela — Péssima</option>
          <option value="2">⭐⭐ 2 estrelas — Ruim</option>
          <option value="3">⭐⭐⭐ 3 estrelas — Regular</option>
          <option value="4">⭐⭐⭐⭐ 4 estrelas — Boa</option>
          <option value="5">⭐⭐⭐⭐⭐ 5 estrelas — Excelente</option>
        </select>
      </div>

      <div className="mb-3">
        <label
          htmlFor="comentario-avaliacao"
          className="form-label"
        >
          Comentário (opcional)
        </label>

        <textarea
          id="comentario-avaliacao"
          className="form-control"
          rows="3"
          placeholder="Conte como foi sua hospedagem..."
          value={comentario}
          onChange={(event) => setComentario(event.target.value)}
          disabled={enviando}
        />
      </div>

      <div className="d-flex gap-2">
        <button
          type="submit"
          className="btn btn-primary"
          disabled={enviando || !nota}
        >
          {enviando
            ? 'Enviando avaliação...'
            : 'Enviar Avaliação'}
        </button>

        <button
          type="button"
          className="btn btn-outline-secondary"
          onClick={onCancelar}
          disabled={enviando}
        >
          Fechar
        </button>
      </div>
    </form>
  )
}
