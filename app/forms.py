from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed, FileField
from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    PasswordField,
    SelectField,
    SelectMultipleField,
    StringField,
    SubmitField,
    TextAreaField,
    TimeField,
)
from wtforms.validators import DataRequired, Email, EqualTo, Length, NumberRange, Optional

from .models.acidente import GRAVIDADES, TIPOS_ACIDENTE
from .models.cipa import CARGOS_CIPA, TIPOS_REPRESENTACAO
from .models.documento_sst import TIPOS_DOCUMENTO
from .models.exame import RESULTADOS, TIPOS_EXAME
from .models.norma_regulamentadora import STATUS_CONFORMIDADE
from .models.pgr import CATEGORIAS_RISCO, NIVEIS_RISCO, STATUS_ACAO_PGR
from .models.plano_acao_psicossocial import STATUS_PLANO_ACAO
from .models.questionario import TIPOS_QUESTIONARIO
from .models.reuniao_cipa import TIPOS_REUNIAO_CIPA


class LoginForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    senha = PasswordField("Senha", validators=[DataRequired()])
    submit = SubmitField("Entrar")


class SetorForm(FlaskForm):
    nome = StringField("Nome do setor", validators=[DataRequired(), Length(max=120)])
    descricao = StringField("Descrição", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Salvar")


class FuncionarioForm(FlaskForm):
    nome = StringField("Nome completo", validators=[DataRequired(), Length(max=120)])
    cargo = StringField("Cargo", validators=[Optional(), Length(max=120)])
    data_admissao = DateField("Data de admissão", validators=[Optional()])
    setor_id = SelectField("Setor", coerce=int, validators=[DataRequired()])
    ativo = BooleanField("Ativo", default=True)
    submit = SubmitField("Salvar")


class EpiForm(FlaskForm):
    nome = StringField("Nome do EPI", validators=[DataRequired(), Length(max=120)])
    ca = StringField("CA (Certificado de Aprovação)", validators=[Optional(), Length(max=30)])
    validade_dias = IntegerField(
        "Vida útil (dias)",
        validators=[Optional(), NumberRange(min=1)],
        description="Deixe em branco se o EPI não tiver validade definida.",
    )
    submit = SubmitField("Salvar")


class EntregaEpiForm(FlaskForm):
    funcionario_id = SelectField("Funcionário", coerce=int, validators=[DataRequired()])
    epi_id = SelectField("EPI", coerce=int, validators=[DataRequired()])
    data_entrega = DateField("Data da entrega", validators=[DataRequired()])
    quantidade = IntegerField(
        "Quantidade", default=1, validators=[DataRequired(), NumberRange(min=1)]
    )
    observacao = StringField("Observação", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Salvar")


class AcidenteForm(FlaskForm):
    funcionario_id = SelectField("Funcionário envolvido", coerce=int, validators=[DataRequired()])
    data = DateField("Data", validators=[DataRequired()])
    local = StringField("Local", validators=[DataRequired(), Length(max=150)])
    tipo = SelectField("Tipo", choices=[(t, t) for t in TIPOS_ACIDENTE], validators=[DataRequired()])
    gravidade = SelectField(
        "Gravidade", choices=[(g, g) for g in GRAVIDADES], validators=[DataRequired()]
    )
    descricao = TextAreaField("O que aconteceu", validators=[DataRequired()])
    causa = TextAreaField("Causa (opcional)", validators=[Optional()])
    medidas_tomadas = TextAreaField("Medidas tomadas (opcional)", validators=[Optional()])
    dias_afastamento = IntegerField(
        "Dias de afastamento", default=0, validators=[Optional(), NumberRange(min=0)]
    )
    submit = SubmitField("Salvar")


class ExameForm(FlaskForm):
    funcionario_id = SelectField("Funcionário", coerce=int, validators=[DataRequired()])
    tipo = SelectField("Tipo de exame", choices=[(t, t) for t in TIPOS_EXAME], validators=[DataRequired()])
    data_exame = DateField("Data do exame", validators=[DataRequired()])
    data_validade = DateField(
        "Validade",
        validators=[Optional()],
        description="Deixe em branco se o exame não tiver validade (ex.: demissional).",
    )
    resultado = SelectField("Resultado", choices=[(r, r) for r in RESULTADOS], validators=[DataRequired()])
    medico = StringField("Médico/clínica responsável", validators=[Optional(), Length(max=120)])
    observacao = TextAreaField("Observação", validators=[Optional()])
    submit = SubmitField("Salvar")


class DocumentoSSTForm(FlaskForm):
    tipo = SelectField("Tipo", choices=[(t, t) for t in TIPOS_DOCUMENTO], validators=[DataRequired()])
    nome = StringField("Nome do documento", validators=[DataRequired(), Length(max=150)])
    data_emissao = DateField("Data de emissão", validators=[DataRequired()])
    data_validade = DateField("Validade", validators=[Optional()])
    responsavel_tecnico = StringField(
        "Responsável técnico", validators=[Optional(), Length(max=120)]
    )
    observacao = TextAreaField("Observação", validators=[Optional()])
    arquivo = FileField(
        "Arquivo (PDF, opcional)",
        validators=[Optional(), FileAllowed(["pdf"], "Envie um arquivo PDF.")],
    )
    submit = SubmitField("Salvar")


class TreinamentoForm(FlaskForm):
    nome = StringField("Nome do treinamento", validators=[DataRequired(), Length(max=150)])
    carga_horaria = IntegerField(
        "Carga horária (horas)", validators=[Optional(), NumberRange(min=1)]
    )
    validade_dias = IntegerField(
        "Validade / reciclagem (dias)",
        validators=[Optional(), NumberRange(min=1)],
        description="Deixe em branco se o treinamento não exigir reciclagem periódica.",
    )
    submit = SubmitField("Salvar")


class RealizacaoTreinamentoForm(FlaskForm):
    funcionario_id = SelectField("Funcionário", coerce=int, validators=[DataRequired()])
    treinamento_id = SelectField("Treinamento", coerce=int, validators=[DataRequired()])
    data_realizacao = DateField("Data de realização", validators=[DataRequired()])
    instrutor = StringField("Instrutor", validators=[Optional(), Length(max=120)])
    observacao = StringField("Observação", validators=[Optional(), Length(max=255)])
    submit = SubmitField("Salvar")


class QuestionarioForm(FlaskForm):
    tipo = SelectField("Tipo", choices=[(t, t) for t in TIPOS_QUESTIONARIO], validators=[DataRequired()])
    nome = StringField("Nome", validators=[DataRequired(), Length(max=150)])
    descricao = TextAreaField("Descrição", validators=[Optional()])
    submit = SubmitField("Salvar")


class PerguntaForm(FlaskForm):
    texto = TextAreaField("Texto da pergunta", validators=[DataRequired()])
    dimensao = StringField("Dimensão/categoria", validators=[DataRequired(), Length(max=80)])
    ordem = IntegerField("Ordem", default=0, validators=[Optional(), NumberRange(min=0)])
    submit = SubmitField("Salvar")


class AplicacaoForm(FlaskForm):
    empresa_id = SelectField("Empresa", coerce=int, validators=[DataRequired()])
    questionario_id = SelectField("Questionário", coerce=int, validators=[DataRequired()])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    descricao = TextAreaField("Descrição", validators=[Optional()])
    data_inicio = DateField("Data de início", validators=[DataRequired()])
    data_fim = DateField(
        "Data de término",
        validators=[Optional()],
        description="Deixe em branco para não ter data limite automática.",
    )
    ativa = BooleanField(
        "Avaliação ativa",
        default=True,
        description="Permite que funcionários respondam.",
    )
    multisetorial = BooleanField(
        "Avaliação multisetorial",
        default=False,
        description="Permite que colaboradores que atuam em mais de um setor marquem todos os setores em que trabalham.",
    )
    submit = SubmitField("Salvar avaliação")


class SegmentoAplicacaoForm(FlaskForm):
    setor_id = SelectField("Setor/Departamento", coerce=int, validators=[DataRequired()])
    quantidade_colaboradores = IntegerField(
        "Quantidade de colaboradores", validators=[DataRequired(), NumberRange(min=1)]
    )
    submit = SubmitField("Adicionar")


class PlanoAcaoPsicossocialForm(FlaskForm):
    dimensao = StringField(
        "Dimensão relacionada (opcional)", validators=[Optional(), Length(max=80)]
    )
    descricao = TextAreaField("Ação", validators=[DataRequired()])
    responsavel = StringField("Responsável", validators=[Optional(), Length(max=120)])
    prazo = DateField("Prazo", validators=[Optional()])
    status = SelectField(
        "Status", choices=[(s, s) for s in STATUS_PLANO_ACAO], validators=[DataRequired()]
    )
    submit = SubmitField("Salvar")


class RespostaPublicaForm(FlaskForm):
    """Só carrega o token CSRF e o setor; as perguntas são renderizadas à parte."""

    setor_id = SelectField("Setor (opcional)", coerce=int, validators=[Optional()])
    submit = SubmitField("Enviar respostas")


class MandatoCipaForm(FlaskForm):
    data_inicio = DateField("Início do mandato", validators=[DataRequired()])
    data_fim = DateField("Fim do mandato", validators=[DataRequired()])
    submit = SubmitField("Salvar")


class MembroCipaForm(FlaskForm):
    funcionario_id = SelectField("Funcionário", coerce=int, validators=[DataRequired()])
    tipo_representacao = SelectField(
        "Representação", choices=[(t, t) for t in TIPOS_REPRESENTACAO], validators=[DataRequired()]
    )
    cargo = SelectField("Cargo", choices=[(c, c) for c in CARGOS_CIPA], validators=[DataRequired()])
    data_inicio = DateField("Início no cargo", validators=[Optional()])
    data_fim = DateField(
        "Fim no cargo",
        validators=[Optional()],
        description="Preencha apenas se o membro saiu antes do fim do mandato.",
    )
    submit = SubmitField("Salvar")


class ReuniaoCipaForm(FlaskForm):
    mandato_id = SelectField("Mandato", coerce=int, validators=[DataRequired()])
    data = DateField("Data da reunião", validators=[DataRequired()])
    tipo = SelectField(
        "Tipo", choices=[(t, t) for t in TIPOS_REUNIAO_CIPA], validators=[DataRequired()]
    )
    pauta = TextAreaField("Pauta", validators=[Optional()])
    ata = TextAreaField("Ata (deliberações)", validators=[DataRequired()])
    presentes = SelectMultipleField(
        "Membros presentes",
        coerce=int,
        validators=[Optional()],
        description="Segure Ctrl (ou Cmd no Mac) para selecionar mais de um.",
    )
    submit = SubmitField("Salvar")


class SipatEdicaoForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    tema = StringField("Tema (opcional)", validators=[Optional(), Length(max=150)])
    data_inicio = DateField("Data de início", validators=[DataRequired()])
    data_fim = DateField("Data de encerramento", validators=[DataRequired()])
    submit = SubmitField("Salvar")


class AtividadeSipatForm(FlaskForm):
    titulo = StringField("Título da atividade", validators=[DataRequired(), Length(max=150)])
    descricao = TextAreaField("Descrição", validators=[Optional()])
    data = DateField("Data", validators=[DataRequired()])
    hora_inicio = TimeField("Horário", validators=[Optional()])
    responsavel = StringField("Responsável", validators=[Optional(), Length(max=120)])
    local = StringField("Local", validators=[Optional(), Length(max=150)])
    submit = SubmitField("Salvar")


class NormaRegulamentadoraForm(FlaskForm):
    numero = StringField("Número (ex.: NR-6)", validators=[DataRequired(), Length(max=10)])
    titulo = StringField("Título", validators=[DataRequired(), Length(max=200)])
    aplicavel = BooleanField("Aplicável à empresa", default=True)
    link_oficial = StringField("Link para o texto oficial", validators=[Optional(), Length(max=255)])
    observacao = TextAreaField("Observação", validators=[Optional()])
    submit = SubmitField("Salvar")


class ItemConformidadeNRForm(FlaskForm):
    descricao = TextAreaField("Item de conformidade", validators=[DataRequired()])
    status = SelectField(
        "Status", choices=[(s, s) for s in STATUS_CONFORMIDADE], validators=[DataRequired()]
    )
    responsavel = StringField("Responsável", validators=[Optional(), Length(max=120)])
    prazo = DateField("Prazo", validators=[Optional()])
    observacao = TextAreaField("Observação", validators=[Optional()])
    submit = SubmitField("Salvar")


class EmpresaForm(FlaskForm):
    razao_social = StringField("Razão social", validators=[DataRequired(), Length(max=200)])
    nome_fantasia = StringField("Nome fantasia", validators=[Optional(), Length(max=200)])
    cnpj = StringField("CNPJ", validators=[Optional(), Length(max=20)])
    endereco = StringField("Endereço", validators=[Optional(), Length(max=255)])
    telefone = StringField("Telefone", validators=[Optional(), Length(max=30)])
    email = StringField("E-mail", validators=[Optional(), Email(), Length(max=120)])
    submit = SubmitField("Salvar")


class DDSForm(FlaskForm):
    data = DateField("Data", validators=[DataRequired()])
    setor_id = SelectField("Setor", coerce=int, validators=[DataRequired()])
    tema = StringField("Tema abordado", validators=[DataRequired(), Length(max=200)])
    responsavel = StringField("Responsável pelo diálogo", validators=[DataRequired(), Length(max=120)])
    conteudo = TextAreaField("Conteúdo / observações", validators=[Optional()])
    participantes = SelectMultipleField(
        "Participantes",
        coerce=int,
        validators=[Optional()],
        description="Segure Ctrl (ou Cmd no Mac) para selecionar mais de um.",
    )
    submit = SubmitField("Salvar")


class AprForm(FlaskForm):
    titulo = StringField("Atividade/tarefa analisada", validators=[DataRequired(), Length(max=200)])
    data = DateField("Data", validators=[DataRequired()])
    setor_id = SelectField("Setor", coerce=int, validators=[DataRequired()])
    local = StringField("Local", validators=[Optional(), Length(max=150)])
    responsavel = StringField("Responsável pela análise", validators=[DataRequired(), Length(max=120)])
    observacoes = TextAreaField("Observações", validators=[Optional()])
    submit = SubmitField("Salvar")


class EtapaAprForm(FlaskForm):
    descricao_etapa = TextAreaField("Etapa da atividade", validators=[DataRequired()])
    perigo_risco = TextAreaField("Perigo/risco identificado", validators=[DataRequired()])
    medida_controle = TextAreaField("Medida de controle", validators=[DataRequired()])
    submit = SubmitField("Adicionar etapa")


class PgrForm(FlaskForm):
    titulo = StringField("Título", validators=[DataRequired(), Length(max=150)])
    responsavel_tecnico = StringField(
        "Responsável técnico", validators=[DataRequired(), Length(max=120)]
    )
    responsavel_tecnico_registro = StringField(
        "Registro profissional (CREA, etc.)", validators=[Optional(), Length(max=60)]
    )
    data_elaboracao = DateField("Data de elaboração", validators=[DataRequired()])
    data_validade = DateField(
        "Validade / próxima revisão",
        validators=[Optional()],
        description="Recomendado revisar o PGR a cada 2 anos, ou antes disso se houver mudança relevante no processo de trabalho.",
    )
    introducao = TextAreaField("Introdução / metodologia (opcional)", validators=[Optional()])
    submit = SubmitField("Salvar")


class ItemRiscoPgrForm(FlaskForm):
    setor_id = SelectField("Setor", coerce=int, validators=[DataRequired()])
    funcao_atividade = StringField("Função/atividade (opcional)", validators=[Optional(), Length(max=150)])
    categoria_risco = SelectField(
        "Categoria de risco", choices=[(c, c) for c in CATEGORIAS_RISCO], validators=[DataRequired()]
    )
    perigo_fator_risco = TextAreaField(
        "Perigo/fator de risco identificado", validators=[DataRequired()]
    )
    fonte_geradora = TextAreaField("Fonte geradora (opcional)", validators=[Optional()])
    medidas_existentes = TextAreaField(
        "Medidas de controle existentes (opcional)", validators=[Optional()]
    )
    nivel_risco = SelectField(
        "Nível de risco", choices=[(n, n) for n in NIVEIS_RISCO], validators=[DataRequired()]
    )
    medidas_recomendadas = TextAreaField(
        "Medidas de controle recomendadas", validators=[DataRequired()]
    )
    prazo = DateField("Prazo (opcional)", validators=[Optional()])
    responsavel_acao = StringField("Responsável pela ação (opcional)", validators=[Optional(), Length(max=120)])
    status = SelectField(
        "Status", choices=[(s, s) for s in STATUS_ACAO_PGR], validators=[DataRequired()]
    )
    submit = SubmitField("Salvar item")


class EsqueciSenhaForm(FlaskForm):
    email = StringField("E-mail", validators=[DataRequired(), Email()])
    codigo_recuperacao = StringField("Código de recuperação", validators=[DataRequired()])
    nova_senha = PasswordField(
        "Nova senha", validators=[DataRequired(), Length(min=6, message="Use pelo menos 6 caracteres.")]
    )
    confirmar_senha = PasswordField(
        "Confirme a nova senha",
        validators=[DataRequired(), EqualTo("nova_senha", message="As senhas não coincidem.")],
    )
    submit = SubmitField("Redefinir senha")
