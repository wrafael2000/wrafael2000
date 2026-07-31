from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import EmpresaForm
from ..models import Empresa

empresa_bp = Blueprint("empresa", __name__, url_prefix="/empresa")


@empresa_bp.route("/", methods=["GET", "POST"])
@login_required
def editar():
    empresa = Empresa.obter_ou_none()
    form = EmpresaForm(obj=empresa)

    if form.validate_on_submit():
        if empresa is None:
            empresa = Empresa()
            db.session.add(empresa)

        empresa.razao_social = form.razao_social.data.strip()
        empresa.nome_fantasia = form.nome_fantasia.data
        empresa.cnpj = form.cnpj.data
        empresa.endereco = form.endereco.data
        empresa.telefone = form.telefone.data
        empresa.email = form.email.data
        db.session.commit()
        flash("Dados da empresa salvos com sucesso.", "success")
        return redirect(url_for("empresa.editar"))

    return render_template("empresa/form.html", form=form, empresa=empresa)
