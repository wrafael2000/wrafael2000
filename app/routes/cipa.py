from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import MandatoCipaForm, MembroCipaForm
from ..models import Funcionario, MandatoCipa, MembroCipa

cipa_bp = Blueprint("cipa", __name__, url_prefix="/cipa")


@cipa_bp.route("/mandatos")
@login_required
def listar_mandatos():
    mandatos = MandatoCipa.query.order_by(MandatoCipa.data_inicio.desc()).all()
    return render_template("cipa/mandatos_listar.html", mandatos=mandatos)


@cipa_bp.route("/mandatos/novo", methods=["GET", "POST"])
@login_required
def novo_mandato():
    form = MandatoCipaForm()
    if form.validate_on_submit():
        mandato = MandatoCipa(data_inicio=form.data_inicio.data, data_fim=form.data_fim.data)
        db.session.add(mandato)
        db.session.commit()
        flash("Mandato da CIPA criado com sucesso.", "success")
        return redirect(url_for("cipa.ver_mandato", mandato_id=mandato.id))
    return render_template("cipa/mandato_form.html", form=form, titulo="Novo mandato da CIPA")


@cipa_bp.route("/mandatos/<int:mandato_id>")
@login_required
def ver_mandato(mandato_id):
    mandato = MandatoCipa.query.get_or_404(mandato_id)
    return render_template("cipa/mandato_ver.html", mandato=mandato)


@cipa_bp.route("/mandatos/<int:mandato_id>/editar", methods=["GET", "POST"])
@login_required
def editar_mandato(mandato_id):
    mandato = MandatoCipa.query.get_or_404(mandato_id)
    form = MandatoCipaForm(obj=mandato)
    if form.validate_on_submit():
        mandato.data_inicio = form.data_inicio.data
        mandato.data_fim = form.data_fim.data
        db.session.commit()
        flash("Mandato atualizado com sucesso.", "success")
        return redirect(url_for("cipa.ver_mandato", mandato_id=mandato.id))
    return render_template("cipa/mandato_form.html", form=form, titulo="Editar mandato da CIPA")


@cipa_bp.route("/mandatos/<int:mandato_id>/alternar-status", methods=["POST"])
@login_required
def alternar_status_mandato(mandato_id):
    mandato = MandatoCipa.query.get_or_404(mandato_id)
    mandato.ativo = not mandato.ativo
    db.session.commit()
    flash("Mandato reaberto." if mandato.ativo else "Mandato encerrado.", "info")
    return redirect(url_for("cipa.listar_mandatos"))


@cipa_bp.route("/mandatos/<int:mandato_id>/excluir", methods=["POST"])
@login_required
def excluir_mandato(mandato_id):
    mandato = MandatoCipa.query.get_or_404(mandato_id)
    db.session.delete(mandato)
    db.session.commit()
    flash("Mandato removido.", "info")
    return redirect(url_for("cipa.listar_mandatos"))


@cipa_bp.route("/mandatos/<int:mandato_id>/membros/novo", methods=["GET", "POST"])
@login_required
def novo_membro(mandato_id):
    mandato = MandatoCipa.query.get_or_404(mandato_id)
    form = MembroCipaForm()
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome).all()
    ]
    if form.validate_on_submit():
        membro = MembroCipa(
            mandato_id=mandato.id,
            funcionario_id=form.funcionario_id.data,
            tipo_representacao=form.tipo_representacao.data,
            cargo=form.cargo.data,
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
        )
        db.session.add(membro)
        db.session.commit()
        flash("Membro adicionado com sucesso.", "success")
        return redirect(url_for("cipa.ver_mandato", mandato_id=mandato.id))
    return render_template(
        "cipa/membro_form.html", form=form, mandato=mandato, titulo="Novo membro"
    )


@cipa_bp.route("/membros/<int:membro_id>/editar", methods=["GET", "POST"])
@login_required
def editar_membro(membro_id):
    membro = MembroCipa.query.get_or_404(membro_id)
    form = MembroCipaForm(obj=membro)
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome).all()
    ]
    if form.validate_on_submit():
        membro.funcionario_id = form.funcionario_id.data
        membro.tipo_representacao = form.tipo_representacao.data
        membro.cargo = form.cargo.data
        membro.data_inicio = form.data_inicio.data
        membro.data_fim = form.data_fim.data
        db.session.commit()
        flash("Membro atualizado com sucesso.", "success")
        return redirect(url_for("cipa.ver_mandato", mandato_id=membro.mandato_id))
    return render_template(
        "cipa/membro_form.html", form=form, mandato=membro.mandato, titulo="Editar membro"
    )


@cipa_bp.route("/membros/<int:membro_id>/excluir", methods=["POST"])
@login_required
def excluir_membro(membro_id):
    membro = MembroCipa.query.get_or_404(membro_id)
    mandato_id = membro.mandato_id
    db.session.delete(membro)
    db.session.commit()
    flash("Membro removido.", "info")
    return redirect(url_for("cipa.ver_mandato", mandato_id=mandato_id))
