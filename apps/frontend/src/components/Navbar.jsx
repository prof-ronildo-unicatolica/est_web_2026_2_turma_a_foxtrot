import { Link } from 'react-router-dom';

function Navbar() {
  return (
    <nav style={{ padding: '1rem', background: '#2c3e50', display: 'flex', gap: '1rem' }}>
      {/* Usamos Link no lugar de <a> para trocar de tela sem recarregar a página inteira */}
      <Link to="/" style={{ color: 'white', textDecoration: 'none' }}>Home</Link>
      <Link to="/hoteis" style={{ color: 'white', textDecoration: 'none' }}>Hotéis</Link>
      <Link to="/admin" style={{ color: '#f1c40f', textDecoration: 'none', marginLeft: 'auto' }}>Painel do Gestor</Link>
    </nav>
  );
}

export default Navbar;