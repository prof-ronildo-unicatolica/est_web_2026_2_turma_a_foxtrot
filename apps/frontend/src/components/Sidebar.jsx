export default function Sidebar() {
  return (
    <div className="bg-dark text-white p-3 rounded shadow-sm h-100">
      <h5 className="text-primary fw-bold mb-4 border-bottom pb-2">
        Menu
      </h5>

      <ul className="nav nav-pills flex-column mb-auto">
        <li className="nav-item mb-2">
          <a
            href="#"
            className="nav-link text-white active"
            aria-current="page"
          >
            Início
          </a>
        </li>

        <li className="nav-item mb-2">
          <a href="#buscar-hoteis" className="nav-link text-white">
            Buscar Hotéis
          </a>
        </li>

        <li className="nav-item mb-2">
          <a href="#minhas-reservas" className="nav-link text-white">
            Minhas Reservas
          </a>
        </li>

        <li className="nav-item mb-2">
          <a href="#perfil" className="nav-link text-white">
            Meu Perfil
          </a>
        </li>

        <li className="nav-item mb-2">
          <a href="#administracao" className="nav-link text-white">
            Administração
          </a>
        </li>
      </ul>
    </div>
  );
}