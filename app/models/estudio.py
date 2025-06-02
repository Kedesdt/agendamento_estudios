from app import db
from app.models.util import save, delete


class Estudio(db.Model):
    __tablename__ = "estudios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    agendamentos = db.relationship("Agendamento", back_populates="estudio")

    def __repr__(self):
        return f"<Estudio {self.id} - {self.nome}>"

    def __init__(self, nome, descricao=None):
        self.nome = nome
        self.descricao = descricao

    @staticmethod
    def get_all_studios():
        """Retorna todos os estúdios."""
        return Estudio.query.all()

    @staticmethod
    def get_studio_by_id(estudio_id):
        """Retorna um estúdio pelo ID."""
        return Estudio.query.get(estudio_id)

    def delete(self):
        """Remove a instância do banco de dados."""
        for agendamento in self.agendamentos:
            agendamento.delete()
        delete(self)

    def save(self):
        save(self)
