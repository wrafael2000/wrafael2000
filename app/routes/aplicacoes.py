from collections import defaultdict

from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import AplicacaoForm, PlanoAcaoPsicossocialForm, SegmentoAplicacaoForm
from ..models import Aplicacao, Empresa, PlanoAcaoPsicossocial, Questionario, SegmentoAplicacao, Setor

aplicacoes_bp = Blueprint("aplicacoes", __name__, url_prefix="/aplicacoes")

INFO_INSTRUMENTOS = {
    "HSE-IT": {
        "titulo": "Sobre o HSE-IT",
        "paragrafos": [
            "O HSE Management Standards Indicator Tool (HSE-IT) é um instrumento desenvolvido pelo "
            "Health and Safety Executive do Reino Unido para identificar fatores de risco "
            "psicossocial relacionados à organização do trabalho.",
            "A versão completa contém 35 questões que avaliam 7 dimensões: Demandas, Controle, "
            "Suporte da chefia, Suporte dos colegas, Relacionamentos, Papel (clareza de função) e "
            "Mudança organizacional.",
        ],
    },
    "COPSOQ II": {
        "titulo": "Sobre o COPSOQ II",
        "paragrafos": [
            "O COPSOQ II (Copenhagen Psychosocial Questionnaire) é um instrumento validado "
            "internacionalmente para avaliação de fatores psicossociais no trabalho.",
            "A versão curta contém 41 questões que avaliam 23 dimensões organizadas em 6 grupos: "
            "Exigências do Trabalho, Organização e Conteúdo, Relações e Liderança, Interface "
            "Trabalho-Indivíduo, Saúde e Bem-estar e Valores no Local de Trabalho.",
        ],
    },
    "CBI (Burnout)": {
        "titulo": "Sobre o CBI",
        "paragrafos": [
            "O CBI (Copenhagen Burnout Inventory) é um instrumento validado internacionalmente para "
            "avaliação do esgotamento profissional (burnout).",
            "Contém 19 itens organizados em 3 dimensões: Burnout pessoal (exaustão física e "
            "psicológica em geral), Burnout relacionado ao trabalho e Burnout relacionado ao "
            "público atendido (clientes, alunos, pacientes etc., quando aplicável).",
        ],
    },
    "Clima Organizacional": {
        "titulo": "Sobre a pesquisa de Clima Organizacional",
        "paragrafos": [
            "A pesquisa de Clima Organizacional é um instrumento personalizável usado para captar a "
            "percepção dos colaboradores sobre o ambiente de trabalho, liderança, comunicação, "
            "reconhecimento e outros aspectos definidos pela empresa.",
            "Diferente do HSE-IT, COPSOQ II e CBI, não é um instrumento cientificamente padronizado "
            "— as perguntas e dimensões são definidas pela própria empresa ao montar o questionário.",
        ],
    },
}


def _info_instrumento(questionario):
    return INFO_INSTRUMENTOS.get(
        questionario.tipo,
        {
            "titulo": "Sobre o instrumento",
            "paragrafos": [questionario.descricao or "Instrumento personalizado desta empresa."],
        },
    )


def _preencher_questionarios(form):
    form.questionario_id.choices = [
        (q.id, q.nome) for q in Questionario.query.order_by(Questionario.nome).all()
    ]


def _preencher_empresas(form):
    form.empresa_id.choices = [
        (e.id, e.nome_fantasia or e.razao_social) for e in Empresa.query.order_by(Empresa.razao_social).all()
    ]


