from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Inicializa extensões
db = SQLAlchemy()
# login_manager = LoginManager()

app = Flask(__name__)

# Configurações básicas
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY", "sua_chave_secreta_padrao")
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI", "sqlite:///app.db")

from app.models.user import User
from app.models.agendamento import Agendamento
from app.models.estudio import Estudio

# Inicializa extensões com a aplicação
db.init_app(app)

from app.service.auth_service import login_manager

login_manager.init_app(app)

# Importa e registra Blueprints (módulos da aplicação)
from app.routes import routes
from app.adm_routes import adm_routes
from app.routes import user_routes
from app.routes import estudios_routes


with app.app_context():
    db.create_all()
