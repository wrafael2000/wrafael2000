from datetime import date, timedelta

from ..extensions import db

TIPOS_DOCUMENTO = ["PCMSO", "PGR", "Outro"]


class DocumentoSST(db.Model):
    """Documento obrigatório de SST da empresa (PCMSO, PGR, etc.)."""

    __tablename__ = "documentos_sst"

    id = db.Column(db.Integer, primary_key=True)
    tipo = db.Column(db.String(20), nullable=False)
    nome = db.Column(db.String(150), nullable=False)
    data_emissao = db.Column(db.Date, nullable=False)
    data_validade = db.Column(db.Date)
    responsavel_tecnico = db.Column(db.String(120))
    observacao = db.Column(db.Text)

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
        return f"<DocumentoSST {self.tipo} - {self.nome}>"
