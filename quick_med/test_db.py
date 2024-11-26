import unittest

from quick_med import create_app
from .extensions import db
from .models.banco import Usuario

class FlaskTestCas(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        self.client = self.app.test_client()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()

    # Teste de criação do banco em memoria
    def test_database(self):
        with db.engine.connect() as connec:
            self.assertIsNotNone(connec)

    # Teste no endpoint de criação do usuario
    def test_create_user(self):
        user_data = {
            'nome': 'Roger',
            'email': 'roger@example.com',
            'senha': 'senha123'
        }

        response = self.client.post('/addUser', data=user_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        user_db = db.session.query(Usuario).filter_by(email=user_data['email']).first()
        self.assertIsNotNone(user_db)
        self.assertEqual(user_db.nome, user_data['nome'])



if __name__ == '__main__':
    unittest.main()