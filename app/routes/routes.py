from app import app
from flask import render_template, request
import time
from datetime import datetime, timedelta
from app.models.agendamento import Agendamento
from app.models.estudio import Estudio
from app.util.util import get_month_name


@app.route("/", methods=["GET", "POST"])
def home():

    estudio = None

    if request.method == "POST":
        estudio_id = request.form.get("estudio_id")
        estudio = Estudio.get_studio_by_id(estudio_id)
        estudios = [estudio]

    if estudio is None:
        estudios = Estudio.get_all_studios()

    hoje = datetime.now()
    mes = hoje.month
    ano = hoje.year
    primeiro_dia_do_mes = hoje.replace(day=1)
    ultimo_dia_do_mes = primeiro_dia_do_mes.replace(
        month=(primeiro_dia_do_mes.month % 12) + 1, day=1
    ) - timedelta(days=1)
    dia_da_semana_primeiro_dia = primeiro_dia_do_mes.weekday()
    domingo_anterior = primeiro_dia_do_mes - timedelta(
        days=((dia_da_semana_primeiro_dia + 1) % 7)
    )

    mes_anterior = (
        primeiro_dia_do_mes.month - 1 if primeiro_dia_do_mes.month > 1 else 12
    )
    proximo_mes = primeiro_dia_do_mes.month + 1 if primeiro_dia_do_mes.month < 12 else 1
    ano_anterior = (
        primeiro_dia_do_mes.year - 1
        if primeiro_dia_do_mes.month == 1
        else primeiro_dia_do_mes.year
    )
    proximo_ano = (
        primeiro_dia_do_mes.year + 1
        if primeiro_dia_do_mes.month == 12
        else primeiro_dia_do_mes.year
    )

    agendamentos = Agendamento.get_agendamentos_by_date_range(
        datainicial=domingo_anterior,
        datafinal=ultimo_dia_do_mes,
    )

    return render_template(
        "home.html",
        data_inicial=domingo_anterior,
        timedelta=timedelta,
        estudios=estudios,
        hoje=hoje.day,
        agendamentos=agendamentos,
        get_month_name=get_month_name,
        mes=mes,
        ano=ano,
        mes_anterior=mes_anterior,
        proximo_mes=proximo_mes,
        ano_anterior=ano_anterior,
        proximo_ano=proximo_ano,
    )


@app.route("/calendario/<int:mes>/<int:ano>", methods=["GET", "POST"])
def calendario(mes, ano, estudio_name=None):
    if not estudio_name:

        estudio = Estudio.query.filter_by(nome=estudio_name).first()
        # if not estudio:
        #    return estudio_name, 404

    primeiro_dia_do_mes = datetime(ano, mes, 1)
    ultimo_dia_do_mes = primeiro_dia_do_mes.replace(
        month=(primeiro_dia_do_mes.month % 12) + 1, day=1
    ) - timedelta(days=1)
    dia_da_semana_primeiro_dia = primeiro_dia_do_mes.weekday()
    domingo_anterior = primeiro_dia_do_mes - timedelta(
        days=((dia_da_semana_primeiro_dia + 1) % 7)
    )

    agendamentos = Agendamento.get_agendamentos_by_date_range(
        datainicial=domingo_anterior,
        datafinal=ultimo_dia_do_mes,
    )
    mes_anterior = (
        primeiro_dia_do_mes.month - 1 if primeiro_dia_do_mes.month > 1 else 12
    )
    proximo_mes = primeiro_dia_do_mes.month + 1 if primeiro_dia_do_mes.month < 12 else 1
    ano_anterior = (
        primeiro_dia_do_mes.year - 1
        if primeiro_dia_do_mes.month == 1
        else primeiro_dia_do_mes.year
    )
    proximo_ano = (
        primeiro_dia_do_mes.year + 1
        if primeiro_dia_do_mes.month == 12
        else primeiro_dia_do_mes.year
    )

    return render_template(
        "calendario.html",
        timedelta=timedelta,
        estudio=estudio,
        agendamentos=agendamentos,
        get_month_name=get_month_name,
        mes=mes,
        ano=ano,
        mes_anterior=mes_anterior,
        proximo_mes=proximo_mes,
        ano_anterior=ano_anterior,
        proximo_ano=proximo_ano,
    )


@app.route("/agendar", methods=["GET", "POST"])
def agendar(data):
    estudio_id = request.args.get("estudio_id")
    estudio = Estudio.get_studio_by_id(estudio_id)
    if not estudio:
        return "Estúdio não encontrado", 404

    return render_template("agendar.html", estudio=estudio)
