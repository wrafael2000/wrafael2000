from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ExameForm
from ..models import Exame, Funcionario

exames_bp = Blueprint("exames", __name__, url_prefix="/exames")


def _preencher_funcionarios(form):
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.order_by(Funcionario.nome).all()
    ]


@exames_bp.route("/")
@login_required
def listar():
    exames = Exame.query.order_by(Exame.data_exame.desc()).all()
    return render_template("exames/listar.html", exames=exames)


@exames_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = ExameForm()
    _preencher_funcionarios(form)
    if form.validate_on_submit():
        exame = Exame(
            funcionario_id=form.funcionario_id.data,
            tipo=form.tipo.data,
            data_exame=form.data_exame.data,
            data_validade=form.data_validade.data,
            resultado=form.resultado.data,
            medico=form.medico.data,
            observacao=form.observacao.data,
        )
        db.session.add(exame)
        db.session.commit()
        flash("Exame registrado com sucesso.", "success")
        return redirect(url_for("exames.listar"))
    return render_template("exames/form.html", form=form, titulo="Novo exame (ASO)")


@exames_bp.route("/<int:exame_id>/editar", methods=["GET", "POST"])
@login_required
def editar(exame_id):
    exame = Exame.query.get_or_404(exame_id)
    form = ExameForm(obj=exame)
    _preencher_funcionarios(form)
    if form.validate_on_submit():
        exame.funcionario_id = form.funcionario_id.data
        exame.tipo = form.tipo.data
        exame.data_exame = form.data_exame.data
        exame.data_validade = form.data_validade.data
        exame.resultado = form.resultado.data
        exame.medico = form.medico.data
        exame.observacao = form.observacao.data
        db.session.commit()
        flash("Exame atualizado com sucesso.", "success")
        return redirect(url_for("exames.listar"))
    return render_template("exames/form.html", form=form, titulo="Editar exame (ASO)")


@exames_bp.route("/<int:exame_id>/excluir", methods=["POST"])
@login_required
def excluir(exame_id):
    exame = Exame.query.get_or_404(exame_id)
    db.session.delete(exame)
    db.session.commit()
    flash("Exame removido.", "info")
    return redirect(url_for("exames.listar"))
