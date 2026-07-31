from ..extensions import db


class Setor(db.Model):
    __tablename__ = "setores"

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(120), unique=True, nullable=False)
    descricao = db.Column(db.String(255))

    funcionarios = db.relationship(
        "Funcionario", back_populates="setor", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Setor {self.nome}>"
