import unittest

from quick_med import create_app
from .extensions import db
from .models.banco import Hospital, Usuario, Consulta

class FlaskTestCas(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

        self.app_context = self.app.app_context()
        self.app_context.push()

        db.create_all()

        # fixture client
        self.client = self.app.test_client()
        # fixture user
        self.user_fixture = self.create_user()
        # fixture hospital
        self.hosp_fixture = self.create_hosp()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

        self.app_context.pop()
    
    def create_user(self):
        user = Usuario(nome='Roger', email='roger@gmail', senha ='123')
        db.session.add(user)
        db.session.commit()

        return user
    
    def create_hosp(self):
        hosp = Hospital(nome='Hospital Sao Roque', email='saoroque@gov.com',
            endereco= 'av sao roque, 150', especialidade= 'clinico geral',
            senha= 'senhagov123')
        db.session.add(hosp)
        db.session.commit()

        return hosp

    # Teste de criação do banco em memoria
    def test_database(self):
        with db.engine.connect() as connec:
            self.assertIsNotNone(connec)

    # Teste no endpoint de criação do usuario
    def test_create_user(self):
        user_data = {
            'nome': self.user_fixture.nome,
            'email': self.user_fixture.email,
            'senha': self.user_fixture.senha
        }

        response = self.client.post('/addUser', data=user_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        user_db = db.session.query(Usuario).filter_by(email=user_data['email']).first()
        self.assertIsNotNone(user_db)
        self.assertEqual(user_db.nome, user_data['nome'])
    
    # Teste no endpoint de criação do hospital
    def test_create_hop(self):
        hosp_data = {
            'nome': self.hosp_fixture.nome,
            'email': self.hosp_fixture.email,
            'endereco': self.hosp_fixture.endereco,
            'especialidade': self.hosp_fixture.especialidade,
            'senha': self.hosp_fixture.senha,
        }

        response = self.client.post('/addHospital', data=hosp_data, follow_redirects=True)
        
        self.assertEqual(response.status_code, 200)

        hosp_db = db.session.query(Hospital).filter_by(email=hosp_data['email']).first()
        self.assertIsNotNone(hosp_db)
        self.assertEqual(hosp_db.email, hosp_data['email'])

    # Teste no endpoint de criação de consulta
    def test_create_appt(self):
        appt_data = {
            'user': self.user_fixture.id,
            'hosp': self.hosp_fixture.id
        }

        response = self.client.post(f'/addConsulta', data=appt_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        appt_db = db.session.query(Consulta).filter_by(idUser = appt_data['user']).first()
        self.assertIsNotNone(appt_db)
        self.assertEqual(appt_db.idHospitail, appt_data['hosp'])
    
    def test_login_user(self):
        user_data = {
            'email': self.user_fixture.email,
            'senha': self.user_fixture.senha
        }

        response = self.client.post('/vld', data=user_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session:
            self.assertEqual(session['usuario_logado'], self.user_fixture.id)

    def test_login_hosp(self):
        hops_data = {
            'email': self.hosp_fixture.email,
            'senha': self.hosp_fixture.senha
        }
        
        response = self.client.post('/vld', data=hops_data, follow_redirects=True)

        self.assertEqual(response.status_code, 200)
        with self.client.session_transaction() as session:
            self.assertEqual(session['hospital_logado'], self.hosp_fixture.id)


if __name__ == '__main__':
    unittest.main()