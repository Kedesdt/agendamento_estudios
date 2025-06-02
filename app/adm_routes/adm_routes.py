from app import app
from flask import render_template, request, redirect, url_for
import time
from datetime import datetime, timedelta
from app.models.agendamento import Agendamento
from app.service.auth_service import login_required


@app.route("/agendamentos/<int:agendamento_id>/delete", methods=["GET", "POST"])
@login_required
def delete(agendamento_id):

    agendamento = Agendamento.query.get(agendamento_id)
    if not agendamento:
        return "Agendamento não encontrado", 404

    agendamento.delete()

    return redirect(url_for("home"))
