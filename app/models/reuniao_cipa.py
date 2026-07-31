from ..extensions import db

TIPOS_REUNIAO_CIPA = ["Ordinária", "Extraordinária"]

presencas_reuniao_cipa = db.Table(
    "presencas_reuniao_cipa",
    db.Column("reuniao_id", db.Integer, db.ForeignKey("reunioes_cipa.id"), primary_key=True),
    db.Column("membro_id", db.Integer, db.ForeignKey("membros_cipa.id"), primary_key=True),
)


class ReuniaoCipa(db.Model):
    """Ata de uma reunião da CIPA."""

    __tablename__ = "reunioes_cipa"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False)
    tipo = db.Column(db.String(20), nullable=False)
    pauta = db.Column(db.Text)
    ata = db.Column(db.Text, nullable=False)

    mandato_id = db.Column(db.Integer, db.ForeignKey("mandatos_cipa.id"), nullable=False)
    mandato = db.relationship("MandatoCipa", back_populates="reunioes")

    presentes = db.relationship("MembroCipa", secondary=presencas_reuniao_cipa)

    def __repr__(self):
        return f"<ReuniaoCipa {self.data}>"
