from ..extensions import db

STATUS_PLANO_ACAO = ["Pendente", "Em andamento", "Concluído"]


class PlanoAcaoPsicossocial(db.Model):
    """Ação de melhoria vinculada aos resultados de uma aplicação de questionário."""

    __tablename__ = "planos_acao_psicossocial"

    id = db.Column(db.Integer, primary_key=True)
    dimensao = db.Column(db.String(80))  # opcional: a que dimensão a ação se refere
    descricao = db.Column(db.Text, nullable=False)
    responsavel = db.Column(db.String(120))
    prazo = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False, default="Pendente")

    aplicacao_id = db.Column(db.Integer, db.ForeignKey("aplicacoes.id"), nullable=False)
    aplicacao = db.relationship("Aplicacao", back_populates="planos_acao")

    def __repr__(self):
        return f"<PlanoAcaoPsicossocial {self.id}>"
