from datetime import date

from ..extensions import db


class Funcionario(db.Model):
    __tablename__ = "funcionarios"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), nullable=False)
    cargo = db.Column(db.String(120))
    data_admissao = db.Column(db.Date, default=date.today)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor", back_populates="funcionarios")

    def __repr__(self):
        return f"<Funcionario {self.nome}>"
