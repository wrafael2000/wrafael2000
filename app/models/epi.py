from ..extensions import db


class Epi(db.Model):
    """Catálogo de tipos de Equipamento de Proteção Individual."""

    __tablename__ = "epis"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    ca = db.Column(db.String(30))  # Certificado de Aprovação
    validade_dias = db.Column(db.Integer)  # vida útil em dias; nulo = sem validade

    entregas = db.relationship(
        "EntregaEpi", back_populates="epi", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Epi {self.nome}>"
