from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import AtividadeSipatForm, SipatEdicaoForm
from ..models import AtividadeSipat, SipatEdicao

sipat_bp = Blueprint("sipat", __name__, url_prefix="/sipat")


@sipat_bp.route("/")
@login_required
def listar():
    edicoes = SipatEdicao.query.order_by(SipatEdicao.data_inicio.desc()).all()
    return render_template("sipat/listar.html", edicoes=edicoes)


@sipat_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = SipatEdicaoForm()
    if form.validate_on_submit():
        edicao = SipatEdicao(
            titulo=form.titulo.data.strip(),
            tema=form.tema.data,
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
        )
        db.session.add(edicao)
        db.session.commit()
        flash("Edição da SIPAT criada com sucesso.", "success")
        return redirect(url_for("sipat.ver", sipat_id=edicao.id))
    return render_template("sipat/form.html", form=form, titulo="Nova edição da SIPAT")


@sipat_bp.route("/<int:sipat_id>")
@login_required
def ver(sipat_id):
    edicao = SipatEdicao.query.get_or_404(sipat_id)
    return render_template("sipat/ver.html", edicao=edicao)


@sipat_bp.route("/<int:sipat_id>/editar", methods=["GET", "POST"])
@login_required
def editar(sipat_id):
    edicao = SipatEdicao.query.get_or_404(sipat_id)
    form = SipatEdicaoForm(obj=edicao)
    if form.validate_on_submit():
        edicao.titulo = form.titulo.data.strip()
        edicao.tema = form.tema.data
        edicao.data_inicio = form.data_inicio.data
        edicao.data_fim = form.data_fim.data
        db.session.commit()
        flash("Edição da SIPAT atualizada com sucesso.", "success")
        return redirect(url_for("sipat.ver", sipat_id=edicao.id))
    return render_template("sipat/form.html", form=form, titulo="Editar edição da SIPAT")


@sipat_bp.route("/<int:sipat_id>/excluir", methods=["POST"])
@login_required
def excluir(sipat_id):
    edicao = SipatEdicao.query.get_or_404(sipat_id)
    db.session.delete(edicao)
    db.session.commit()
    flash("Edição da SIPAT removida.", "info")
    return redirect(url_for("sipat.listar"))


@sipat_bp.route("/<int:sipat_id>/atividades/nova", methods=["GET", "POST"])
@login_required
def nova_atividade(sipat_id):
    edicao = SipatEdicao.query.get_or_404(sipat_id)
    form = AtividadeSipatForm()
    if form.validate_on_submit():
        atividade = AtividadeSipat(
            sipat_id=edicao.id,
            titulo=form.titulo.data.strip(),
            descricao=form.descricao.data,
            data=form.data.data,
            hora_inicio=form.hora_inicio.data,
            responsavel=form.responsavel.data,
            local=form.local.data,
        )
        db.session.add(atividade)
        db.session.commit()
        flash("Atividade adicionada com sucesso.", "success")
        return redirect(url_for("sipat.ver", sipat_id=edicao.id))
    return render_template(
        "sipat/atividade_form.html", form=form, edicao=edicao, titulo="Nova atividade"
    )


@sipat_bp.route("/atividades/<int:atividade_id>/editar", methods=["GET", "POST"])
@login_required
def editar_atividade(atividade_id):
    atividade = AtividadeSipat.query.get_or_404(atividade_id)
    form = AtividadeSipatForm(obj=atividade)
    if form.validate_on_submit():
        atividade.titulo = form.titulo.data.strip()
        atividade.descricao = form.descricao.data
        atividade.data = form.data.data
        atividade.hora_inicio = form.hora_inicio.data
        atividade.responsavel = form.responsavel.data
        atividade.local = form.local.data
        db.session.commit()
        flash("Atividade atualizada com sucesso.", "success")
        return redirect(url_for("sipat.ver", sipat_id=atividade.sipat_id))
    return render_template(
        "sipat/atividade_form.html", form=form, edicao=atividade.sipat, titulo="Editar atividade"
    )


@sipat_bp.route("/atividades/<int:atividade_id>/excluir", methods=["POST"])
@login_required
def excluir_atividade(atividade_id):
    atividade = AtividadeSipat.query.get_or_404(atividade_id)
    sipat_id = atividade.sipat_id
    db.session.delete(atividade)
    db.session.commit()
    flash("Atividade removida.", "info")
    return redirect(url_for("sipat.ver", sipat_id=sipat_id))
