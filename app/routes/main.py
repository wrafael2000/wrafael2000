from datetime import date, timedelta

from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required

from ..models import (
    Acidente,
    DocumentoSST,
    EntregaEpi,
    Exame,
    Funcionario,
    RealizacaoTreinamento,
    Setor,
)

main_bp = Blueprint("main", __name__)


def _coletar_alertas_vencimento():
    """Reúne EPIs, exames e documentos vencidos ou vencendo em um só lugar."""
    alertas = []

    for entrega in EntregaEpi.query.all():
        if entrega.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": "EPI",
                    "descricao": f"{entrega.epi.nome} — {entrega.funcionario.nome}",
                    "vencimento": entrega.data_validade,
                    "status": entrega.status,
                }
            )

    for exame in Exame.query.all():
        if exame.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": "Exame (ASO)",
                    "descricao": f"{exame.tipo} — {exame.funcionario.nome}",
                    "vencimento": exame.data_validade,
                    "status": exame.status,
                }
            )

    for documento in DocumentoSST.query.all():
        if documento.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": documento.tipo,
                    "descricao": documento.nome,
                    "vencimento": documento.data_validade,
                    "status": documento.status,
                }
            )

    for realizacao in RealizacaoTreinamento.query.all():
        if realizacao.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": "Treinamento",
                    "descricao": f"{realizacao.treinamento.nome} — {realizacao.funcionario.nome}",
                    "vencimento": realizacao.data_validade,
                    "status": realizacao.status,
                }
            )

    alertas.sort(key=lambda item: item["vencimento"])
    return alertas


@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    total_funcionarios = Funcionario.query.filter_by(ativo=True).count()
    total_setores = Setor.query.count()

    hoje = date.today()
    limite_30_dias = hoje - timedelta(days=30)
    acidentes_recentes = Acidente.query.filter(Acidente.data >= limite_30_dias).count()

    alertas = _coletar_alertas_vencimento()
    itens_vencidos = sum(1 for a in alertas if a["status"] == "vencido")
    itens_vencendo = sum(1 for a in alertas if a["status"] == "vencendo")

    return render_template(
        "dashboard.html",
        total_funcionarios=total_funcionarios,
        total_setores=total_setores,
        acidentes_recentes=acidentes_recentes,
        itens_vencidos=itens_vencidos,
        itens_vencendo=itens_vencendo,
        alertas=alertas,
    )
