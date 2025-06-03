from app import app
from flask import render_template, request, redirect, url_for
from app.service.auth_service import authenticate
from app.models.agendamento import Agendamento
from app.models.estudio import Estudio
from app.service.auth_service import login_required


@app.route('/adm/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        # Aqui você deve implementar a lógica de autenticação
        if authenticate(username, password):
            return redirect(url_for('home'))
    return render_template('login.html')

app.route('/adm/logout')
def logout():
    from app.service.auth_service import logout
    logout()
    return redirect(url_for('home'))

@app.route('/adm/dashboard')
@login_required # Protege a rota com autenticação
def adm_dashboard():
    return render_template('adm_dashboard.html')


@app.route("/agendamentos/<int:agendamento_id>/delete", methods=["GET", "POST"])
@login_required
def delete(agendamento_id):

    agendamento = Agendamento.query.get(agendamento_id)
    if not agendamento:
        return "Agendamento não encontrado", 404

    agendamento.delete()

    return redirect(url_for("home"))

@app.route("/estudios/add", methods=["GET", "POST"])
@login_required
def add_estudio():
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        estudio = Estudio(nome=nome, descricao=descricao)
        estudio.save()
        return redirect(url_for("home"))
    
    return render_template("add_estudio.html")