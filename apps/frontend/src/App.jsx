import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Navbar from './components/Navbar';

function App() {
  return (
    <BrowserRouter>
      {/* A Navbar fica fora das rotas para aparecer fixada no topo em todas as telas */}
      <Navbar />
      
      <div style={{ padding: '2rem' }}>
        <Routes>
          {/* Rotas Públicas (Hóspedes) */}
          <Route path="/" element={<h2>Página Inicial - Bem-vindo à Rede Hoteleira!</h2>} />
          <Route path="/hoteis" element={<h2>Lista de Hotéis Disponíveis</h2>} />
          
          {/* Rotas Privadas (Gestão) */}
          <Route path="/admin" element={<h2>Dashboard da Franquia (Acesso Restrito)</h2>} />
        </Routes>
      </div>
    </BrowserRouter>
  );
}

export default App;