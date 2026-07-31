from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ItemPcmsoForm, PcmsoForm
from ..models import DocumentoSST, ItemPcmso, Pcmso, Setor
from ..relatorios_pdf import gerar_pdf_pcmso
from ..uploads import remover_arquivo, salvar_bytes

pcmso_bp = Blueprint("pcmso", __name__, url_prefix="/pcmso")


def _preencher_setores(form):
    form.setor_id.choices = [(s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()]


@pcmso_bp.route("/")
@login_required
def listar():
    registros = Pcmso.query.order_by(Pcmso.data_elaboracao.desc()).all()
    return render_template("pcmso/listar.html", registros=registros)


@pcmso_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = PcmsoForm()
    if form.validate_on_submit():
        pcmso = Pcmso(
            titulo=form.titulo.data.strip(),
            medico_coordenador=form.medico_coordenador.data.strip(),
            medico_coordenador_crm=form.medico_coordenador_crm.data,
            data_elaboracao=form.data_elaboracao.data,
            data_validade=form.data_validade.data,
            diretrizes=form.diretrizes.data,
        )
        db.session.add(pcmso)
        db.session.commit()
        flash("PCMSO criado com sucesso. Adicione o quadro de funções/riscos/exames abaixo.", "success")
        return redirect(url_for("pcmso.ver", pcmso_id=pcmso.id))
    return render_template("pcmso/form.html", form=form, titulo="Novo PCMSO")


@pcmso_bp.route("/<int:pcmso_id>")
@login_required
def ver(pcmso_id):
    pcmso = Pcmso.query.get_or_404(pcmso_id)
    return render_template("pcmso/ver.html", pcmso=pcmso)


@pcmso_bp.route("/<int:pcmso_id>/editar", methods=["GET", "POST"])
@login_required
def editar(pcmso_id):
    pcmso = Pcmso.query.get_or_404(pcmso_id)
    form = PcmsoForm(obj=pcmso)
    if form.validate_on_submit():
        pcmso.titulo = form.titulo.data.strip()
        pcmso.medico_coordenador = form.medico_coordenador.data.strip()
        pcmso.medico_coordenador_crm = form.medico_coordenador_crm.data
        pcmso.data_elaboracao = form.data_elaboracao.data
        pcmso.data_validade = form.data_validade.data
        pcmso.diretrizes = form.diretrizes.data
        db.session.commit()
        flash("PCMSO atualizado com sucesso.", "success")
        return redirect(url_for("pcmso.ver", pcmso_id=pcmso.id))
    return render_template("pcmso/form.html", form=form, titulo="Editar PCMSO")


@pcmso_bp.route("/<int:pcmso_id>/excluir", methods=["POST"])
@login_required
def excluir(pcmso_id):
    pcmso = Pcmso.query.get_or_404(pcmso_id)
    db.session.delete(pcmso)
    db.session.commit()
    flash("PCMSO removido. O documento já gerado em Documentos SST (se houver) não foi apagado.", "info")
    return redirect(url_for("pcmso.listar"))


@pcmso_bp.route("/<int:pcmso_id>/gerar", methods=["POST"])
@login_required
def gerar(pcmso_id):
    pcmso = Pcmso.query.get_or_404(pcmso_id)
    if not pcmso.itens:
        flash("Adicione ao menos um item de função/risco/exame antes de gerar o PDF.", "danger")
        return redirect(url_for("pcmso.ver", pcmso_id=pcmso.id))

    pdf_buffer = gerar_pdf_pcmso(pcmso)
    nome_arquivo = f"pcmso-{pcmso.id}.pdf"

    documento = pcmso.documento
    if documento is None:
        documento = DocumentoSST(tipo="PCMSO")
        pcmso.documento = documento
        db.session.add(documento)
    else:
        remover_arquivo(documento.arquivo_nome_armazenado)

    documento.nome = pcmso.titulo
    documento.data_emissao = pcmso.data_elaboracao
    documento.data_validade = pcmso.data_validade
    documento.responsavel_tecnico = pcmso.medico_coordenador
    documento.observacao = f"Gerado automaticamente a partir do PCMSO #{pcmso.id} pelo sistema."
    documento.arquivo_nome_original = nome_arquivo
    documento.arquivo_nome_armazenado = salvar_bytes(pdf_buffer.getvalue(), nome_arquivo)

    db.session.commit()
    flash("PDF do PCMSO gerado e salvo em Documentos SST.", "success")
    return redirect(url_for("pcmso.ver", pcmso_id=pcmso.id))


@pcmso_bp.route("/<int:pcmso_id>/itens/novo", methods=["GET", "POST"])
@login_required
def novo_item(pcmso_id):
    pcmso = Pcmso.query.get_or_404(pcmso_id)
    form = ItemPcmsoForm()
    _preencher_setores(form)
    if form.validate_on_submit():
        item = ItemPcmso(
            pcmso_id=pcmso.id,
            setor_id=form.setor_id.data,
            funcao=form.funcao.data.strip(),
            riscos_ocupacionais=form.riscos_ocupacionais.data,
            exames_indicados=form.exames_indicados.data,
            periodicidade_meses=form.periodicidade_meses.data,
            observacoes=form.observacoes.data,
        )
        db.session.add(item)
        db.session.commit()
        flash("Item adicionado com sucesso.", "success")
        return redirect(url_for("pcmso.ver", pcmso_id=pcmso.id))
    return render_template("pcmso/item_form.html", form=form, pcmso=pcmso, titulo="Novo item")


@pcmso_bp.route("/itens/<int:item_id>/editar", methods=["GET", "POST"])
@login_required
def editar_item(item_id):
    item = ItemPcmso.query.get_or_404(item_id)
    form = ItemPcmsoForm(obj=item)
    _preencher_setores(form)
    if form.validate_on_submit():
        item.setor_id = form.setor_id.data
        item.funcao = form.funcao.data.strip()
        item.riscos_ocupacionais = form.riscos_ocupacionais.data
        item.exames_indicados = form.exames_indicados.data
        item.periodicidade_meses = form.periodicidade_meses.data
        item.observacoes = form.observacoes.data
        db.session.commit()
        flash("Item atualizado com sucesso.", "success")
        return redirect(url_for("pcmso.ver", pcmso_id=item.pcmso_id))
    return render_template(
        "pcmso/item_form.html", form=form, pcmso=item.pcmso, titulo="Editar item"
    )


@pcmso_bp.route("/itens/<int:item_id>/excluir", methods=["POST"])
@login_required
def excluir_item(item_id):
    item = ItemPcmso.query.get_or_404(item_id)
    pcmso_id = item.pcmso_id
    db.session.delete(item)
    db.session.commit()
    flash("Item removido.", "info")
    return redirect(url_for("pcmso.ver", pcmso_id=pcmso_id))
