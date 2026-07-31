from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ItemRiscoPgrForm, PgrForm
from ..models import DocumentoSST, ItemRiscoPgr, Pgr, Setor
from ..relatorios_pdf import gerar_pdf_pgr
from ..uploads import remover_arquivo, salvar_bytes

pgr_bp = Blueprint("pgr", __name__, url_prefix="/pgr")


def _preencher_setores(form):
    form.setor_id.choices = [(s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()]


@pgr_bp.route("/")
@login_required
def listar():
    registros = Pgr.query.order_by(Pgr.data_elaboracao.desc()).all()
    return render_template("pgr/listar.html", registros=registros)


@pgr_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = PgrForm()
    if form.validate_on_submit():
        pgr = Pgr(
            titulo=form.titulo.data.strip(),
            responsavel_tecnico=form.responsavel_tecnico.data.strip(),
            responsavel_tecnico_registro=form.responsavel_tecnico_registro.data,
            data_elaboracao=form.data_elaboracao.data,
            data_validade=form.data_validade.data,
            introducao=form.introducao.data,
        )
        db.session.add(pgr)
        db.session.commit()
        flash("PGR criado com sucesso. Adicione o inventário de riscos abaixo.", "success")
        return redirect(url_for("pgr.ver", pgr_id=pgr.id))
    return render_template("pgr/form.html", form=form, titulo="Novo PGR")


@pgr_bp.route("/<int:pgr_id>")
@login_required
def ver(pgr_id):
    pgr = Pgr.query.get_or_404(pgr_id)
    return render_template("pgr/ver.html", pgr=pgr)


@pgr_bp.route("/<int:pgr_id>/editar", methods=["GET", "POST"])
@login_required
def editar(pgr_id):
    pgr = Pgr.query.get_or_404(pgr_id)
    form = PgrForm(obj=pgr)
    if form.validate_on_submit():
        pgr.titulo = form.titulo.data.strip()
        pgr.responsavel_tecnico = form.responsavel_tecnico.data.strip()
        pgr.responsavel_tecnico_registro = form.responsavel_tecnico_registro.data
        pgr.data_elaboracao = form.data_elaboracao.data
        pgr.data_validade = form.data_validade.data
        pgr.introducao = form.introducao.data
        db.session.commit()
        flash("PGR atualizado com sucesso.", "success")
        return redirect(url_for("pgr.ver", pgr_id=pgr.id))
    return render_template("pgr/form.html", form=form, titulo="Editar PGR")


@pgr_bp.route("/<int:pgr_id>/excluir", methods=["POST"])
@login_required
def excluir(pgr_id):
    pgr = Pgr.query.get_or_404(pgr_id)
    db.session.delete(pgr)
    db.session.commit()
    flash("PGR removido. O documento já gerado em Documentos SST (se houver) não foi apagado.", "info")
    return redirect(url_for("pgr.listar"))


@pgr_bp.route("/<int:pgr_id>/gerar", methods=["POST"])
@login_required
def gerar(pgr_id):
    pgr = Pgr.query.get_or_404(pgr_id)
    if not pgr.itens:
        flash("Adicione ao menos um item de risco antes de gerar o PDF.", "danger")
        return redirect(url_for("pgr.ver", pgr_id=pgr.id))

    pdf_buffer = gerar_pdf_pgr(pgr)
    nome_arquivo = f"pgr-{pgr.id}.pdf"

    documento = pgr.documento
    if documento is None:
        documento = DocumentoSST(tipo="PGR")
        pgr.documento = documento
        db.session.add(documento)
    else:
        remover_arquivo(documento.arquivo_nome_armazenado)

    documento.nome = pgr.titulo
    documento.data_emissao = pgr.data_elaboracao
    documento.data_validade = pgr.data_validade
    documento.responsavel_tecnico = pgr.responsavel_tecnico
    documento.observacao = f"Gerado automaticamente a partir do PGR #{pgr.id} pelo sistema."
    documento.arquivo_nome_original = nome_arquivo
    documento.arquivo_nome_armazenado = salvar_bytes(pdf_buffer.getvalue(), nome_arquivo)

    db.session.commit()
    flash("PDF do PGR gerado e salvo em Documentos SST.", "success")
    return redirect(url_for("pgr.ver", pgr_id=pgr.id))


@pgr_bp.route("/<int:pgr_id>/itens/novo", methods=["GET", "POST"])
@login_required
def novo_item(pgr_id):
    pgr = Pgr.query.get_or_404(pgr_id)
    form = ItemRiscoPgrForm()
    _preencher_setores(form)
    if form.validate_on_submit():
        item = ItemRiscoPgr(
            pgr_id=pgr.id,
            setor_id=form.setor_id.data,
            funcao_atividade=form.funcao_atividade.data,
            categoria_risco=form.categoria_risco.data,
            perigo_fator_risco=form.perigo_fator_risco.data,
            fonte_geradora=form.fonte_geradora.data,
            medidas_existentes=form.medidas_existentes.data,
            nivel_risco=form.nivel_risco.data,
            medidas_recomendadas=form.medidas_recomendadas.data,
            prazo=form.prazo.data,
            responsavel_acao=form.responsavel_acao.data,
            status=form.status.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Item de risco adicionado com sucesso.", "success")
        return redirect(url_for("pgr.ver", pgr_id=pgr.id))
    return render_template("pgr/item_form.html", form=form, pgr=pgr, titulo="Novo item de risco")


@pgr_bp.route("/itens/<int:item_id>/editar", methods=["GET", "POST"])
@login_required
def editar_item(item_id):
    item = ItemRiscoPgr.query.get_or_404(item_id)
    form = ItemRiscoPgrForm(obj=item)
    _preencher_setores(form)
    if form.validate_on_submit():
        item.setor_id = form.setor_id.data
        item.funcao_atividade = form.funcao_atividade.data
        item.categoria_risco = form.categoria_risco.data
        item.perigo_fator_risco = form.perigo_fator_risco.data
        item.fonte_geradora = form.fonte_geradora.data
        item.medidas_existentes = form.medidas_existentes.data
        item.nivel_risco = form.nivel_risco.data
        item.medidas_recomendadas = form.medidas_recomendadas.data
        item.prazo = form.prazo.data
        item.responsavel_acao = form.responsavel_acao.data
        item.status = form.status.data
        db.session.commit()
        flash("Item de risco atualizado com sucesso.", "success")
        return redirect(url_for("pgr.ver", pgr_id=item.pgr_id))
    return render_template(
        "pgr/item_form.html", form=form, pgr=item.pgr, titulo="Editar item de risco"
    )


@pgr_bp.route("/itens/<int:item_id>/excluir", methods=["POST"])
@login_required
def excluir_item(item_id):
    item = ItemRiscoPgr.query.get_or_404(item_id)
    pgr_id = item.pgr_id
    db.session.delete(item)
    db.session.commit()
    flash("Item de risco removido.", "info")
    return redirect(url_for("pgr.ver", pgr_id=pgr_id))
