from datetime import date, timedelta

from ..extensions import db


class RealizacaoTreinamento(db.Model):
    """Registro de que um funcionário realizou um treinamento."""

    __tablename__ = "realizacoes_treinamento"

    id = db.Column(db.Integer, primary_key=True)
    data_realizacao = db.Column(db.Date, nullable=False, default=date.today)
    data_validade = db.Column(db.Date)  # calculada a partir do Treinamento.validade_dias
    instrutor = db.Column(db.String(120))
    observacao = db.Column(db.String(255))

    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    funcionario = db.relationship("Funcionario")

    treinamento_id = db.Column(db.Integer, db.ForeignKey("treinamentos.id"), nullable=False)
    treinamento = db.relationship("Treinamento", back_populates="realizacoes")

    DIAS_ALERTA_VENCIMENTO = 30

    def calcular_validade(self):
        if self.treinamento and self.treinamento.validade_dias and self.data_realizacao:
            self.data_validade = self.data_realizacao + timedelta(
                days=self.treinamento.validade_dias
            )
        else:
            self.data_validade = None

    @property
    def status(self):
        if not self.data_validade:
            return "sem_validade"
        hoje = date.today()
        if self.data_validade < hoje:
            return "vencido"
        if self.data_validade <= hoje + timedelta(days=self.DIAS_ALERTA_VENCIMENTO):
            return "vencendo"
        return "valido"

    def __repr__(self):
        return f"<RealizacaoTreinamento {self.treinamento_id} -> {self.funcionario_id}>"
