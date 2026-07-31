from flask import Blueprint, abort, flash, redirect, render_template, send_from_directory, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import DocumentoSSTForm
from ..models import DocumentoSST
from ..uploads import pasta_uploads, remover_arquivo, salvar_arquivo

documentos_bp = Blueprint("documentos", __name__, url_prefix="/documentos")


def _processar_arquivo(form, documento):
    arquivo_enviado = form.arquivo.data
    if not arquivo_enviado or not getattr(arquivo_enviado, "filename", ""):
        return

    if documento.arquivo_nome_armazenado:
        remover_arquivo(documento.arquivo_nome_armazenado)

    documento.arquivo_nome_original = arquivo_enviado.filename
    documento.arquivo_nome_armazenado = salvar_arquivo(arquivo_enviado)


@documentos_bp.route("/")
@login_required
def listar():
    documentos = DocumentoSST.query.order_by(DocumentoSST.data_emissao.desc()).all()
    return render_template("documentos/listar.html", documentos=documentos)


@documentos_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = DocumentoSSTForm()
    if form.validate_on_submit():
        documento = DocumentoSST(
            tipo=form.tipo.data,
            nome=form.nome.data.strip(),
            data_emissao=form.data_emissao.data,
            data_validade=form.data_validade.data,
            responsavel_tecnico=form.responsavel_tecnico.data,
            observacao=form.observacao.data,
        )
        _processar_arquivo(form, documento)
        db.session.add(documento)
        db.session.commit()
        flash("Documento cadastrado com sucesso.", "success")
        return redirect(url_for("documentos.listar"))
    return render_template("documentos/form.html", form=form, titulo="Novo documento")


@documentos_bp.route("/<int:documento_id>/editar", methods=["GET", "POST"])
@login_required
def editar(documento_id):
    documento = DocumentoSST.query.get_or_404(documento_id)
    form = DocumentoSSTForm(obj=documento)
    if form.validate_on_submit():
        documento.tipo = form.tipo.data
        documento.nome = form.nome.data.strip()
        documento.data_emissao = form.data_emissao.data
        documento.data_validade = form.data_validade.data
        documento.responsavel_tecnico = form.responsavel_tecnico.data
        documento.observacao = form.observacao.data
        _processar_arquivo(form, documento)
        db.session.commit()
        flash("Documento atualizado com sucesso.", "success")
        return redirect(url_for("documentos.listar"))
    return render_template("documentos/form.html", form=form, titulo="Editar documento")


@documentos_bp.route("/<int:documento_id>/excluir", methods=["POST"])
@login_required
def excluir(documento_id):
    documento = DocumentoSST.query.get_or_404(documento_id)
    remover_arquivo(documento.arquivo_nome_armazenado)
    db.session.delete(documento)
    db.session.commit()
    flash("Documento removido.", "info")
    return redirect(url_for("documentos.listar"))


@documentos_bp.route("/<int:documento_id>/arquivo")
@login_required
def baixar_arquivo(documento_id):
    documento = DocumentoSST.query.get_or_404(documento_id)
    if not documento.tem_arquivo:
        abort(404)
    return send_from_directory(
        pasta_uploads(),
        documento.arquivo_nome_armazenado,
        as_attachment=True,
        download_name=documento.arquivo_nome_original,
    )
