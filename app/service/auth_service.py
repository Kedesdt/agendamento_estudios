from flask import request, redirect, url_for
from app.models.user import User
from flask_login import (
    LoginManager,
    UserMixin,
    login_user,
    logout_user,
    login_required,
    current_user,
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Configurando o gerenciador de login
login_manager = LoginManager()
login_manager.login_view = "login"


@login_manager.user_loader
def load_user(user_id):
    return User.get_user_by_id(user_id)


# Função de autenticação
def authenticate(username, password):
    #user = users.get(username)
    user = User.get_user_by_username(username)

    if user and user.check_password(password):
        login_user(user)
        return True
    return False


# Função de logout
def logout():
    logout_user()


# Exemplo de rota protegida
@login_required
def protected_view():
    return "Você está autenticado e pode ver esta página protegida!"
