from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ItemConformidadeNRForm, NormaRegulamentadoraForm
from ..models import ItemConformidadeNR, NormaRegulamentadora

normas_bp = Blueprint("normas", __name__, url_prefix="/normas")


@normas_bp.route("/")
@login_required
def listar():
    normas = NormaRegulamentadora.query.order_by(NormaRegulamentadora.numero).all()
    return render_template("normas/listar.html", normas=normas)


@normas_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = NormaRegulamentadoraForm()
    if form.validate_on_submit():
        norma = NormaRegulamentadora(
            numero=form.numero.data.strip(),
            titulo=form.titulo.data.strip(),
            aplicavel=form.aplicavel.data,
            link_oficial=form.link_oficial.data,
            observacao=form.observacao.data,
        )
        db.session.add(norma)
        db.session.commit()
        flash("Norma cadastrada com sucesso.", "success")
        return redirect(url_for("normas.listar"))
    return render_template("normas/form.html", form=form, titulo="Nova norma")


@normas_bp.route("/<int:norma_id>")
@login_required
def ver(norma_id):
    norma = NormaRegulamentadora.query.get_or_404(norma_id)
    return render_template("normas/ver.html", norma=norma)


@normas_bp.route("/<int:norma_id>/editar", methods=["GET", "POST"])
@login_required
def editar(norma_id):
    norma = NormaRegulamentadora.query.get_or_404(norma_id)
    form = NormaRegulamentadoraForm(obj=norma)
    if form.validate_on_submit():
        norma.numero = form.numero.data.strip()
        norma.titulo = form.titulo.data.strip()
        norma.aplicavel = form.aplicavel.data
        norma.link_oficial = form.link_oficial.data
        norma.observacao = form.observacao.data
        db.session.commit()
        flash("Norma atualizada com sucesso.", "success")
        return redirect(url_for("normas.ver", norma_id=norma.id))
    return render_template("normas/form.html", form=form, titulo="Editar norma")


@normas_bp.route("/<int:norma_id>/excluir", methods=["POST"])
@login_required
def excluir(norma_id):
    norma = NormaRegulamentadora.query.get_or_404(norma_id)
    db.session.delete(norma)
    db.session.commit()
    flash("Norma removida.", "info")
    return redirect(url_for("normas.listar"))


@normas_bp.route("/<int:norma_id>/itens/novo", methods=["GET", "POST"])
@login_required
def novo_item(norma_id):
    norma = NormaRegulamentadora.query.get_or_404(norma_id)
    form = ItemConformidadeNRForm()
    if form.validate_on_submit():
        item = ItemConformidadeNR(
            norma_id=norma.id,
            descricao=form.descricao.data,
            status=form.status.data,
            responsavel=form.responsavel.data,
            prazo=form.prazo.data,
            observacao=form.observacao.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Item de conformidade adicionado com sucesso.", "success")
        return redirect(url_for("normas.ver", norma_id=norma.id))
    return render_template(
        "normas/item_form.html", form=form, norma=norma, titulo="Novo item de conformidade"
    )


@normas_bp.route("/itens/<int:item_id>/editar", methods=["GET", "POST"])
@login_required
def editar_item(item_id):
    item = ItemConformidadeNR.query.get_or_404(item_id)
    form = ItemConformidadeNRForm(obj=item)
    if form.validate_on_submit():
        item.descricao = form.descricao.data
        item.status = form.status.data
        item.responsavel = form.responsavel.data
        item.prazo = form.prazo.data
        item.observacao = form.observacao.data
        db.session.commit()
        flash("Item de conformidade atualizado com sucesso.", "success")
        return redirect(url_for("normas.ver", norma_id=item.norma_id))
    return render_template(
        "normas/item_form.html", form=form, norma=item.norma, titulo="Editar item de conformidade"
    )


@normas_bp.route("/itens/<int:item_id>/excluir", methods=["POST"])
@login_required
def excluir_item(item_id):
    item = ItemConformidadeNR.query.get_or_404(item_id)
    norma_id = item.norma_id
    db.session.delete(item)
    db.session.commit()
    flash("Item removido.", "info")
    return redirect(url_for("normas.ver", norma_id=norma_id))
