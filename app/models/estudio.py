from app import db
from app.models.util import save, delete


class Estudio(db.Model):
    __tablename__ = "estudios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="estudios")
    agendamentos = db.relationship("Agendamento", back_populates="estudio")

    def __repr__(self):
        return f"<Estudio {self.id} - {self.nome}>"

    def __init__(self, nome, user_id, descricao=None):
        self.nome = nome
        self.descricao = descricao
        self.user_id = user_id

    @staticmethod
    def get_all_studios():
        """Retorna todos os estúdios."""
        return Estudio.query.all()

    @staticmethod
    def get_studio_by_name(nome):
        """Retorna um estúdio pelo nome."""
        return Estudio.query.filter_by(nome=nome).first()

    @staticmethod
    def get_studios_by_user_id(user_id):
        """Retorna todos os estúdios de um usuário pelo ID."""
        return Estudio.query.filter_by(user_id=user_id).order_by(Estudio.nome).all()

    @staticmethod
    def get_studio_by_id(estudio_id):
        """Retorna um estúdio pelo ID."""
        return Estudio.query.get(estudio_id)

    @staticmethod
    def get_studio_by_id_safe(user_id, estudio_id):
        """Retorna um estúdio pelo ID."""
        return Estudio.query.filter(
            Estudio.id == estudio_id, Estudio.user_id == user_id
        ).first()

    def delete(self):
        """Remove a instância do banco de dados."""
        for agendamento in self.agendamentos:
            agendamento.delete()
        delete(self)

    def save(self):
        save(self)
