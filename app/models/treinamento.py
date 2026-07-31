from ..extensions import db


class Treinamento(db.Model):
    """Catálogo de treinamentos/certificações (ex.: NRs)."""

    __tablename__ = "treinamentos"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(150), nullable=False)
    carga_horaria = db.Column(db.Integer)  # em horas
    validade_dias = db.Column(db.Integer)  # nulo = sem validade (sem reciclagem)

    realizacoes = db.relationship(
        "RealizacaoTreinamento", back_populates="treinamento", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Treinamento {self.nome}>"
