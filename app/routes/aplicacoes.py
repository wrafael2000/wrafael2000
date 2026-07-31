from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import AplicacaoForm, PlanoAcaoPsicossocialForm
from ..models import Aplicacao, PlanoAcaoPsicossocial, Questionario

aplicacoes_bp = Blueprint("aplicacoes", __name__, url_prefix="/aplicacoes")


def _preencher_questionarios(form):
    form.questionario_id.choices = [
        (q.id, q.nome) for q in Questionario.query.order_by(Questionario.nome).all()
    ]


@aplicacoes_bp.route("/")
@login_required
def listar():
    aplicacoes = Aplicacao.query.order_by(Aplicacao.data_inicio.desc()).all()
    return render_template("aplicacoes/listar.html", aplicacoes=aplicacoes)


@aplicacoes_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = AplicacaoForm()
    _preencher_questionarios(form)
    if form.validate_on_submit():
        aplicacao = Aplicacao(
            questionario_id=form.questionario_id.data,
            titulo=form.titulo.data.strip(),
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
        )
        db.session.add(aplicacao)
        db.session.commit()
        flash("Aplicação criada com sucesso. Compartilhe o link público com os funcionários.", "success")
        return redirect(url_for("aplicacoes.listar"))
    return render_template("aplicacoes/form.html", form=form, titulo="Nova aplicação")


@aplicacoes_bp.route("/<int:aplicacao_id>/alternar-status", methods=["POST"])
@login_required
def alternar_status(aplicacao_id):
    aplicacao = Aplicacao.query.get_or_404(aplicacao_id)
    aplicacao.ativa = not aplicacao.ativa
    db.session.commit()
    flash("Aplicação reaberta." if aplicacao.ativa else "Aplicação encerrada.", "info")
    return redirect(url_for("aplicacoes.listar"))


@aplicacoes_bp.route("/<int:aplicacao_id>/resultados")
@login_required
def resultados(aplicacao_id):
    aplicacao = Aplicacao.query.get_or_404(aplicacao_id)

    somas = defaultdict(int)
    contagens = defaultdict(int)
    for envio in aplicacao.envios:
        for resposta in envio.respostas:
            dimensao = resposta.pergunta.dimensao
            somas[dimensao] += resposta.valor
            contagens[dimensao] += 1

    medias_por_dimensao = [
        {"dimensao": dimensao, "media": round(somas[dimensao] / contagens[dimensao], 2), "respostas": contagens[dimensao]}
        for dimensao in sorted(somas)
    ]

    planos_acao = PlanoAcaoPsicossocial.query.filter_by(aplicacao_id=aplicacao.id).all()

    return render_template(
        "aplicacoes/resultados.html",
        aplicacao=aplicacao,
        total_envios=len(aplicacao.envios),
        medias_por_dimensao=medias_por_dimensao,
        planos_acao=planos_acao,
    )


@aplicacoes_bp.route("/<int:aplicacao_id>/planos-acao/novo", methods=["GET", "POST"])
@login_required
def novo_plano_acao(aplicacao_id):
    aplicacao = Aplicacao.query.get_or_404(aplicacao_id)
    form = PlanoAcaoPsicossocialForm()
    if form.validate_on_submit():
        plano = PlanoAcaoPsicossocial(
            aplicacao_id=aplicacao.id,
            dimensao=form.dimensao.data,
            descricao=form.descricao.data,
            responsavel=form.responsavel.data,
            prazo=form.prazo.data,
            status=form.status.data,
        )
        db.session.add(plano)
        db.session.commit()
        flash("Ação registrada com sucesso.", "success")
        return redirect(url_for("aplicacoes.resultados", aplicacao_id=aplicacao.id))
    return render_template(
        "aplicacoes/plano_acao_form.html", form=form, aplicacao=aplicacao, titulo="Nova ação"
    )


@aplicacoes_bp.route("/planos-acao/<int:plano_id>/editar", methods=["GET", "POST"])
@login_required
def editar_plano_acao(plano_id):
    plano = PlanoAcaoPsicossocial.query.get_or_404(plano_id)
    form = PlanoAcaoPsicossocialForm(obj=plano)
    if form.validate_on_submit():
        plano.dimensao = form.dimensao.data
        plano.descricao = form.descricao.data
        plano.responsavel = form.responsavel.data
        plano.prazo = form.prazo.data
        plano.status = form.status.data
        db.session.commit()
        flash("Ação atualizada com sucesso.", "success")
        return redirect(url_for("aplicacoes.resultados", aplicacao_id=plano.aplicacao_id))
    return render_template(
        "aplicacoes/plano_acao_form.html", form=form, aplicacao=plano.aplicacao, titulo="Editar ação"
    )


@aplicacoes_bp.route("/planos-acao/<int:plano_id>/excluir", methods=["POST"])
@login_required
def excluir_plano_acao(plano_id):
    plano = PlanoAcaoPsicossocial.query.get_or_404(plano_id)
    aplicacao_id = plano.aplicacao_id
    db.session.delete(plano)
    db.session.commit()
    flash("Ação removida.", "info")
    return redirect(url_for("aplicacoes.resultados", aplicacao_id=aplicacao_id))
