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

@bP.route('/<hosp_id>')
def home_loggedHosp(hosp_id):
    hosp_query = Hospital.query.filter_by(id = hosp_id).first()

    return render_template('home_page.html', ent=hosp_query)

@bP.route('/<user_id>')
def home_loggedUser(user_id):
    user_query = Usuario.query.filter_by(id = user_id).first()

    return render_template('home_page.htmL', ent=user_query)

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
    uId = user_query.id

    return redirect(url_for("bP.home"))

@bP.route('/addHospital', methods=["POST"])
def cria_contaHosp():
    hNome = request.form["nome"]
    hEmail = request.form["email"]
    hEndereco = request.form["endereco"]
    hEspecialidade = request.form["especialidade"]
    hSenha = request.form["senha"]

    hospt = Hospital(nome=hNome, email=hEmail, endereco=hEndereco, especialidade=hEspecialidade, senha=hSenha)
    db.session.add(hospt)
    db.session.commit()

    return redirect(url_for("bP.home"))

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
        return redirect(url_for("bP.home_loggedHos", hosp_id = hId))
    else:
        uId = user_query.id
        session['usuario_logado'] = user_query.id
        return redirect(url_for("bP.home_loggedUser", user_id = uId))
    