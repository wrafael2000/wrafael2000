from datetime import date

from ..extensions import db


class Pcmso(db.Model):
    """Programa de Controle Médico de Saúde Ocupacional (PCMSO), conforme a NR-07."""

    __tablename__ = "pcmsos"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    medico_coordenador = db.Column(db.String(120), nullable=False)
    medico_coordenador_crm = db.Column(db.String(60))
    data_elaboracao = db.Column(db.Date, nullable=False, default=date.today)
    data_validade = db.Column(db.Date)
    diretrizes = db.Column(db.Text)

    documento_id = db.Column(db.Integer, db.ForeignKey("documentos_sst.id"))
    documento = db.relationship("DocumentoSST")

    itens = db.relationship(
        "ItemPcmso", back_populates="pcmso", cascade="all, delete-orphan", order_by="ItemPcmso.id"
    )

    def __repr__(self):
        return f"<Pcmso {self.titulo}>"


class ItemPcmso(db.Model):
    """Um item do quadro de riscos/exames do PCMSO, por função ou setor."""

    __tablename__ = "itens_pcmso"

    id = db.Column(db.Integer, primary_key=True)
    funcao = db.Column(db.String(150), nullable=False)
    riscos_ocupacionais = db.Column(db.Text, nullable=False)
    exames_indicados = db.Column(db.Text, nullable=False)
    periodicidade_meses = db.Column(db.Integer, nullable=False, default=12)
    observacoes = db.Column(db.Text)

    pcmso_id = db.Column(db.Integer, db.ForeignKey("pcmsos.id"), nullable=False)
    pcmso = db.relationship("Pcmso", back_populates="itens")

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor")

    def __repr__(self):
        return f"<ItemPcmso {self.id} - pcmso {self.pcmso_id}>"
