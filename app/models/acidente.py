from ..extensions import db

TIPOS_ACIDENTE = [
    "Acidente com afastamento",
    "Acidente sem afastamento",
    "Incidente/quase-acidente",
]

GRAVIDADES = ["Leve", "Moderada", "Grave", "Fatal"]


class Acidente(db.Model):
    """Registro de acidente, incidente ou quase-acidente de trabalho."""

    __tablename__ = "acidentes"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    local = db.Column(db.String(150), nullable=False)
    tipo = db.Column(db.String(40), nullable=False)
    gravidade = db.Column(db.String(20), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    causa = db.Column(db.Text)
    medidas_tomadas = db.Column(db.Text)
    dias_afastamento = db.Column(db.Integer, default=0)

    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    funcionario = db.relationship("Funcionario")

    def __repr__(self):
        return f"<Acidente {self.id} - {self.funcionario_id}>"
