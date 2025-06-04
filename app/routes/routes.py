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



@app.route("/adm/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        # Aqui você deve implementar a lógica de autenticação
        if authenticate(username, password):
            return redirect(url_for("home", username=username))
    return render_template("login.html")

@app.route("/adm/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        name = request.form.get("name")
        password = request.form.get("password")

        if not username or not email or not name or not password:
            error = "Todos os campos são obrigatórios"
            return render_template("register.html", error=error)

        user = User(username=username, email=email, name=name)
        user.set_password(password)

        try:
            user.save()
            return redirect(url_for("login"))
        except ValueError as e:
            error = str(e)
            return render_template("register.html", error=error)

    return render_template("register.html")

@app.route("/", methods=["GET", "POST"])
def index():
    
    if current_user.is_authenticated:
        return redirect(url_for("home", username=current_user.username))
    return redirect(url_for("login"))

    """error = None
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if not username or not password:
            error = "Usuário e senha são obrigatórios"
        else:
            user = User.authenticate(username, password)
            if user:
                return redirect(url_for("home", username=user.username))
            else:
                error = "Usuário ou senha inválidos"

    return render_template("index.html", error=error)"""

@app.route("/<username>/", methods=["GET", "POST"])
def home(username):

    user = User.get_user_by_username(username)

    if user is None:
        return "Usuário não encontrado", 404
    
    estudio = None

    estudio_id = request.args.get("estudio_id", None)
    ano = request.args.get("ano")
    mes = request.args.get("mes")
    if estudio_id:
        estudio = Estudio.get_studio_by_id(estudio_id)

    if estudio is None:
        estudio = user.estudios[0] if user.estudios else None

    estudios = user.estudios

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
        user_id=user.id,
        datainicial=domingo_anterior,
        datafinal=ultimo_dia_do_mes,
    )

    return render_template(
        "home.html",
        data_inicial=domingo_anterior,
        timedelta=timedelta,
        user=user,
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


@app.route("/<username>/calendario/<int:estudio_id>/<int:mes>/<int:ano>", methods=["GET", "POST"])
def calendario(mes, ano, estudio_id, username):

    user = User.get_user_by_username(username)
    if user is None:
        return "Usuário não encontrado", 404

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
        user=user,
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


@app.route("/<username>/calendario/dia/<int:dia>/<int:mes>/<int:ano>", methods=["GET", "POST"])
def calendario_dia(username, dia, mes, ano):

    user = User.get_user_by_username(username)
    if user is None:
        return "Usuário não encontrado", 404
    estudio_id = request.args.get("estudio_id", None)
    estudio = Estudio.get_studio_by_id(estudio_id)

    hoje = datetime.now()

    data_escolhida = datetime(ano, mes, dia)

    agendamentos = Agendamento.get_agendamentos_by_date_range(
        user_id=user.id,
        datainicial=data_escolhida,
        datafinal=data_escolhida + timedelta(days=1),
    )

    return render_template(
        "calendario_dia.html",
        data_escolhida=data_escolhida,
        timedelta=timedelta,
        estudio=estudio,
        user=user,
        hoje=hoje.strftime("%m%d"),
        agendamentos=agendamentos,
    )


@app.route("/<username>/agendar", methods=["GET", "POST"])
def agendar(username):
    user = User.get_user_by_username(username)
    if user is None:
        return "Usuário não encontrado", 404
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
            user_id=user.id,
            descricao=request.form.get("descricao", ""),
            data_hora_inicio=datetime.strptime(data_hora, "%Y-%m-%d %H:%M"),
            data_hora_final=datetime.strptime(data_hora_fim, "%Y-%m-%d %H:%M"),
            responsavel=responsavel,
        )

        try:
            agendamento.save()
            return redirect(url_for("home", username=username))
        except ValueError as e:
            error = str(e)

    return render_template(
        "agendar.html", estudios=estudios, error=error if "error" in locals() else None
    )
