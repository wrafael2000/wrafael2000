from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import TreinamentoForm
from ..models import Treinamento

treinamentos_bp = Blueprint("treinamentos", __name__, url_prefix="/treinamentos")


@treinamentos_bp.route("/")
@login_required
def listar():
    treinamentos = Treinamento.query.order_by(Treinamento.nome).all()
    return render_template("treinamentos/listar.html", treinamentos=treinamentos)


@treinamentos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = TreinamentoForm()
    if form.validate_on_submit():
        treinamento = Treinamento(
            nome=form.nome.data.strip(),
            carga_horaria=form.carga_horaria.data,
            validade_dias=form.validade_dias.data,
        )
        db.session.add(treinamento)
        db.session.commit()
        flash("Treinamento cadastrado com sucesso.", "success")
        return redirect(url_for("treinamentos.listar"))
    return render_template("treinamentos/form.html", form=form, titulo="Novo treinamento")


@treinamentos_bp.route("/<int:treinamento_id>/editar", methods=["GET", "POST"])
@login_required
def editar(treinamento_id):
    treinamento = Treinamento.query.get_or_404(treinamento_id)
    form = TreinamentoForm(obj=treinamento)
    if form.validate_on_submit():
        treinamento.nome = form.nome.data.strip()
        treinamento.carga_horaria = form.carga_horaria.data
        treinamento.validade_dias = form.validade_dias.data
        db.session.commit()
        flash("Treinamento atualizado com sucesso.", "success")
        return redirect(url_for("treinamentos.listar"))
    return render_template("treinamentos/form.html", form=form, titulo="Editar treinamento")


@treinamentos_bp.route("/<int:treinamento_id>/excluir", methods=["POST"])
@login_required
def excluir(treinamento_id):
    treinamento = Treinamento.query.get_or_404(treinamento_id)
    db.session.delete(treinamento)
    db.session.commit()
    flash("Treinamento removido.", "info")
    return redirect(url_for("treinamentos.listar"))
