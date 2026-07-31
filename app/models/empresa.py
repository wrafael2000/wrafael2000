from ..extensions import db


class Empresa(db.Model):
    """Dados cadastrais da empresa que usa o sistema (registro único)."""

    __tablename__ = "empresa"

    id = db.Column(db.Integer, primary_key=True)
    razao_social = db.Column(db.String(200), nullable=False)
    nome_fantasia = db.Column(db.String(200))
    cnpj = db.Column(db.String(20))
    endereco = db.Column(db.String(255))
    telefone = db.Column(db.String(30))
    email = db.Column(db.String(120))

    def __repr__(self):
        return f"<Empresa {self.razao_social}>"

    @staticmethod
    def obter_ou_none():
        return Empresa.query.first()
