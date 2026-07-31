from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import PerguntaForm, QuestionarioForm
from ..models import Pergunta, Questionario

questionarios_bp = Blueprint("questionarios", __name__, url_prefix="/questionarios")


@questionarios_bp.route("/")
@login_required
def listar():
    questionarios = Questionario.query.order_by(Questionario.nome).all()
    return render_template("questionarios/listar.html", questionarios=questionarios)


@questionarios_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = QuestionarioForm()
    if form.validate_on_submit():
        questionario = Questionario(
            tipo=form.tipo.data, nome=form.nome.data.strip(), descricao=form.descricao.data
        )
        db.session.add(questionario)
        db.session.commit()
        flash("Questionário criado com sucesso.", "success")
        return redirect(url_for("questionarios.ver", questionario_id=questionario.id))
    return render_template("questionarios/form.html", form=form, titulo="Novo questionário")


@questionarios_bp.route("/<int:questionario_id>")
@login_required
def ver(questionario_id):
    questionario = Questionario.query.get_or_404(questionario_id)
    return render_template("questionarios/ver.html", questionario=questionario)


@questionarios_bp.route("/<int:questionario_id>/editar", methods=["GET", "POST"])
@login_required
def editar(questionario_id):
    questionario = Questionario.query.get_or_404(questionario_id)
    form = QuestionarioForm(obj=questionario)
    if form.validate_on_submit():
        questionario.tipo = form.tipo.data
        questionario.nome = form.nome.data.strip()
        questionario.descricao = form.descricao.data
        db.session.commit()
        flash("Questionário atualizado com sucesso.", "success")
        return redirect(url_for("questionarios.ver", questionario_id=questionario.id))
    return render_template("questionarios/form.html", form=form, titulo="Editar questionário")


@questionarios_bp.route("/<int:questionario_id>/excluir", methods=["POST"])
@login_required
def excluir(questionario_id):
    questionario = Questionario.query.get_or_404(questionario_id)
    db.session.delete(questionario)
    db.session.commit()
    flash("Questionário removido.", "info")
    return redirect(url_for("questionarios.listar"))


@questionarios_bp.route("/<int:questionario_id>/perguntas/nova", methods=["GET", "POST"])
@login_required
def nova_pergunta(questionario_id):
    questionario = Questionario.query.get_or_404(questionario_id)
    form = PerguntaForm()
    if form.validate_on_submit():
        pergunta = Pergunta(
            texto=form.texto.data,
            dimensao=form.dimensao.data.strip(),
            ordem=form.ordem.data or 0,
            questionario_id=questionario.id,
        )
        db.session.add(pergunta)
        db.session.commit()
        flash("Pergunta adicionada com sucesso.", "success")
        return redirect(url_for("questionarios.ver", questionario_id=questionario.id))
    return render_template(
        "questionarios/pergunta_form.html", form=form, questionario=questionario, titulo="Nova pergunta"
    )


@questionarios_bp.route("/perguntas/<int:pergunta_id>/editar", methods=["GET", "POST"])
@login_required
def editar_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    form = PerguntaForm(obj=pergunta)
    if form.validate_on_submit():
        pergunta.texto = form.texto.data
        pergunta.dimensao = form.dimensao.data.strip()
        pergunta.ordem = form.ordem.data or 0
        db.session.commit()
        flash("Pergunta atualizada com sucesso.", "success")
        return redirect(url_for("questionarios.ver", questionario_id=pergunta.questionario_id))
    return render_template(
        "questionarios/pergunta_form.html",
        form=form,
        questionario=pergunta.questionario,
        titulo="Editar pergunta",
    )


@questionarios_bp.route("/perguntas/<int:pergunta_id>/excluir", methods=["POST"])
@login_required
def excluir_pergunta(pergunta_id):
    pergunta = Pergunta.query.get_or_404(pergunta_id)
    questionario_id = pergunta.questionario_id
    db.session.delete(pergunta)
    db.session.commit()
    flash("Pergunta removida.", "info")
    return redirect(url_for("questionarios.ver", questionario_id=questionario_id))
