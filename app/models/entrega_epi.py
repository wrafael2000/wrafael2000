from datetime import date, timedelta

from ..extensions import db


class EntregaEpi(db.Model):
    """Registro de entrega de um EPI a um funcionário."""

    __tablename__ = "entregas_epi"

    id = db.Column(db.Integer, primary_key=True)
    data_entrega = db.Column(db.Date, nullable=False, default=date.today)
    data_validade = db.Column(db.Date)  # calculada a partir do EPI.validade_dias
    quantidade = db.Column(db.Integer, nullable=False, default=1)
    observacao = db.Column(db.String(255))

    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    funcionario = db.relationship("Funcionario")

    epi_id = db.Column(db.Integer, db.ForeignKey("epis.id"), nullable=False)
    epi = db.relationship("Epi", back_populates="entregas")

    DIAS_ALERTA_VENCIMENTO = 30

    def calcular_validade(self):
        if self.epi and self.epi.validade_dias and self.data_entrega:
            self.data_validade = self.data_entrega + timedelta(days=self.epi.validade_dias)
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
        return f"<EntregaEpi {self.epi_id} -> {self.funcionario_id}>"
