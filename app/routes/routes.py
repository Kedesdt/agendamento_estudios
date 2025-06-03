from app import app
from flask import render_template, request, redirect, url_for
import time
from datetime import datetime, timedelta
from app.models.agendamento import Agendamento
from app.models.estudio import Estudio
from app.util.util import get_month_name
from app.service.auth_service import current_user


@app.route("/", methods=["GET", "POST"])
def home():

    estudio_id = request.args.get("estudio_id")
    ano = request.args.get("ano")
    mes = request.args.get("mes")
    estudio = Estudio.get_studio_by_id(estudio_id)

    if estudio is None:
        estudio = Estudio.get_studio_by_id(1)

    estudios = Estudio.get_all_studios()

    hoje = datetime.now()

    if ano and mes:

        ano = int(ano)
        mes = int(mes)
        primeiro_dia_do_mes = datetime(ano, mes, 1)
    else:
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
        estudio=estudio,
        estudios=estudios,
        hoje=hoje.strftime("%m%d"),
        agendamentos=agendamentos,
        get_month_name=get_month_name,
        mes=mes,
        ano=ano,
        mes_anterior=mes_anterior,
        proximo_mes=proximo_mes,
        ano_anterior=ano_anterior,
        proximo_ano=proximo_ano,
        current_user=current_user,
    )


@app.route("/calendario/<int:estudio_id>/<int:mes>/<int:ano>", methods=["GET", "POST"])
def calendario(mes, ano, estudio_id):

    estudio_id = request.form.get("estudio_id", None)
    estudio = Estudio.get_studio_by_id(estudio_id)

    hoje = datetime.now()

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
        data_inicial=domingo_anterior,
        timedelta=timedelta,
        estudio=estudio,
        hoje=hoje.strftime("%m%d"),
        agendamentos=agendamentos,
        get_month_name=get_month_name,
        mes=mes,
        ano=ano,
        mes_anterior=mes_anterior,
        proximo_mes=proximo_mes,
        ano_anterior=ano_anterior,
        proximo_ano=proximo_ano,
    )


@app.route("/calendario/dia/<int:dia>/<int:mes>/<int:ano>", methods=["GET", "POST"])
def calendario_dia(dia, mes, ano):

    estudio_id = request.args.get("estudio_id", None)
    estudio = Estudio.get_studio_by_id(estudio_id)

    hoje = datetime.now()

    data_escolhida = datetime(ano, mes, dia)

    agendamentos = Agendamento.get_agendamentos_by_date_range(
        datainicial=data_escolhida,
        datafinal=data_escolhida + timedelta(days=1),
    )

    return render_template(
        "calendario_dia.html",
        data_escolhida=data_escolhida,
        timedelta=timedelta,
        estudio=estudio,
        hoje=hoje.strftime("%m%d"),
        agendamentos=agendamentos,
    )


@app.route("/agendar", methods=["GET", "POST"])
def agendar():

    estudios = Estudio.get_all_studios()

    if request.method == "POST":
        data = request.form.get("data")
        hora_inicio = request.form.get("hora_inicio")
        hora_fim = request.form.get("hora_fim")
        responsavel = request.form.get("responsavel", "Desconhecido")
        estudio_id = request.form.get("estudio_id")
        estudio = Estudio.get_studio_by_id(estudio_id)

        if not data or not hora_inicio or not hora_fim:
            return "Data e hora são obrigatórios", 400
        data_hora = f"{data} {hora_inicio}"
        data_hora_fim = f"{data} {hora_fim}"

        agendamento = Agendamento(
            estudio_id=estudio.id,
            descricao=request.form.get("descricao", ""),
            data_hora_inicio=datetime.strptime(data_hora, "%Y-%m-%d %H:%M"),
            data_hora_final=datetime.strptime(data_hora_fim, "%Y-%m-%d %H:%M"),
            responsavel=responsavel,
        )

        try:
            agendamento.save()
            return redirect(url_for("home"))
        except ValueError as e:
            error = str(e)

    return render_template(
        "agendar.html", estudios=estudios, error=error if "error" in locals() else None
    )
