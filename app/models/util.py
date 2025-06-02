from app import db


def save(instance):
    """Salva uma instância no banco de dados."""
    db.session.add(instance)
    db.session.commit()


def delete(instance):
    """Remove uma instância do banco de dados."""
    db.session.delete(instance)
    db.session.commit()
