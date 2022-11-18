from flask import Blueprint, flash, render_template, request, redirect, url_for, session
from ..extensions import db
from ..models.banco import Hospital, Usuario, Consulta

bP = Blueprint('bP', __name__)

@bP.route('/')
def home(ent_email=0):
    #db.create_all()
    user_query = Usuario.query.filter_by(email = ent_email).first()
    hosp_query = Hospital.query.filter_by(email = ent_email).first()

    if user_query == None:
        return render_template('home_page.html', ent=hosp_query)
    else:
        return render_template('home_page.html', ent=user_query)

@bP.route('/hosp/<hosp_id>')
def home_loggedHosp(hosp_id):
    hosp_query = Hospital.query.filter_by(id = hosp_id).first()
    return render_template('home_page.html', ent=hosp_query, log = 1)

@bP.route('/user/<user_id>')
def home_loggedUser(user_id):
    user_query = Usuario.query.filter_by(id = user_id).first()
    return render_template('home_page.htmL', ent=user_query, log = 0)

@bP.route('/registerUser')
def signupUser():
    return render_template('registerUser_page.html')

@bP.route('/registerHospital')
def signupHospital():
    return render_template('registerHospital_page.html')

@bP.route('/addUser', methods=["POST"])
def cria_contaUser():
    uNome = request.form["nome"]
    uEmail = request.form["email"]
    uSenha = request.form["senha"]

    user = Usuario(nome=uNome, email=uEmail, senha=uSenha)
    db.session.add(user)
    db.session.commit()

    user_query = Usuario.query.filter_by(email = uEmail).first()

    session['usuario_logado'] = user_query.id
    return redirect(url_for("bP.home_loggedUser", user_id = user_query.id))

@bP.route('/addHospital', methods=["POST"])
def cria_contaHosp():
    hNome = request.form["nome"]
    hEmail = request.form["email"]
    hEndereco = request.form["endereco"]
    hEspecialidade = request.form["especialidade"]
    hSenha = request.form["senha"]

    hosp_query = Hospital(nome=hNome, email=hEmail, endereco=hEndereco, especialidade=hEspecialidade, senha=hSenha)
    db.session.add(hosp_query)
    db.session.commit()

    session['hospital_logado'] = hosp_query.id
    return redirect(url_for("bP.home_loggedHosp", hosp_id = hosp_query.id))

@bP.route('/login')
def login():
    return render_template('login_page.html')

@bP.route('/vld', methods=['POST'])
def valida_login():
    eEmail = request.form["email"]
    eSenha = request.form["senha"]

    user_query = Usuario.query.filter_by(email = eEmail, senha = eSenha).first()
    hosp_query = Hospital.query.filter_by(email = eEmail, senha = eSenha).first()

    print(user_query)
    print(hosp_query)
    if user_query == None and hosp_query == None:
        flash('')
        return redirect(url_for('bP.login'))
    elif user_query == None:
        hId = hosp_query.id
        session['hospital_logado'] = hosp_query.id
        return redirect(url_for("bP.home_loggedHosp", hosp_id = hId))
    else:
        uId = user_query.id
        session['usuario_logado'] = user_query.id
        return redirect(url_for("bP.home_loggedUser", user_id = uId))

@bP.route('/marcarconsulta/<user_id>')
def appointment(user_id=0):

    user_query = Usuario.query.filter_by(id = user_id).first()
    hosp_query = Hospital.query.all()
    return render_template('appointment_page.html', user = user_query, hosps = hosp_query, ent=user_query)

@bP.route('/addConsulta/<hosp_id>/<user_id>')
def cria_consulta(hosp_id=0, user_id = 0):

    user_query = Usuario.query.filter_by(id = user_id).first()
    hosp_query = Hospital.query.filter_by(id = hosp_id).first()
    uId = user_query.id

    consulta_query = Consulta(usuario=user_query, hospital=hosp_query)
    db.session.add(consulta_query)
    db.session.commit()

    flash('Consulta agendada com sucesso !!')
    return redirect(url_for("bP.appointment", user_id = uId))

@bP.route('/consultasAgendadas/<user_id>')
def consultas(user_id=0):

    user_query = Usuario.query.filter_by(id = user_id).first()
    consultas_user = Consulta.query.filter_by(idUser = user_id).all()

    return render_template('scheduledAppo_page.html', consultas = consultas_user, ent=user_query) 

@bP.route('/deletar/<user_id>')
def deletar_conta(user_id=0):

    user_query = Usuario.query.filter_by(id = user_id).first()

    return render_template('delete_page.html', user=user_query, ent=user_query)

@bP.route('/deletar', methods=['POST'])
def deletar():
    uId = request.form['id']

    user_query = Usuario.query.filter_by(id = uId).first()
    consultas_user = Consulta.query.filter_by(idUser = uId).all()
    for cons in consultas_user:
        db.session.delete(cons)

    db.session.delete(user_query)
    db.session.commit()

    return redirect(url_for('bP.home'))

@bP.route('/logoff')
def logoff():
     session['usuario_logado'] = None

     return redirect(url_for('bP.home'))

@bP.route('/update/<user_id>')
def update_conta(user_id=0):
     
    user_query = Usuario.query.filter_by(id = user_id).first()

    return render_template('update_page.html', user=user_query, ent=user_query)

@bP.route('/upd', methods=['POST'])
def update_user():
    uId = request.form["id"]
    uNome = request.form["nome"]
    uEmail = request.form["email"]
    uSenha = request.form["senha"]

    user_query = Usuario.query.filter_by(id = uId).first()

    user_query.nome = uNome
    user_query.email = uEmail
    user_query.senha = uSenha
    db.session.add(user_query)
    db.session.commit()

    return redirect(url_for("bP.home_loggedUser", user_id=uId))
