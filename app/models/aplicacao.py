import secrets
from datetime import date

from ..extensions import db


def _gerar_token():
    return secrets.token_urlsafe(16)


class Aplicacao(db.Model):
    """Uma rodada de aplicação de um questionário (ex.: 'Clima 2026 - 1º sem.')."""

    __tablename__ = "aplicacoes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    data_inicio = db.Column(db.Date, nullable=False, default=date.today)
    data_fim = db.Column(db.Date)
    ativa = db.Column(db.Boolean, default=True, nullable=False)
    multisetorial = db.Column(db.Boolean, default=False, nullable=False)
    token_publico = db.Column(db.String(40), unique=True, nullable=False, default=_gerar_token)

    questionario_id = db.Column(db.Integer, db.ForeignKey("questionarios.id"), nullable=False)
    questionario = db.relationship("Questionario", back_populates="aplicacoes")

    empresa_id = db.Column(db.Integer, db.ForeignKey("empresa.id"), nullable=True)
    empresa = db.relationship("Empresa")

    envios = db.relationship("Envio", back_populates="aplicacao", cascade="all, delete-orphan")
    planos_acao = db.relationship(
        "PlanoAcaoPsicossocial", back_populates="aplicacao", cascade="all, delete-orphan"
    )
    segmentos = db.relationship(
        "SegmentoAplicacao", back_populates="aplicacao", cascade="all, delete-orphan"
    )

    @property
    def disponivel(self):
        if not self.ativa:
            return False
        if self.data_fim and date.today() > self.data_fim:
            return False
        return True

    def __repr__(self):
        return f"<Aplicacao {self.titulo}>"


class Envio(db.Model):
    """Uma submissão anônima de respostas a uma aplicação."""

    __tablename__ = "envios"

    id = db.Column(db.Integer, primary_key=True)
    criado_em = db.Column(db.DateTime, default=db.func.now())

    aplicacao_id = db.Column(db.Integer, db.ForeignKey("aplicacoes.id"), nullable=False)
    aplicacao = db.relationship("Aplicacao", back_populates="envios")

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=True)
    setor = db.relationship("Setor")

    segmentos = db.relationship(
        "SegmentoAplicacao", secondary="envio_segmentos", backref="envios"
    )

    respostas = db.relationship("Resposta", back_populates="envio", cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Envio {self.id} - aplicacao {self.aplicacao_id}>"


class Resposta(db.Model):
    """O valor dado por um envio anônimo a uma pergunta específica."""

    __tablename__ = "respostas"

    id = db.Column(db.Integer, primary_key=True)
    valor = db.Column(db.Integer, nullable=False)

    envio_id = db.Column(db.Integer, db.ForeignKey("envios.id"), nullable=False)
    envio = db.relationship("Envio", back_populates="respostas")

    pergunta_id = db.Column(db.Integer, db.ForeignKey("perguntas.id"), nullable=False)
    pergunta = db.relationship("Pergunta", back_populates="respostas")

    def __repr__(self):
        return f"<Resposta {self.pergunta_id}={self.valor}>"
