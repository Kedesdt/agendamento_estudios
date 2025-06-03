from flask import request, redirect, url_for
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

current_user = current_user  # Variável global para armazenar o usuário atual


# Modelo de usuário (simplificado)
class User(UserMixin):
    def __init__(self, id, username, password):
        self.id = id
        self.username = username
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)


# Simulando um banco de dados de usuários
users = {
    "admin": User(1, "admin", os.environ.get("ADMIN_PASSWORD", "admin123")),
}


@login_manager.user_loader
def load_user(user_id):
    return next((user for user in users.values() if str(user.id) == user_id), None)


# Função de autenticação
def authenticate(username, password):
    user = users.get(username)
    if user and user.verify_password(password):
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
