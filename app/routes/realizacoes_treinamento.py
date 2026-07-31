from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import RealizacaoTreinamentoForm
from ..models import Funcionario, RealizacaoTreinamento, Treinamento

realizacoes_treinamento_bp = Blueprint(
    "realizacoes_treinamento", __name__, url_prefix="/realizacoes-treinamento"
)


def _preencher_selects(form):
    form.funcionario_id.choices = [
        (f.id, f.nome) for f in Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome).all()
    ]
    form.treinamento_id.choices = [
        (t.id, t.nome) for t in Treinamento.query.order_by(Treinamento.nome).all()
    ]


@realizacoes_treinamento_bp.route("/")
@login_required
def listar():
    realizacoes = RealizacaoTreinamento.query.order_by(
        RealizacaoTreinamento.data_realizacao.desc()
    ).all()
    return render_template("realizacoes_treinamento/listar.html", realizacoes=realizacoes)


@realizacoes_treinamento_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = RealizacaoTreinamentoForm()
    _preencher_selects(form)
    if form.validate_on_submit():
        realizacao = RealizacaoTreinamento(
            funcionario_id=form.funcionario_id.data,
            treinamento_id=form.treinamento_id.data,
            data_realizacao=form.data_realizacao.data,
            instrutor=form.instrutor.data,
            observacao=form.observacao.data,
        )
        realizacao.treinamento = Treinamento.query.get(form.treinamento_id.data)
        realizacao.calcular_validade()
        db.session.add(realizacao)
        db.session.commit()
        flash("Realização de treinamento registrada com sucesso.", "success")
        return redirect(url_for("realizacoes_treinamento.listar"))
    return render_template(
        "realizacoes_treinamento/form.html", form=form, titulo="Nova realização de treinamento"
    )


@realizacoes_treinamento_bp.route("/<int:realizacao_id>/editar", methods=["GET", "POST"])
@login_required
def editar(realizacao_id):
    realizacao = RealizacaoTreinamento.query.get_or_404(realizacao_id)
    form = RealizacaoTreinamentoForm(obj=realizacao)
    _preencher_selects(form)
    if form.validate_on_submit():
        realizacao.funcionario_id = form.funcionario_id.data
        realizacao.treinamento_id = form.treinamento_id.data
        realizacao.data_realizacao = form.data_realizacao.data
        realizacao.instrutor = form.instrutor.data
        realizacao.observacao = form.observacao.data
        realizacao.treinamento = Treinamento.query.get(form.treinamento_id.data)
        realizacao.calcular_validade()
        db.session.commit()
        flash("Realização de treinamento atualizada com sucesso.", "success")
        return redirect(url_for("realizacoes_treinamento.listar"))
    return render_template(
        "realizacoes_treinamento/form.html", form=form, titulo="Editar realização de treinamento"
    )


@realizacoes_treinamento_bp.route("/<int:realizacao_id>/excluir", methods=["POST"])
@login_required
def excluir(realizacao_id):
    realizacao = RealizacaoTreinamento.query.get_or_404(realizacao_id)
    db.session.delete(realizacao)
    db.session.commit()
    flash("Realização removida.", "info")
    return redirect(url_for("realizacoes_treinamento.listar"))
