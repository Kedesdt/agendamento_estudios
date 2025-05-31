from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager


# Inicializa extensões
db = SQLAlchemy()
#login_manager = LoginManager()

app = Flask(__name__)

# Configurações básicas
app.config['SECRET_KEY'] = 'sua_chave_secreta'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'

# Inicializa extensões com a aplicação
db.init_app(app)

from app.service.auth_service import login_manager
login_manager.init_app(app)

# Importa e registra Blueprints (módulos da aplicação)
from app.routes import routes
#from app.adm_routes import adm_routes
#from app.service import auth_service