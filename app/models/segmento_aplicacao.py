from ..extensions import db

envio_segmentos = db.Table(
    "envio_segmentos",
    db.Column("envio_id", db.Integer, db.ForeignKey("envios.id"), primary_key=True),
    db.Column(
        "segmento_aplicacao_id",
        db.Integer,
        db.ForeignKey("segmentos_aplicacao.id"),
        primary_key=True,
    ),
)


class SegmentoAplicacao(db.Model):
    """Um setor/departamento configurado para participar de uma aplicação.

    Guarda um retrato (snapshot) da quantidade de colaboradores no momento
    da criação da aplicação, usado para calcular a taxa de resposta — não
    precisa acompanhar o número atual de funcionários cadastrados no setor.
    """

    __tablename__ = "segmentos_aplicacao"

    id = db.Column(db.Integer, primary_key=True)

    aplicacao_id = db.Column(db.Integer, db.ForeignKey("aplicacoes.id"), nullable=False)
    aplicacao = db.relationship("Aplicacao", back_populates="segmentos")

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor")

    quantidade_colaboradores = db.Column(db.Integer, nullable=False, default=0)

    def __repr__(self):
        return f"<SegmentoAplicacao setor={self.setor_id} aplicacao={self.aplicacao_id}>"
