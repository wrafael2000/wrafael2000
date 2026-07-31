from flask import Blueprint, flash, redirect, render_template, send_file, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import PppExposicaoForm, PppForm
from ..models import Funcionario, Ppp, PppExposicao, Setor
from ..relatorios_pdf import gerar_pdf_ppp

ppp_bp = Blueprint("ppp", __name__, url_prefix="/ppp")


def _preencher_funcionarios(form):
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.order_by(Funcionario.nome).all()
    ]


def _preencher_setores(form):
    form.setor_id.choices = [(s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()]


@ppp_bp.route("/")
@login_required
def listar():
    registros = Ppp.query.join(Ppp.funcionario).order_by(Ppp.data_emissao.desc()).all()
    return render_template("ppp/listar.html", registros=registros)


@ppp_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = PppForm()
    _preencher_funcionarios(form)
    if form.validate_on_submit():
        ppp = Ppp(
            funcionario_id=form.funcionario_id.data,
            data_emissao=form.data_emissao.data,
            responsavel_emissao=form.responsavel_emissao.data.strip(),
            responsavel_tecnico_seguranca=form.responsavel_tecnico_seguranca.data,
            responsavel_tecnico_seguranca_registro=form.responsavel_tecnico_seguranca_registro.data,
            medico_coordenador=form.medico_coordenador.data,
            medico_coordenador_crm=form.medico_coordenador_crm.data,
            observacoes=form.observacoes.data,
        )
        db.session.add(ppp)
        db.session.commit()
        flash("PPP criado com sucesso. Adicione o histórico de exposição abaixo.", "success")
        return redirect(url_for("ppp.ver", ppp_id=ppp.id))
    return render_template("ppp/form.html", form=form, titulo="Novo PPP")


@ppp_bp.route("/<int:ppp_id>")
@login_required
def ver(ppp_id):
    ppp = Ppp.query.get_or_404(ppp_id)
    return render_template("ppp/ver.html", ppp=ppp)


@ppp_bp.route("/<int:ppp_id>/editar", methods=["GET", "POST"])
@login_required
def editar(ppp_id):
    ppp = Ppp.query.get_or_404(ppp_id)
    form = PppForm(obj=ppp)
    _preencher_funcionarios(form)
    if form.validate_on_submit():
        ppp.funcionario_id = form.funcionario_id.data
        ppp.data_emissao = form.data_emissao.data
        ppp.responsavel_emissao = form.responsavel_emissao.data.strip()
        ppp.responsavel_tecnico_seguranca = form.responsavel_tecnico_seguranca.data
        ppp.responsavel_tecnico_seguranca_registro = form.responsavel_tecnico_seguranca_registro.data
        ppp.medico_coordenador = form.medico_coordenador.data
        ppp.medico_coordenador_crm = form.medico_coordenador_crm.data
        ppp.observacoes = form.observacoes.data
        db.session.commit()
        flash("PPP atualizado com sucesso.", "success")
        return redirect(url_for("ppp.ver", ppp_id=ppp.id))
    return render_template("ppp/form.html", form=form, titulo="Editar PPP")


@ppp_bp.route("/<int:ppp_id>/excluir", methods=["POST"])
@login_required
def excluir(ppp_id):
    ppp = Ppp.query.get_or_404(ppp_id)
    db.session.delete(ppp)
    db.session.commit()
    flash("PPP removido.", "info")
    return redirect(url_for("ppp.listar"))


@ppp_bp.route("/<int:ppp_id>/pdf")
@login_required
def pdf(ppp_id):
    ppp = Ppp.query.get_or_404(ppp_id)
    pdf_buffer = gerar_pdf_ppp(ppp)
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"ppp-{ppp.id}.pdf",
    )


@ppp_bp.route("/<int:ppp_id>/exposicoes/nova", methods=["GET", "POST"])
@login_required
def nova_exposicao(ppp_id):
    ppp = Ppp.query.get_or_404(ppp_id)
    form = PppExposicaoForm()
    _preencher_setores(form)
    if form.validate_on_submit():
        exposicao = PppExposicao(
            ppp_id=ppp.id,
            setor_id=form.setor_id.data,
            funcao=form.funcao.data.strip(),
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            tipo_agente=form.tipo_agente.data,
            agente_nocivo=form.agente_nocivo.data,
            intensidade_concentracao=form.intensidade_concentracao.data,
            epi_eficaz=form.epi_eficaz.data,
            observacoes=form.observacoes.data,
        )
        db.session.add(exposicao)
        db.session.commit()
        flash("Período de exposição adicionado com sucesso.", "success")
        return redirect(url_for("ppp.ver", ppp_id=ppp.id))
    return render_template(
        "ppp/exposicao_form.html", form=form, ppp=ppp, titulo="Novo período de exposição"
    )


@ppp_bp.route("/exposicoes/<int:exposicao_id>/editar", methods=["GET", "POST"])
@login_required
def editar_exposicao(exposicao_id):
    exposicao = PppExposicao.query.get_or_404(exposicao_id)
    form = PppExposicaoForm(obj=exposicao)
    _preencher_setores(form)
    if form.validate_on_submit():
        exposicao.setor_id = form.setor_id.data
        exposicao.funcao = form.funcao.data.strip()
        exposicao.data_inicio = form.data_inicio.data
        exposicao.data_fim = form.data_fim.data
        exposicao.tipo_agente = form.tipo_agente.data
        exposicao.agente_nocivo = form.agente_nocivo.data
        exposicao.intensidade_concentracao = form.intensidade_concentracao.data
        exposicao.epi_eficaz = form.epi_eficaz.data
        exposicao.observacoes = form.observacoes.data
        db.session.commit()
        flash("Período de exposição atualizado com sucesso.", "success")
        return redirect(url_for("ppp.ver", ppp_id=exposicao.ppp_id))
    return render_template(
        "ppp/exposicao_form.html", form=form, ppp=exposicao.ppp, titulo="Editar período de exposição"
    )


@ppp_bp.route("/exposicoes/<int:exposicao_id>/excluir", methods=["POST"])
@login_required
def excluir_exposicao(exposicao_id):
    exposicao = PppExposicao.query.get_or_404(exposicao_id)
    ppp_id = exposicao.ppp_id
    db.session.delete(exposicao)
    db.session.commit()
    flash("Período de exposição removido.", "info")
    return redirect(url_for("ppp.ver", ppp_id=ppp_id))
