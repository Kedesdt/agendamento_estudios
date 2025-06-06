from app import db
from app.models.util import save, delete
from sqlalchemy import or_, and_


class Agendamento(db.Model):
    __tablename__ = "agendamentos"

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", back_populates="agendamentos")
    data_hora_inicio = db.Column(db.DateTime, nullable=False)
    data_hora_final = db.Column(db.DateTime, nullable=False)
    estudio_id = db.Column(db.Integer, db.ForeignKey("estudios.id"), nullable=False)
    estudio = db.relationship("Estudio", back_populates="agendamentos")
    responsavel = db.Column(
        db.String(100), nullable=False
    )  # responsável pelo agendamento
    # relacionamento com a tabela Estudios
    descricao = db.Column(db.String(255), nullable=False)

    def __repr__(self):
        return f"<Agendamento {self.id} - {self.descricao} em {self.data_hora_inicio}>"

    def __init__(
        self,
        data_hora_inicio,
        data_hora_final,
        estudio_id,
        user_id,
        descricao,
        responsavel="Desconhecido",
    ):
        self.user_id = user_id
        self.responsavel = responsavel
        self.data_hora_inicio = data_hora_inicio
        self.data_hora_final = data_hora_final
        self.estudio_id = estudio_id
        self.descricao = descricao

    @classmethod
    def get_agendamentos_by_date_range(cls, user_id, datainicial, datafinal):
        """Retorna agendamentos dentro de um intervalo de datas."""
        return (
            cls.query.filter(
                cls.user_id == user_id,
                cls.data_hora_inicio >= datainicial,
                cls.data_hora_inicio <= datafinal,
            )
            .order_by(cls.data_hora_inicio)
            .all()
        )

    @classmethod
    def get_agendamentos_by_date_range_and_estudio(
        cls, user_id, estudio_id, datainicial, datafinal
    ):
        """Retorna agendamentos dentro de um intervalo de datas."""
        return (
            cls.query.filter(
                cls.user_id == user_id,
                cls.estudio_id == estudio_id,
                cls.data_hora_inicio >= datainicial,
                cls.data_hora_inicio <= datafinal,
            )
            .order_by(cls.data_hora_inicio)
            .all()
        )

    @classmethod
    def get_agendamentos_by_estudio_data_e_hora(
        cls, user_id, estudio_id, data_hora_inicio, data_hora_final
    ):
        """Retorna agendamentos que realmente entram em conflito com a nova marcação."""

        return (
            cls.query.filter(
                cls.estudio_id == estudio_id,
                or_(
                    and_(
                        cls.data_hora_inicio < data_hora_final,
                        cls.data_hora_inicio > data_hora_inicio,
                    ),
                    and_(
                        cls.data_hora_final < data_hora_final,
                        cls.data_hora_final > data_hora_inicio,
                    ),
                    and_(
                        cls.data_hora_inicio <= data_hora_inicio,
                        cls.data_hora_final >= data_hora_final,
                    ),
                ),
            )
            .order_by(cls.data_hora_inicio)
            .all()
        )

    @classmethod
    def get_agendamento_by_id(cls, agendamento_id):
        """Retorna um agendamento pelo ID."""
        return cls.query.get(agendamento_id)

    @classmethod
    def get_agendamentos_by_estudio(cls, estudio_id):
        """Retorna agendamentos de um estúdio específico."""
        return (
            cls.query.filter_by(estudio_id=estudio_id)
            .order_by(cls.data_hora_inicio)
            .all()
        )

    @classmethod
    def get_agendamentos_by_user(cls, user_id):
        """Retorna agendamentos de um usuário específico."""
        return cls.query.filter_by(user_id=user_id).order_by(cls.data_hora_inicio).all()

    def delete(self):
        """Remove a instância do banco de dados."""
        delete(self)

    def save(self):
        agendamentos = self.get_agendamentos_by_estudio_data_e_hora(
            self.user_id, self.estudio_id, self.data_hora_inicio, self.data_hora_final
        )
        print(agendamentos)
        if agendamentos:
            raise ValueError("Já existe um agendamento nesse horário.")
        save(self)
