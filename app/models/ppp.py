from datetime import date

from ..extensions import db


class Ppp(db.Model):
    """Perfil Profissiográfico Previdenciário (PPP) de um funcionário."""

    __tablename__ = "ppps"

    id = db.Column(db.Integer, primary_key=True)
    data_emissao = db.Column(db.Date, nullable=False, default=date.today)
    responsavel_emissao = db.Column(db.String(120), nullable=False)
    responsavel_tecnico_seguranca = db.Column(db.String(120))
    responsavel_tecnico_seguranca_registro = db.Column(db.String(60))
    medico_coordenador = db.Column(db.String(120))
    medico_coordenador_crm = db.Column(db.String(60))
    observacoes = db.Column(db.Text)

    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    funcionario = db.relationship("Funcionario")

    exposicoes = db.relationship(
        "PppExposicao", back_populates="ppp", cascade="all, delete-orphan", order_by="PppExposicao.data_inicio"
    )

    def __repr__(self):
        return f"<Ppp funcionario={self.funcionario_id}>"


class PppExposicao(db.Model):
    """Um período de exposição a agente nocivo no histórico do funcionário."""

    __tablename__ = "exposicoes_ppp"

    id = db.Column(db.Integer, primary_key=True)
    funcao = db.Column(db.String(150), nullable=False)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date)
    tipo_agente = db.Column(db.String(20), nullable=False)
    agente_nocivo = db.Column(db.Text, nullable=False)
    intensidade_concentracao = db.Column(db.String(80))
    epi_eficaz = db.Column(db.String(10), nullable=False, default="Não")
    observacoes = db.Column(db.Text)

    ppp_id = db.Column(db.Integer, db.ForeignKey("ppps.id"), nullable=False)
    ppp = db.relationship("Ppp", back_populates="exposicoes")

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor")

    def __repr__(self):
        return f"<PppExposicao {self.id} - ppp {self.ppp_id}>"
