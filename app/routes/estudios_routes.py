from app import app
from flask import render_template, request, redirect, url_for
from app.service.auth_service import authenticate
import time
from datetime import datetime, timedelta
from app.models.agendamento import Agendamento
from app.models.estudio import Estudio
from app.models.user import User
from app.util.util import get_month_name
from flask_login import current_user


@app.route("/<username>/estudios", methods=["GET"])
def estudios(username):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    user = User.get_user_by_username(username)
    if not user:
        return "Usuário não encontrado", 404
    if user.id != current_user.id:
        return "Você não tem permissão para acessar os estudios deste usuário", 403

    estudios = Estudio.get_studios_by_user_id(user.id)
    return render_template(
        "estudios.html", username=username, user=user, estudios=estudios
    )


@app.route("/<username>/estudios/<int:estudio_id>/delete", methods=["GET", "POST"])
def delete_estudio(username, estudio_id):
    if not current_user.is_authenticated:
        return redirect(url_for("login"))

    user = User.get_user_by_username(username)
    if not user:
        return "Usuário não encontrado", 404
    if user.id != current_user.id:
        return "Você não tem permissão para acessar os estudios deste usuário", 403

    estudio = Estudio.get_studio_by_id_safe(user.id, estudio_id)
    if not estudio:
        return "Estúdio não encontrado", 404

    estudio.delete()
    return redirect(url_for("estudios", username=username))
