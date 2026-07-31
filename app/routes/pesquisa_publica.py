from flask import Blueprint, abort, redirect, render_template, request, url_for

from ..extensions import db
from ..forms import RespostaPublicaForm
from ..models import Aplicacao, Envio, Resposta, Setor

pesquisa_publica_bp = Blueprint("pesquisa_publica", __name__, url_prefix="/responder")


def _agrupar_por_dimensao(perguntas):
    grupos = {}
    for pergunta in perguntas:
        grupos.setdefault(pergunta.dimensao, []).append(pergunta)
    return grupos


@pesquisa_publica_bp.route("/<token>", methods=["GET", "POST"])
def responder(token):
    aplicacao = Aplicacao.query.filter_by(token_publico=token).first()
    if aplicacao is None:
        abort(404)

    if not aplicacao.disponivel:
        return render_template("pesquisa_publica/encerrada.html", aplicacao=aplicacao)

    form = RespostaPublicaForm()
    form.setor_id.choices = [(0, "Prefiro não informar")] + [
        (s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()
    ]

    perguntas = aplicacao.questionario.perguntas
    erros_perguntas = []

    if form.validate_on_submit():
        respostas_coletadas = {}
        for pergunta in perguntas:
            valor_bruto = request.form.get(f"pergunta_{pergunta.id}")
            if not valor_bruto or not valor_bruto.isdigit():
                erros_perguntas.append(pergunta.id)
                continue
            valor = int(valor_bruto)
            if not (aplicacao.questionario.escala_min <= valor <= aplicacao.questionario.escala_max):
                erros_perguntas.append(pergunta.id)
                continue
            respostas_coletadas[pergunta.id] = valor

        if not erros_perguntas:
            envio = Envio(
                aplicacao_id=aplicacao.id,
                setor_id=form.setor_id.data if form.setor_id.data else None,
            )
            db.session.add(envio)
            db.session.flush()
            for pergunta_id, valor in respostas_coletadas.items():
                db.session.add(Resposta(envio_id=envio.id, pergunta_id=pergunta_id, valor=valor))
            db.session.commit()
            return redirect(url_for("pesquisa_publica.obrigado"))

    grupos = _agrupar_por_dimensao(perguntas)
    return render_template(
        "pesquisa_publica/responder.html",
        aplicacao=aplicacao,
        grupos=grupos,
        form=form,
        erros_perguntas=erros_perguntas,
    )


@pesquisa_publica_bp.route("/obrigado")
def obrigado():
    return render_template("pesquisa_publica/obrigado.html")
