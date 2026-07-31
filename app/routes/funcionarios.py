from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import FuncionarioForm
from ..models import Funcionario, Setor

funcionarios_bp = Blueprint("funcionarios", __name__, url_prefix="/funcionarios")


def _preencher_setores(form):
    form.setor_id.choices = [(s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()]


@funcionarios_bp.route("/")
@login_required
def listar():
    funcionarios = Funcionario.query.order_by(Funcionario.nome).all()
    return render_template("funcionarios/listar.html", funcionarios=funcionarios)


@funcionarios_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = FuncionarioForm()
    _preencher_setores(form)
    if form.validate_on_submit():
        funcionario = Funcionario(
            nome=form.nome.data.strip(),
            cargo=form.cargo.data,
            data_admissao=form.data_admissao.data,
            setor_id=form.setor_id.data,
            ativo=form.ativo.data,
        )
        db.session.add(funcionario)
        db.session.commit()
        flash("Funcionário cadastrado com sucesso.", "success")
        return redirect(url_for("funcionarios.listar"))
    return render_template("funcionarios/form.html", form=form, titulo="Novo funcionário")


@funcionarios_bp.route("/<int:funcionario_id>/editar", methods=["GET", "POST"])
@login_required
def editar(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    form = FuncionarioForm(obj=funcionario)
    _preencher_setores(form)
    if form.validate_on_submit():
        funcionario.nome = form.nome.data.strip()
        funcionario.cargo = form.cargo.data
        funcionario.data_admissao = form.data_admissao.data
        funcionario.setor_id = form.setor_id.data
        funcionario.ativo = form.ativo.data
        db.session.commit()
        flash("Funcionário atualizado com sucesso.", "success")
        return redirect(url_for("funcionarios.listar"))
    return render_template("funcionarios/form.html", form=form, titulo="Editar funcionário")


@funcionarios_bp.route("/<int:funcionario_id>/excluir", methods=["POST"])
@login_required
def excluir(funcionario_id):
    funcionario = Funcionario.query.get_or_404(funcionario_id)
    db.session.delete(funcionario)
    db.session.commit()
    flash("Funcionário removido.", "info")
    return redirect(url_for("funcionarios.listar"))
