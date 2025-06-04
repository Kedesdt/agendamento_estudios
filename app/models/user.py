from app import db
from app.models.util import save, delete
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(db.Model, UserMixin):
    __tablename__ = "users"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    agendamentos = db.relationship("Agendamento", back_populates="user")
    estudios = db.relationship("Estudio", back_populates="user")

    def __init__(self, username, email, name):
        self.name = name
        self.username = username
        self.email = email
        self.password = None

    def __repr__(self):
        return f"<User {self.username}>"
    
    def set_password(self, password):
        """Define a senha do usuário."""
        self.password = generate_password_hash(password)
    
    def check_password(self, password):
        """Verifica se a senha informada confere com o hash armazenado."""
        return check_password_hash(self.password, password)

    @classmethod
    def get_user_by_id(cls, user_id):
        """Retorna um usuário pelo ID."""
        return cls.query.get(user_id)

    @classmethod
    def get_user_by_username(cls, username):
        """Retorna um usuário pelo nome de usuário."""
        return cls.query.filter_by(username=username).first()
    
    def save(self):
        """Salva a instância no banco de dados."""
        save(self)
    def delete(self):
        """Remove a instância do banco de dados."""
        delete(self)