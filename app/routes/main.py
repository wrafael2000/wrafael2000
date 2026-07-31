from datetime import date, timedelta

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from ..models import Acidente, EntregaEpi, Funcionario, Setor

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    total_funcionarios = Funcionario.query.filter_by(ativo=True).count()
    total_setores = Setor.query.count()

    hoje = date.today()
    limite_alerta = hoje + timedelta(days=EntregaEpi.DIAS_ALERTA_VENCIMENTO)
    epis_vencidos = EntregaEpi.query.filter(EntregaEpi.data_validade < hoje).count()
    epis_vencendo = EntregaEpi.query.filter(
        EntregaEpi.data_validade >= hoje, EntregaEpi.data_validade <= limite_alerta
    ).count()

    limite_30_dias = hoje - timedelta(days=30)
    acidentes_recentes = Acidente.query.filter(Acidente.data >= limite_30_dias).count()

    return render_template(
        "dashboard.html",
        total_funcionarios=total_funcionarios,
        total_setores=total_setores,
        epis_vencidos=epis_vencidos,
        epis_vencendo=epis_vencendo,
        acidentes_recentes=acidentes_recentes,
    )
