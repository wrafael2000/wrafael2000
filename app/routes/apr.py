from flask import Blueprint, flash, redirect, render_template, send_file, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import AprForm, EtapaAprForm
from ..models import Apr, EtapaApr, Setor
from ..relatorios_pdf import gerar_pdf_apr

apr_bp = Blueprint("apr", __name__, url_prefix="/apr")


def _preencher_setores(form):
    form.setor_id.choices = [(s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()]


@apr_bp.route("/")
@login_required
def listar():
    aprs = Apr.query.order_by(Apr.data.desc()).all()
    return render_template("apr/listar.html", aprs=aprs)


@apr_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = AprForm()
    _preencher_setores(form)
    if form.validate_on_submit():
        apr = Apr(
            titulo=form.titulo.data.strip(),
            data=form.data.data,
            setor_id=form.setor_id.data,
            local=form.local.data,
            responsavel=form.responsavel.data.strip(),
            observacoes=form.observacoes.data,
        )
        db.session.add(apr)
        db.session.commit()
        flash("APR criada com sucesso. Adicione as etapas da atividade abaixo.", "success")
        return redirect(url_for("apr.ver", apr_id=apr.id))
    return render_template("apr/form.html", form=form, titulo="Nova APR")


@apr_bp.route("/<int:apr_id>")
@login_required
def ver(apr_id):
    apr = Apr.query.get_or_404(apr_id)
    return render_template("apr/ver.html", apr=apr)


@apr_bp.route("/<int:apr_id>/editar", methods=["GET", "POST"])
@login_required
def editar(apr_id):
    apr = Apr.query.get_or_404(apr_id)
    form = AprForm(obj=apr)
    _preencher_setores(form)
    if form.validate_on_submit():
        apr.titulo = form.titulo.data.strip()
        apr.data = form.data.data
        apr.setor_id = form.setor_id.data
        apr.local = form.local.data
        apr.responsavel = form.responsavel.data.strip()
        apr.observacoes = form.observacoes.data
        db.session.commit()
        flash("APR atualizada com sucesso.", "success")
        return redirect(url_for("apr.ver", apr_id=apr.id))
    return render_template("apr/form.html", form=form, titulo="Editar APR")


@apr_bp.route("/<int:apr_id>/excluir", methods=["POST"])
@login_required
def excluir(apr_id):
    apr = Apr.query.get_or_404(apr_id)
    db.session.delete(apr)
    db.session.commit()
    flash("APR removida.", "info")
    return redirect(url_for("apr.listar"))


@apr_bp.route("/<int:apr_id>/pdf")
@login_required
def pdf(apr_id):
    apr = Apr.query.get_or_404(apr_id)
    pdf_buffer = gerar_pdf_apr(apr)
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"apr-{apr.id}.pdf",
    )


@apr_bp.route("/<int:apr_id>/etapas/nova", methods=["GET", "POST"])
@login_required
def nova_etapa(apr_id):
    apr = Apr.query.get_or_404(apr_id)
    form = EtapaAprForm()
    if form.validate_on_submit():
        etapa = EtapaApr(
            apr_id=apr.id,
            ordem=len(apr.etapas),
            descricao_etapa=form.descricao_etapa.data,
            perigo_risco=form.perigo_risco.data,
            medida_controle=form.medida_controle.data,
        )
        db.session.add(etapa)
        db.session.commit()
        flash("Etapa adicionada com sucesso.", "success")
        return redirect(url_for("apr.ver", apr_id=apr.id))
    return render_template("apr/etapa_form.html", form=form, apr=apr, titulo="Nova etapa")


@apr_bp.route("/etapas/<int:etapa_id>/editar", methods=["GET", "POST"])
@login_required
def editar_etapa(etapa_id):
    etapa = EtapaApr.query.get_or_404(etapa_id)
    form = EtapaAprForm(obj=etapa)
    if form.validate_on_submit():
        etapa.descricao_etapa = form.descricao_etapa.data
        etapa.perigo_risco = form.perigo_risco.data
        etapa.medida_controle = form.medida_controle.data
        db.session.commit()
        flash("Etapa atualizada com sucesso.", "success")
        return redirect(url_for("apr.ver", apr_id=etapa.apr_id))
    return render_template(
        "apr/etapa_form.html", form=form, apr=etapa.apr, titulo="Editar etapa"
    )


@apr_bp.route("/etapas/<int:etapa_id>/excluir", methods=["POST"])
@login_required
def excluir_etapa(etapa_id):
    etapa = EtapaApr.query.get_or_404(etapa_id)
    apr_id = etapa.apr_id
    db.session.delete(etapa)
    db.session.commit()
    flash("Etapa removida.", "info")
    return redirect(url_for("apr.ver", apr_id=apr_id))
