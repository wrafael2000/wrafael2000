from ..extensions import db

STATUS_CONFORMIDADE = ["Conforme", "Não conforme", "Em andamento", "Não aplicável"]


class NormaRegulamentadora(db.Model):
    """Catálogo de Normas Regulamentadoras (NRs) de SST."""

    __tablename__ = "normas_regulamentadoras"

    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(10), unique=True, nullable=False)  # ex.: "NR-6"
    titulo = db.Column(db.String(200), nullable=False)
    aplicavel = db.Column(db.Boolean, default=True, nullable=False)
    link_oficial = db.Column(db.String(255))
    observacao = db.Column(db.Text)

    itens_conformidade = db.relationship(
        "ItemConformidadeNR", back_populates="norma", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<NormaRegulamentadora {self.numero}>"


class ItemConformidadeNR(db.Model):
    """Item de checklist de conformidade vinculado a uma NR."""

    __tablename__ = "itens_conformidade_nr"

    id = db.Column(db.Integer, primary_key=True)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), nullable=False, default="Em andamento")
    responsavel = db.Column(db.String(120))
    prazo = db.Column(db.Date)
    observacao = db.Column(db.Text)

    norma_id = db.Column(db.Integer, db.ForeignKey("normas_regulamentadoras.id"), nullable=False)
    norma = db.relationship("NormaRegulamentadora", back_populates="itens_conformidade")

    def __repr__(self):
        return f"<ItemConformidadeNR {self.id} - {self.norma_id}>"
