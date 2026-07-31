from flask_wtf import FlaskForm
from wtforms import (
    BooleanField,
    DateField,
    IntegerField,
    PasswordField,
    SelectField,
    StringField,
    SubmitField,
)
from wtforms.validators import DataRequired, Email, Length, NumberRange, Optional


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
