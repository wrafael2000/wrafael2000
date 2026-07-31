from ..extensions import db

TIPOS_QUESTIONARIO = ["HSE-IT", "COPSOQ II", "CBI (Burnout)", "Clima Organizacional", "Outro"]


class Questionario(db.Model):
    """Modelo de um questionário (catálogo de perguntas + dimensões)."""

    __tablename__ = "questionarios"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    escala_min = db.Column(db.Integer, nullable=False, default=1)
    escala_max = db.Column(db.Integer, nullable=False, default=5)
    escala_legenda = db.Column(
        db.String(255), default="1 = Nunca · 2 = Raramente · 3 = Às vezes · 4 = Frequentemente · 5 = Sempre"
    )

    perguntas = db.relationship(
        "Pergunta",
        back_populates="questionario",
        cascade="all, delete-orphan",
        order_by="Pergunta.ordem",
    )
    aplicacoes = db.relationship(
        "Aplicacao", back_populates="questionario", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Questionario {self.nome}>"


class Pergunta(db.Model):
    """Um item/pergunta de um questionário, agrupado por dimensão."""

    __tablename__ = "perguntas"

    id = db.Column(db.Integer, primary_key=True)
    texto = db.Column(db.Text, nullable=False)
    dimensao = db.Column(db.String(80), nullable=False)
    ordem = db.Column(db.Integer, nullable=False, default=0)

    questionario_id = db.Column(db.Integer, db.ForeignKey("questionarios.id"), nullable=False)
    questionario = db.relationship("Questionario", back_populates="perguntas")

    respostas = db.relationship("Resposta", back_populates="pergunta", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Pergunta {self.id} - {self.dimensao}>"
