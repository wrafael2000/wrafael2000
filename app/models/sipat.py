from ..extensions import db


class SipatEdicao(db.Model):
    """Uma edição anual da Semana Interna de Prevenção de Acidentes (SIPAT)."""

    __tablename__ = "sipat_edicoes"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    tema = db.Column(db.String(150))
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)

    atividades = db.relationship(
        "AtividadeSipat",
        back_populates="sipat",
        cascade="all, delete-orphan",
        order_by="AtividadeSipat.data, AtividadeSipat.hora_inicio",
    )

    def __repr__(self):
        return f"<SipatEdicao {self.titulo}>"


class AtividadeSipat(db.Model):
    """Um item da programação de uma edição da SIPAT."""

    __tablename__ = "atividades_sipat"

    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(150), nullable=False)
    descricao = db.Column(db.Text)
    data = db.Column(db.Date, nullable=False)
    hora_inicio = db.Column(db.Time)
    responsavel = db.Column(db.String(120))
    local = db.Column(db.String(150))

    sipat_id = db.Column(db.Integer, db.ForeignKey("sipat_edicoes.id"), nullable=False)
    sipat = db.relationship("SipatEdicao", back_populates="atividades")

    def __repr__(self):
        return f"<AtividadeSipat {self.titulo}>"