def _preencher_setores(form, aplicacao, segmento_atual=None):
    ids_usados = {s.setor_id for s in aplicacao.segmentos if s is not segmento_atual}
    form.setor_id.choices = [
        (s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all() if s.id not in ids_usados
    ]


@aplicacoes_bp.route("/")
@login_required
def listar():
    aplicacoes = Aplicacao.query.order_by(Aplicacao.data_inicio.desc()).all()
    return render_template("aplicacoes/listar.html", aplicacoes=aplicacoes)


@aplicacoes_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    if Empresa.query.first() is None:
        flash("Cadastre uma empresa antes de criar uma nova avaliação.", "danger")
        return redirect(url_for("empresa.nova"))

    form = AplicacaoForm()
    _preencher_empresas(form)
    _preencher_questionarios(form)
    if form.validate_on_submit():
        aplicacao = Aplicacao(
            empresa_id=form.empresa_id.data,
            questionario_id=form.questionario_id.data,
            titulo=form.titulo.data.strip(),
            descricao=form.descricao.data,
            data_inicio=form.data_inicio.data,
            data_fim=form.data_fim.data,
            ativa=form.ativa.data,
            multisetorial=form.multisetorial.data,
        )
        db.session.add(aplicacao)
        db.session.commit()
        flash("Avaliação criada com sucesso. Configure os setores participantes abaixo.", "success")
        return redirect(url_for("aplicacoes.ver", aplicacao_id=aplicacao.id))
    return render_template("aplicacoes/form.html", form=form, titulo="Nova Avaliação")


@aplicacoes_bp.route("/<int:aplicacao_id>")
@login_required
def ver(aplicacao_id):
    aplicacao = Aplicacao.query.get_or_404(aplicacao_id)
    return render_template(
        "aplicacoes/ver.html",
        aplicacao=aplicacao,
        info_instrumento=_info_instrumento(aplicacao.questionario),
    )


@aplicacoes_bp.route("/<int:aplicacao_id>/editar", methods=["GET", "POST"])
@login_required
def editar(aplicacao_id):
    aplicacao = Aplicacao.query.get_or_404(aplicacao_id)
    form = AplicacaoForm(obj=aplicacao)
    _preencher_empresas(form)
    _preencher_questionarios(form)
    if form.validate_on_submit():
        aplicacao.empresa_id = form.empresa_id.data
        aplicacao.questionario_id = form.questionario_id.data
        aplicacao.titulo = form.titulo.data.strip()
        aplicacao.descricao = form.descricao.data
        aplicacao.data_inicio = form.data_inicio.data
        aplicacao.data_fim = form.data_fim.data
        aplicacao.ativa = form.ativa.data
        aplicacao.multisetorial = form.multisetorial.data
        db.session.commit()
        flash("Avaliação atualizada com sucesso.", "success")
        return redirect(url_for("aplicacoes.ver", aplicacao_id=aplicacao.id))
    return render_template("aplicacoes/form.html", form=form, titulo="Editar Avaliação")


@aplicacoes_bp.route("/<int:aplicacao_id>/alternar-status", methods=["POST"])
@login_required
def alternar_status(aplicacao_id):
    aplicacao = Aplicacao.query.get_or_404(aplicacao_id)
    aplicacao.ativa = not aplicacao.ativa
    db.session.commit()
    flash("Aplicação reaberta." if aplicacao.ativa else "Aplicação encerrada.", "info")
    return redirect(url_for("aplicacoes.listar"))


@aplicacoes_bp.route("/<int:aplicacao_id>/segmentos/novo", methods=["GET", "POST"])
@login_required
def novo_segmento(aplicacao_id):
    aplicacao = Aplicacao.query.get_or_404(aplicacao_id)
    form = SegmentoAplicacaoForm()
    _preencher_setores(form, aplicacao)
    if not form.setor_id.choices:
        flash(
            "Todos os setores cadastrados já foram adicionados a esta avaliação, ou não há "
            "setores cadastrados. Cadastre setores em Setores antes de continuar.",
            "danger",
        )
        return redirect(url_for("aplicacoes.ver", aplicacao_id=aplicacao.id))
    if form.validate_on_submit():
        segmento = SegmentoAplicacao(
            aplicacao_id=aplicacao.id,
            setor_id=form.setor_id.data,
            quantidade_colaboradores=form.quantidade_colaboradores.data,
        )
        db.session.add(segmento)
        db.session.commit()
        flash("Setor adicionado à avaliação.", "success")
        return redirect(url_for("aplicacoes.ver", aplicacao_id=aplicacao.id))
    return render_template(
        "aplicacoes/segmento_form.html", form=form, aplicacao=aplicacao, titulo="Adicionar setor"
    )


@aplicacoes_bp.route("/segmentos/<int:segmento_id>/editar", methods=["GET", "POST"])
@login_required
def editar_segmento(segmento_id):
    segmento = SegmentoAplicacao.query.get_or_404(segmento_id)
    form = SegmentoAplicacaoForm(obj=segmento)
    _preencher_setores(form, segmento.aplicacao, segmento_atual=segmento)
    if form.validate_on_submit():
        segmento.setor_id = form.setor_id.data
        segmento.quantidade_colaboradores = form.quantidade_colaboradores.data
        db.session.commit()
        flash("Setor atualizado.", "success")
        return redirect(url_for("aplicacoes.ver", aplicacao_id=segmento.aplicacao_id))
    return render_template(
        "aplicacoes/segmento_form.html",
        form=form,
        aplicacao=segmento.aplicacao,
        titulo="Editar setor",
    )


@aplicacoes_bp.route("/segmentos/<int:segmento_id>/excluir", methods=["POST"])
@login_required
def excluir_segmento(segmento_id):
    segmento = SegmentoAplicacao.query.get_or_404(segmento_id)
    aplicacao_id = segmento.aplicacao_id
    db.session.delete(segmento)
    db.session.commit()
    flash("Setor removido da avaliação.", "info")
    return redirect(url_for("aplicacoes.ver", aplicacao_id=aplicacao_id))


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

    taxa_por_segmento = []
    for segmento in aplicacao.segmentos:
        respondentes = len(segmento.envios)
        quantidade = segmento.quantidade_colaboradores or 0
        taxa = round((respondentes / quantidade) * 100, 1) if quantidade else None
        taxa_por_segmento.append(
            {
                "setor": segmento.setor.nome,
                "respondentes": respondentes,
                "quantidade_colaboradores": quantidade,
                "taxa": taxa,
            }
        )

    return render_template(
        "aplicacoes/resultados.html",
        aplicacao=aplicacao,
        total_envios=len(aplicacao.envios),
        medias_por_dimensao=medias_por_dimensao,
        planos_acao=planos_acao,
        taxa_por_segmento=taxa_por_segmento,
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
