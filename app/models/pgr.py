from datetime import date

from ..extensions import db

CATEGORIAS_RISCO = ["Físico", "Químico", "Biológico", "Ergonômico", "Acidente/Mecânico"]
NIVEIS_RISCO = ["Baixo", "Médio", "Alto", "Crítico"]
STATUS_ACAO_PGR = ["Pendente", "Em andamento", "Concluído"]


class Pgr(db.Model):
    """Programa de Gerenciamento de Riscos (PGR), conforme a NR-01."""

    __tablename__ = "pgrs"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    responsavel_tecnico = db.Column(db.String(120), nullable=False)
    responsavel_tecnico_registro = db.Column(db.String(60))
    data_elaboracao = db.Column(db.Date, nullable=False, default=date.today)
    data_validade = db.Column(db.Date)
    introducao = db.Column(db.Text)

    documento_id = db.Column(db.Integer, db.ForeignKey("documentos_sst.id"))
    documento = db.relationship("DocumentoSST")

    itens = db.relationship(
        "ItemRiscoPgr", back_populates="pgr", cascade="all, delete-orphan", order_by="ItemRiscoPgr.id"
    )

    def __repr__(self):
        return f"<Pgr {self.titulo}>"


class ItemRiscoPgr(db.Model):
    """Um item do inventário de riscos / plano de ação do PGR."""

    __tablename__ = "itens_risco_pgr"

    id = db.Column(db.Integer, primary_key=True)
    funcao_atividade = db.Column(db.String(150))
    categoria_risco = db.Column(db.String(30), nullable=False)
    perigo_fator_risco = db.Column(db.Text, nullable=False)
    fonte_geradora = db.Column(db.Text)
    medidas_existentes = db.Column(db.Text)
    nivel_risco = db.Column(db.String(20), nullable=False)
    medidas_recomendadas = db.Column(db.Text, nullable=False)
    prazo = db.Column(db.Date)
    responsavel_acao = db.Column(db.String(120))
    status = db.Column(db.String(20), nullable=False, default="Pendente")

    pgr_id = db.Column(db.Integer, db.ForeignKey("pgrs.id"), nullable=False)
    pgr = db.relationship("Pgr", back_populates="itens")

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor")

    def __repr__(self):
        return f"<ItemRiscoPgr {self.id} - pgr {self.pgr_id}>"
