from app import db
from app.models.util import save, delete


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # duração em minutos
    estudio_id = db.Column(db.Integer, db.ForeignKey("estudios.id"), nullable=False)
    estudio = db.relationship("Estudio", back_populates="agendamentos")
    # relacionamento com a tabela Estudios
    descricao = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Agendamento {self.id} - {self.descricao} em {self.data_hora}>"

    def __init__(self, data_hora, duracao, estudio_id, descricao):
        self.data_hora = data_hora
        self.duracao = duracao
        self.estudio_id = estudio_id
        self.descricao = descricao

    @classmethod
    def get_agendamentos_by_date_range(cls, datainicial, datafinal):
        """Retorna agendamentos dentro de um intervalo de datas."""
        return (
            cls.query.filter(cls.data_hora >= datainicial, cls.data_hora <= datafinal)
            .order_by(cls.data_hora)
            .all()
        )

    @classmethod
    def get_agendamento_by_id(cls, agendamento_id):
        """Retorna um agendamento pelo ID."""
        return cls.query.get(agendamento_id)

    @classmethod
    def get_agendamentos_by_estudio(cls, estudio_id):
        """Retorna agendamentos de um estúdio específico."""
        return cls.query.filter_by(estudio_id=estudio_id).order_by(cls.data_hora).all()

    def delete(self):
        """Remove a instância do banco de dados."""
        delete(self)

    def save(self):
        save(self)
