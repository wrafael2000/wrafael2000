from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import EntregaEpiForm
from ..models import EntregaEpi, Epi, Funcionario

entregas_epi_bp = Blueprint("entregas_epi", __name__, url_prefix="/entregas-epi")


def _preencher_selects(form):
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome).all()
    ]
    form.epi_id.choices = [(e.id, e.nome) for e in Epi.query.order_by(Epi.nome).all()]


@entregas_epi_bp.route("/")
@login_required
def listar():
    entregas = EntregaEpi.query.order_by(EntregaEpi.data_entrega.desc()).all()
    return render_template("entregas_epi/listar.html", entregas=entregas)


@entregas_epi_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = EntregaEpiForm()
    _preencher_selects(form)
    if form.validate_on_submit():
        entrega = EntregaEpi(
            funcionario_id=form.funcionario_id.data,
            epi_id=form.epi_id.data,
            data_entrega=form.data_entrega.data,
            quantidade=form.quantidade.data,
            observacao=form.observacao.data,
        )
        entrega.epi = Epi.query.get(form.epi_id.data)
        entrega.calcular_validade()
        db.session.add(entrega)
        db.session.commit()
        flash("Entrega de EPI registrada com sucesso.", "success")
        return redirect(url_for("entregas_epi.listar"))
    return render_template("entregas_epi/form.html", form=form, titulo="Nova entrega de EPI")


@entregas_epi_bp.route("/<int:entrega_id>/editar", methods=["GET", "POST"])
@login_required
def editar(entrega_id):
    entrega = EntregaEpi.query.get_or_404(entrega_id)
    form = EntregaEpiForm(obj=entrega)
    _preencher_selects(form)
    if form.validate_on_submit():
        entrega.funcionario_id = form.funcionario_id.data
        entrega.epi_id = form.epi_id.data
        entrega.data_entrega = form.data_entrega.data
        entrega.quantidade = form.quantidade.data
        entrega.observacao = form.observacao.data
        entrega.epi = Epi.query.get(form.epi_id.data)
        entrega.calcular_validade()
        db.session.commit()
        flash("Entrega de EPI atualizada com sucesso.", "success")
        return redirect(url_for("entregas_epi.listar"))
    return render_template("entregas_epi/form.html", form=form, titulo="Editar entrega de EPI")


@entregas_epi_bp.route("/<int:entrega_id>/excluir", methods=["POST"])
@login_required
def excluir(entrega_id):
    entrega = EntregaEpi.query.get_or_404(entrega_id)
    db.session.delete(entrega)
    db.session.commit()
    flash("Entrega removida.", "info")
    return redirect(url_for("entregas_epi.listar"))
