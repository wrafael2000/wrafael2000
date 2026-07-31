from flask import Blueprint, redirect, render_template, send_file, url_for
from flask_login import login_required

from ..relatorios import coletar_dados_gerais
from ..relatorios_pdf import gerar_pdf_relatorio_geral

main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    return redirect(url_for("main.dashboard"))


@main_bp.route("/dashboard")
@login_required
def dashboard():
    dados = coletar_dados_gerais()
    return render_template("dashboard.html", **dados)


@main_bp.route("/dashboard/relatorio.pdf")
@login_required
def relatorio_geral_pdf():
    dados = coletar_dados_gerais()
    pdf = gerar_pdf_relatorio_geral(dados)
    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="relatorio-geral-sst.pdf",
    )
