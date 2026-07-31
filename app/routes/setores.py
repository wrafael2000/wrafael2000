from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import SetorForm
from ..models import Setor

setores_bp = Blueprint("setores", __name__, url_prefix="/setores")


@setores_bp.route("/")
@login_required
def listar():
    setores = Setor.query.order_by(Setor.nome).all()
    return render_template("setores/listar.html", setores=setores)


@setores_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = SetorForm()
    if form.validate_on_submit():
        setor = Setor(nome=form.nome.data.strip(), descricao=form.descricao.data)
        db.session.add(setor)
        db.session.commit()
        flash("Setor cadastrado com sucesso.", "success")
        return redirect(url_for("setores.listar"))
    return render_template("setores/form.html", form=form, titulo="Novo setor")


@setores_bp.route("/<int:setor_id>/editar", methods=["GET", "POST"])
@login_required
def editar(setor_id):
    setor = Setor.query.get_or_404(setor_id)
    form = SetorForm(obj=setor)
    if form.validate_on_submit():
        setor.nome = form.nome.data.strip()
        setor.descricao = form.descricao.data
        db.session.commit()
        flash("Setor atualizado com sucesso.", "success")
        return redirect(url_for("setores.listar"))
    return render_template("setores/form.html", form=form, titulo="Editar setor")


@setores_bp.route("/<int:setor_id>/excluir", methods=["POST"])
@login_required
def excluir(setor_id):
    setor = Setor.query.get_or_404(setor_id)
    db.session.delete(setor)
    db.session.commit()
    flash("Setor removido.", "info")
    return redirect(url_for("setores.listar"))
