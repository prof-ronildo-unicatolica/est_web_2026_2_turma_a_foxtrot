import axios from 'axios';

// Cria uma instância do axios com a URL base da nossa API
const api = axios.create({
  baseURL: 'http://localhost:8000/api/v1', // Confirme com a equipe se esse é o caminho correto no backend
  timeout: 10000, // Se o backend demorar mais de 10 segundos, ele cancela
  headers: {
    'Content-Type': 'application/json',
  }
});

// Futuramente, é aqui que adicionaremos um "Interceptors" para injetar o token JWT 
// e garantir a segurança que o CEO pediu no Estudo de Caso!

export default api;