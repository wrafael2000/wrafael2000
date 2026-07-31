from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import EpiForm
from ..models import Epi

epis_bp = Blueprint("epis", __name__, url_prefix="/epis")


@epis_bp.route("/")
@login_required
def listar():
    epis = Epi.query.order_by(Epi.nome).all()
    return render_template("epis/listar.html", epis=epis)


@epis_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = EpiForm()
    if form.validate_on_submit():
        epi = Epi(
            nome=form.nome.data.strip(),
            ca=form.ca.data,
            validade_dias=form.validade_dias.data,
        )
        db.session.add(epi)
        db.session.commit()
        flash("EPI cadastrado com sucesso.", "success")
        return redirect(url_for("epis.listar"))
    return render_template("epis/form.html", form=form, titulo="Novo EPI")


@epis_bp.route("/<int:epi_id>/editar", methods=["GET", "POST"])
@login_required
def editar(epi_id):
    epi = Epi.query.get_or_404(epi_id)
    form = EpiForm(obj=epi)
    if form.validate_on_submit():
        epi.nome = form.nome.data.strip()
        epi.ca = form.ca.data
        epi.validade_dias = form.validade_dias.data
        db.session.commit()
        flash("EPI atualizado com sucesso.", "success")
        return redirect(url_for("epis.listar"))
    return render_template("epis/form.html", form=form, titulo="Editar EPI")


@epis_bp.route("/<int:epi_id>/excluir", methods=["POST"])
@login_required
def excluir(epi_id):
    epi = Epi.query.get_or_404(epi_id)
    db.session.delete(epi)
    db.session.commit()
    flash("EPI removido.", "info")
    return redirect(url_for("epis.listar"))
