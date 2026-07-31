from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import EmpresaForm
from ..models import Aplicacao, Empresa

empresa_bp = Blueprint("empresa", __name__, url_prefix="/empresa")


@empresa_bp.route("/")
@login_required
def listar():
    empresas = Empresa.query.order_by(Empresa.razao_social).all()
    return render_template("empresa/listar.html", empresas=empresas)


@empresa_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = EmpresaForm()
    if form.validate_on_submit():
        empresa = Empresa(
            razao_social=form.razao_social.data.strip(),
            nome_fantasia=form.nome_fantasia.data,
            cnpj=form.cnpj.data,
            endereco=form.endereco.data,
            telefone=form.telefone.data,
            email=form.email.data,
        )
        db.session.add(empresa)
        db.session.commit()
        flash("Empresa cadastrada com sucesso.", "success")
        return redirect(url_for("empresa.listar"))
    return render_template("empresa/form.html", form=form, titulo="Nova empresa")


@empresa_bp.route("/<int:empresa_id>/editar", methods=["GET", "POST"])
@login_required
def editar(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    form = EmpresaForm(obj=empresa)
    if form.validate_on_submit():
        empresa.razao_social = form.razao_social.data.strip()
        empresa.nome_fantasia = form.nome_fantasia.data
        empresa.cnpj = form.cnpj.data
        empresa.endereco = form.endereco.data
        empresa.telefone = form.telefone.data
        empresa.email = form.email.data
        db.session.commit()
        flash("Dados da empresa atualizados com sucesso.", "success")
        return redirect(url_for("empresa.listar"))
    return render_template("empresa/form.html", form=form, titulo="Editar empresa")


@empresa_bp.route("/<int:empresa_id>/excluir", methods=["POST"])
@login_required
def excluir(empresa_id):
    empresa = Empresa.query.get_or_404(empresa_id)
    if Aplicacao.query.filter_by(empresa_id=empresa.id).first() is not None:
        flash(
            "Não é possível remover esta empresa: existem avaliações de questionário "
            "vinculadas a ela.",
            "danger",
        )
        return redirect(url_for("empresa.listar"))
    db.session.delete(empresa)
    db.session.commit()
    flash("Empresa removida.", "info")
    return redirect(url_for("empresa.listar"))
