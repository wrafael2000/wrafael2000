from datetime import date

from ..extensions import db


class Apr(db.Model):
    """Análise Preliminar de Risco (APR) de uma atividade/tarefa."""

    __tablename__ = "aprs"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    data = db.Column(db.Date, nullable=False, default=date.today)
    local = db.Column(db.String(150))
    responsavel = db.Column(db.String(120), nullable=False)
    observacoes = db.Column(db.Text)

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor")

    etapas = db.relationship(
        "EtapaApr", back_populates="apr", cascade="all, delete-orphan", order_by="EtapaApr.ordem"
    )

    def __repr__(self):
        return f"<Apr {self.titulo}>"


class EtapaApr(db.Model):
    """Uma etapa da atividade analisada, com o perigo/risco e a medida de controle."""

    __tablename__ = "etapas_apr"

    id = db.Column(db.Integer, primary_key=True)
    ordem = db.Column(db.Integer, nullable=False, default=0)
    descricao_etapa = db.Column(db.Text, nullable=False)
    perigo_risco = db.Column(db.Text, nullable=False)
    medida_controle = db.Column(db.Text, nullable=False)

    apr_id = db.Column(db.Integer, db.ForeignKey("aprs.id"), nullable=False)
    apr = db.relationship("Apr", back_populates="etapas")

    def __repr__(self):
        return f"<EtapaApr {self.id} - apr {self.apr_id}>"
