from ..extensions import db

TIPOS_REPRESENTACAO = ["Empregador", "Empregado"]
CARGOS_CIPA = ["Presidente", "Vice-presidente", "Titular", "Suplente"]


class MandatoCipa(db.Model):
    """Uma gestão/mandato da CIPA (geralmente 1 ano, conforme NR-5)."""

    __tablename__ = "mandatos_cipa"

    id = db.Column(db.Integer, primary_key=True)
    data_inicio = db.Column(db.Date, nullable=False)
    data_fim = db.Column(db.Date, nullable=False)
    ativo = db.Column(db.Boolean, default=True, nullable=False)

    membros = db.relationship(
        "MembroCipa", back_populates="mandato", cascade="all, delete-orphan"
    )
    reunioes = db.relationship(
        "ReuniaoCipa", back_populates="mandato", cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<MandatoCipa {self.data_inicio}-{self.data_fim}>"


class MembroCipa(db.Model):
    """Um membro da CIPA em um mandato específico."""

    __tablename__ = "membros_cipa"

    id = db.Column(db.Integer, primary_key=True)
    tipo_representacao = db.Column(db.String(20), nullable=False)
    cargo = db.Column(db.String(20), nullable=False)
    data_inicio = db.Column(db.Date)
    data_fim = db.Column(db.Date)  # preenchido se o membro saiu antes do fim do mandato

    mandato_id = db.Column(db.Integer, db.ForeignKey("mandatos_cipa.id"), nullable=False)
    mandato = db.relationship("MandatoCipa", back_populates="membros")

    funcionario_id = db.Column(db.Integer, db.ForeignKey("funcionarios.id"), nullable=False)
    funcionario = db.relationship("Funcionario")

    def __repr__(self):
        return f"<MembroCipa {self.funcionario_id} - {self.cargo}>"
