from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from ..models import Funcionario, Setor

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    total_funcionarios = Funcionario.query.filter_by(ativo=True).count()
    total_setores = Setor.query.count()
    return render_template(
        "dashboard.html",
        total_funcionarios=total_funcionarios,
        total_setores=total_setores,
    )
