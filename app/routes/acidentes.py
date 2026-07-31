from flask import Blueprint, flash, redirect, render_template, send_file, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import AcidenteForm
from ..models import Acidente, Funcionario
from ..relatorios import coletar_dados_acidentes
from ..relatorios_pdf import gerar_pdf_relatorio_acidentes

acidentes_bp = Blueprint("acidentes", __name__, url_prefix="/acidentes")


def _preencher_funcionarios(form):
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.order_by(Funcionario.nome).all()
    ]


@acidentes_bp.route("/")
@login_required
def listar():
    acidentes = Acidente.query.order_by(Acidente.data.desc()).all()
    return render_template("acidentes/listar.html", acidentes=acidentes)


@acidentes_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = AcidenteForm()
    _preencher_funcionarios(form)
    if form.validate_on_submit():
        acidente = Acidente(
            funcionario_id=form.funcionario_id.data,
            data=form.data.data,
            local=form.local.data.strip(),
            tipo=form.tipo.data,
            gravidade=form.gravidade.data,
            descricao=form.descricao.data,
            causa=form.causa.data,
            medidas_tomadas=form.medidas_tomadas.data,
            dias_afastamento=form.dias_afastamento.data or 0,
        )
        db.session.add(acidente)
        db.session.commit()
        flash("Ocorrência registrada com sucesso.", "success")
        return redirect(url_for("acidentes.listar"))
    return render_template("acidentes/form.html", form=form, titulo="Nova ocorrência")


@acidentes_bp.route("/<int:acidente_id>/editar", methods=["GET", "POST"])
@login_required
def editar(acidente_id):
    acidente = Acidente.query.get_or_404(acidente_id)
    form = AcidenteForm(obj=acidente)
    _preencher_funcionarios(form)
    if form.validate_on_submit():
        acidente.funcionario_id = form.funcionario_id.data
        acidente.data = form.data.data
        acidente.local = form.local.data.strip()
        acidente.tipo = form.tipo.data
        acidente.gravidade = form.gravidade.data
        acidente.descricao = form.descricao.data
        acidente.causa = form.causa.data
        acidente.medidas_tomadas = form.medidas_tomadas.data
        acidente.dias_afastamento = form.dias_afastamento.data or 0
        db.session.commit()
        flash("Ocorrência atualizada com sucesso.", "success")
        return redirect(url_for("acidentes.listar"))
    return render_template("acidentes/form.html", form=form, titulo="Editar ocorrência")


@acidentes_bp.route("/<int:acidente_id>/excluir", methods=["POST"])
@login_required
def excluir(acidente_id):
    acidente = Acidente.query.get_or_404(acidente_id)
    db.session.delete(acidente)
    db.session.commit()
    flash("Ocorrência removida.", "info")
    return redirect(url_for("acidentes.listar"))


@acidentes_bp.route("/relatorio")
@login_required
def relatorio():
    return render_template("acidentes/relatorio.html", **coletar_dados_acidentes())


@acidentes_bp.route("/relatorio.pdf")
@login_required
def relatorio_pdf():
    dados = coletar_dados_acidentes()
    pdf = gerar_pdf_relatorio_acidentes(dados)
    return send_file(
        pdf,
        mimetype="application/pdf",
        as_attachment=True,
        download_name="relatorio-acidentes.pdf",
    )
