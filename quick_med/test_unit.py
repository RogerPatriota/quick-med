from unittest import TestCase
from unittest.mock import patch, MagicMock
from quick_med.routes.bP import consultas
from quick_med import create_app

class TestConsultasUnitario(TestCase):
    
    def setUp(self):
        # Cria a aplicação Flask
        self.app = create_app()
        self.app.config['TESTING'] = True

        # Ativa o contexto de aplicação
        self.app_context = self.app.app_context()
        self.app_context.push()

    def tearDown(self):
        # Remove o contexto de aplicação após cada teste
        self.app_context.pop()

    @patch("quick_med.routes.bP.Usuario.query")
    @patch("quick_med.routes.bP.Consulta.query")
    def test_consultas_logic(self, mock_consulta_query, mock_usuario_query):
        # Mock do retorno do usuário
        mock_usuario_query.filter_by.return_value.first.return_value = MagicMock(nome="Test User")

        # Mock do retorno das consultas
        mock_consulta_query.filter_by.return_value.all.return_value = [
            MagicMock(id=1, hospital_id=1),
            MagicMock(id=2, hospital_id=2),
        ]

        # Simula a execução da lógica
        with self.app.test_request_context():
            response = consultas(user_id=1)

        # Verifica se as queries foram chamadas corretamente
        mock_usuario_query.filter_by.assert_called_once_with(id=1)
        mock_consulta_query.filter_by.assert_called_once_with(idUser=1)

        # Você pode validar o comportamento esperado aqui
        # (ex.: verificar se o template correto seria renderizado)