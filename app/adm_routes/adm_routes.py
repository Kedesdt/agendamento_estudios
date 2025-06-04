from app import app
from flask import render_template, request, redirect, url_for
from app.models.agendamento import Agendamento
from app.models.estudio import Estudio
from flask_login import login_required, current_user



@app.route("/adm/logout")
def logout():
    from app.service.auth_service import logout

    logout()
    return redirect(url_for("index"))


@app.route("/adm/dashboard")
@login_required  # Protege a rota com autenticação
def adm_dashboard():
    return render_template("adm_dashboard.html")


@app.route("/agendamentos/<int:agendamento_id>/delete", methods=["GET", "POST"])
@login_required
def delete(agendamento_id):

    agendamento = Agendamento.query.get(agendamento_id)

    if not agendamento:
        return "Agendamento não encontrado", 404
    
    if agendamento.user_id != current_user.id:
        return "Você não tem permissão para excluir este agendamento", 403

    agendamento.delete()

    return redirect(request.referrer or url_for("home", username=current_user.username))


@app.route("/estudios/add", methods=["GET", "POST"])
@login_required
def add_estudio():
    if request.method == "POST":
        nome = request.form.get("nome")
        descricao = request.form.get("descricao")
        estudio = Estudio(nome=nome, descricao=descricao, user_id=current_user.id)
        estudio.save()
        return redirect(url_for("home", username=current_user.username))

    return render_template("add_estudio.html")
