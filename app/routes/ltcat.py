from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ItemLtcatForm, LtcatForm
from ..models import DocumentoSST, ItemLtcat, Ltcat, Setor
from ..relatorios_pdf import gerar_pdf_ltcat
from ..uploads import remover_arquivo, salvar_bytes

ltcat_bp = Blueprint("ltcat", __name__, url_prefix="/ltcat")


def _preencher_setores(form):
    form.setor_id.choices = [(s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()]


@ltcat_bp.route("/")
@login_required
def listar():
    registros = Ltcat.query.order_by(Ltcat.data_elaboracao.desc()).all()
    return render_template("ltcat/listar.html", registros=registros)


@ltcat_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = LtcatForm()
    if form.validate_on_submit():
        ltcat = Ltcat(
            titulo=form.titulo.data.strip(),
            responsavel_tecnico=form.responsavel_tecnico.data.strip(),
            responsavel_tecnico_registro=form.responsavel_tecnico_registro.data,
            data_elaboracao=form.data_elaboracao.data,
            data_validade=form.data_validade.data,
            metodologia=form.metodologia.data,
        )
        db.session.add(ltcat)
        db.session.commit()
        flash("LTCAT criado com sucesso. Adicione os agentes nocivos avaliados abaixo.", "success")
        return redirect(url_for("ltcat.ver", ltcat_id=ltcat.id))
    return render_template("ltcat/form.html", form=form, titulo="Novo LTCAT")


@ltcat_bp.route("/<int:ltcat_id>")
@login_required
def ver(ltcat_id):
    ltcat = Ltcat.query.get_or_404(ltcat_id)
    return render_template("ltcat/ver.html", ltcat=ltcat)


@ltcat_bp.route("/<int:ltcat_id>/editar", methods=["GET", "POST"])
@login_required
def editar(ltcat_id):
    ltcat = Ltcat.query.get_or_404(ltcat_id)
    form = LtcatForm(obj=ltcat)
    if form.validate_on_submit():
        ltcat.titulo = form.titulo.data.strip()
        ltcat.responsavel_tecnico = form.responsavel_tecnico.data.strip()
        ltcat.responsavel_tecnico_registro = form.responsavel_tecnico_registro.data
        ltcat.data_elaboracao = form.data_elaboracao.data
        ltcat.data_validade = form.data_validade.data
        ltcat.metodologia = form.metodologia.data
        db.session.commit()
        flash("LTCAT atualizado com sucesso.", "success")
        return redirect(url_for("ltcat.ver", ltcat_id=ltcat.id))
    return render_template("ltcat/form.html", form=form, titulo="Editar LTCAT")


@ltcat_bp.route("/<int:ltcat_id>/excluir", methods=["POST"])
@login_required
def excluir(ltcat_id):
    ltcat = Ltcat.query.get_or_404(ltcat_id)
    db.session.delete(ltcat)
    db.session.commit()
    flash("LTCAT removido. O documento já gerado em Documentos SST (se houver) não foi apagado.", "info")
    return redirect(url_for("ltcat.listar"))


@ltcat_bp.route("/<int:ltcat_id>/gerar", methods=["POST"])
@login_required
def gerar(ltcat_id):
    ltcat = Ltcat.query.get_or_404(ltcat_id)
    if not ltcat.itens:
        flash("Adicione ao menos um agente nocivo avaliado antes de gerar o PDF.", "danger")
        return redirect(url_for("ltcat.ver", ltcat_id=ltcat.id))

    pdf_buffer = gerar_pdf_ltcat(ltcat)
    nome_arquivo = f"ltcat-{ltcat.id}.pdf"

    documento = ltcat.documento
    if documento is None:
        documento = DocumentoSST(tipo="LTCAT")
        ltcat.documento = documento
        db.session.add(documento)
    else:
        remover_arquivo(documento.arquivo_nome_armazenado)

    documento.nome = ltcat.titulo
    documento.data_emissao = ltcat.data_elaboracao
    documento.data_validade = ltcat.data_validade
    documento.responsavel_tecnico = ltcat.responsavel_tecnico
    documento.observacao = f"Gerado automaticamente a partir do LTCAT #{ltcat.id} pelo sistema."
    documento.arquivo_nome_original = nome_arquivo
    documento.arquivo_nome_armazenado = salvar_bytes(pdf_buffer.getvalue(), nome_arquivo)

    db.session.commit()
    flash("PDF do LTCAT gerado e salvo em Documentos SST.", "success")
    return redirect(url_for("ltcat.ver", ltcat_id=ltcat.id))


@ltcat_bp.route("/<int:ltcat_id>/itens/novo", methods=["GET", "POST"])
@login_required
def novo_item(ltcat_id):
    ltcat = Ltcat.query.get_or_404(ltcat_id)
    form = ItemLtcatForm()
    _preencher_setores(form)
    if form.validate_on_submit():
        item = ItemLtcat(
            ltcat_id=ltcat.id,
            setor_id=form.setor_id.data,
            funcao=form.funcao.data.strip(),
            tipo_agente=form.tipo_agente.data,
            agente_nocivo=form.agente_nocivo.data,
            intensidade_concentracao=form.intensidade_concentracao.data,
            limite_tolerancia=form.limite_tolerancia.data,
            tecnica_utilizada=form.tecnica_utilizada.data,
            epi_epc_eficaz=form.epi_epc_eficaz.data,
            conclusao=form.conclusao.data,
            observacoes=form.observacoes.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Agente nocivo adicionado com sucesso.", "success")
        return redirect(url_for("ltcat.ver", ltcat_id=ltcat.id))
    return render_template("ltcat/item_form.html", form=form, ltcat=ltcat, titulo="Novo agente nocivo")


@ltcat_bp.route("/itens/<int:item_id>/editar", methods=["GET", "POST"])
@login_required
def editar_item(item_id):
    item = ItemLtcat.query.get_or_404(item_id)
    form = ItemLtcatForm(obj=item)
    _preencher_setores(form)
    if form.validate_on_submit():
        item.setor_id = form.setor_id.data
        item.funcao = form.funcao.data.strip()
        item.tipo_agente = form.tipo_agente.data
        item.agente_nocivo = form.agente_nocivo.data
        item.intensidade_concentracao = form.intensidade_concentracao.data
        item.limite_tolerancia = form.limite_tolerancia.data
        item.tecnica_utilizada = form.tecnica_utilizada.data
        item.epi_epc_eficaz = form.epi_epc_eficaz.data
        item.conclusao = form.conclusao.data
        item.observacoes = form.observacoes.data
        db.session.commit()
        flash("Agente nocivo atualizado com sucesso.", "success")
        return redirect(url_for("ltcat.ver", ltcat_id=item.ltcat_id))
    return render_template(
        "ltcat/item_form.html", form=form, ltcat=item.ltcat, titulo="Editar agente nocivo"
    )


@ltcat_bp.route("/itens/<int:item_id>/excluir", methods=["POST"])
@login_required
def excluir_item(item_id):
    item = ItemLtcat.query.get_or_404(item_id)
    ltcat_id = item.ltcat_id
    db.session.delete(item)
    db.session.commit()
    flash("Agente nocivo removido.", "info")
    return redirect(url_for("ltcat.ver", ltcat_id=ltcat_id))
