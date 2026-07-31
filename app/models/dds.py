from datetime import date

from ..extensions import db

dds_participantes = db.Table(
    "dds_participantes",
    db.Column("dds_id", db.Integer, db.ForeignKey("dialogos_seguranca.id"), primary_key=True),
    db.Column("funcionario_id", db.Integer, db.ForeignKey("funcionarios.id"), primary_key=True),
)


class DDS(db.Model):
    """Registro de um Diálogo Diário de Segurança (DDS)."""

    __tablename__ = "dialogos_seguranca"

    id = db.Column(db.Integer, primary_key=True)
    data = db.Column(db.Date, nullable=False, default=date.today)
    tema = db.Column(db.String(200), nullable=False)
    responsavel = db.Column(db.String(120), nullable=False)
    conteudo = db.Column(db.Text)

    setor_id = db.Column(db.Integer, db.ForeignKey("setores.id"), nullable=False)
    setor = db.relationship("Setor")

    participantes = db.relationship("Funcionario", secondary=dds_participantes)

    def __repr__(self):
        return f"<DDS {self.data} - {self.tema}>"
