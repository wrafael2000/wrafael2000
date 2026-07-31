from datetime import date

from ..extensions import db

CATEGORIAS_AGENTE = ["Físico", "Químico", "Biológico"]
EFICACIA_EPI_EPC = ["Sim", "Não", "Parcial"]
CONCLUSOES_LTCAT = [
    "Com direito a aposentadoria especial",
    "Sem direito a aposentadoria especial",
    "Não avaliado",
]


class Ltcat(db.Model):
    """Laudo Técnico das Condições do Ambiente de Trabalho (LTCAT)."""

    __tablename__ = "ltcats"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    responsavel_tecnico = db.Column(db.String(120), nullable=False)
    responsavel_tecnico_registro = db.Column(db.String(60))
    data_elaboracao = db.Column(db.Date, nullable=False, default=date.today)
    data_validade = db.Column(db.Date)
    metodologia = db.Column(db.Text)

    documento_id = db.Column(db.Integer, db.ForeignKey("documentos_sst.id"))
    documento = db.relationship("DocumentoSST")

    itens = db.relationship(
        "ItemLtcat", back_populates="ltcat", cascade="all, delete-orphan", order_by="ItemLtcat.id"
    )

    def __repr__(self):
        return f"<Ltcat {self.titulo}>"


class ItemLtcat(db.Model):
    """Um agente nocivo avaliado no LTCAT, por função/setor."""

    __tablename__ = "itens_ltcat"

    id = db.Column(db.Integer, primary_key=True)
    funcao = db.Column(db.String(150), nullable=False)
    agente_nocivo = db.Column(db.Text, nullable=False)
    tipo_agente = db.Column(db.String(20), nullable=False)
    intensidade_concentracao = db.Column(db.String(80))
    limite_tolerancia = db.Column(db.String(80))
    tecnica_utilizada = db.Column(db.String(150))
    epi_epc_eficaz = db.Column(db.String(10), nullable=False, default="Não")
    conclusao = db.Column(db.String(60), nullable=False, default="Não avaliado")
    observacoes = db.Column(db.Text)

    ltcat_id = db.Column(db.Integer, db.ForeignKey("ltcats.id"), nullable=False)
    ltcat = db.relationship("Ltcat", back_populates="itens")

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor")

    def __repr__(self):
        return f"<ItemLtcat {self.id} - ltcat {self.ltcat_id}>"
