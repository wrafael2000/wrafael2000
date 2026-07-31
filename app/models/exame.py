from datetime import date, timedelta

from ..extensions import db

TIPOS_EXAME = [
    "Admissional",
    "Periódico",
    "Retorno ao Trabalho",
    "Mudança de Função",
    "Demissional",
]

RESULTADOS = ["Apto", "Inapto"]


class Exame(db.Model):
    """Atestado de Saúde Ocupacional (ASO) de um funcionário."""

    __tablename__ = "exames"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(30), nullable=False)
    data_exame = db.Column(db.Date, nullable=False)
    data_validade = db.Column(db.Date)
    resultado = db.Column(db.String(10), nullable=False)
    medico = db.Column(db.String(120))
    observacao = db.Column(db.Text)

    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    funcionario = db.relationship("Funcionario")

    DIAS_ALERTA_VENCIMENTO = 30

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
        return f"<Exame {self.tipo} - {self.funcionario_id}>"
