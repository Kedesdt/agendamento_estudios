from app import db

class Estudio(db.Model):
    __tablename__ = 'estudios'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.String(255), nullable=True)
    
    def __repr__(self):
        return f'<Estudio {self.nome}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao
        }
    def save(self):
        db.session.add(self)
        db.session.commit()

class Agendamento(db.Model):
    __tablename__ = 'agendamentos'
    
    id = db.Column(db.Integer, primary_key=True)
    estudio_id = db.Column(db.Integer, db.ForeignKey('estudios.id'), nullable=False)
    data_hora = db.Column(db.DateTime, nullable=False)
    duracao = db.Column(db.Integer, nullable=False)  # duração em minutos
    cliente_nome = db.Column(db.String(100), nullable=False)
    
    estudio = db.relationship('Estudio', backref=db.backref('agendamentos', lazy=True))
    
    def __repr__(self):
        return f'<Agendamento {self.id} - {self.data_hora}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'estudio_id': self.estudio_id,
            'data_hora': self.data_hora.isoformat(),
            'cliente_nome': self.cliente_nome
        }
    
    def save(self):
        db.session.add(self)
        db.session.commit()