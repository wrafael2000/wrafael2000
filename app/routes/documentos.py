from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import DocumentoSSTForm
from ..models import DocumentoSST

documentos_bp = Blueprint("documentos", __name__, url_prefix="/documentos")


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
        db.session.commit()
        flash("Documento atualizado com sucesso.", "success")
        return redirect(url_for("documentos.listar"))
    return render_template("documentos/form.html", form=form, titulo="Editar documento")


@documentos_bp.route("/<int:documento_id>/excluir", methods=["POST"])
@login_required
def excluir(documento_id):
    documento = DocumentoSST.query.get_or_404(documento_id)
    db.session.delete(documento)
    db.session.commit()
    flash("Documento removido.", "info")
    return redirect(url_for("documentos.listar"))
