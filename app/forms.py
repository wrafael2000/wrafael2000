from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
    TextAreaField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional

from .models.acidente import GRAVIDADES, TIPOS_ACIDENTE
from .models.documento_sst import TIPOS_DOCUMENTO
from .models.exame import RESULTADOS, TIPOS_EXAME


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
