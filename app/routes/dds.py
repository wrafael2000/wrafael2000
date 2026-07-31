from flask import Blueprint, flash, redirect, render_template, send_file, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import DDSForm
from ..models import DDS, Funcionario, Setor
from ..relatorios_pdf import gerar_pdf_dds

dds_bp = Blueprint("dds", __name__, url_prefix="/dds")


def _preencher_selects(form):
    form.setor_id.choices = [(s.id, s.nome) for s in Setor.query.order_by(Setor.nome).all()]
    form.participantes.choices = [
        (f.id, f.nome) for f in Funcionario.query.filter_by(ativo=True).order_by(Funcionario.nome).all()
    ]


@dds_bp.route("/")
@login_required
def listar():
    registros = DDS.query.order_by(DDS.data.desc()).all()
    return render_template("dds/listar.html", registros=registros)


@dds_bp.route("/novo", methods=["GET", "POST"])
@login_required
def novo():
    form = DDSForm()
    _preencher_selects(form)
    if form.validate_on_submit():
        registro = DDS(
            data=form.data.data,
            setor_id=form.setor_id.data,
            tema=form.tema.data.strip(),
            responsavel=form.responsavel.data.strip(),
            conteudo=form.conteudo.data,
        )
        registro.participantes = Funcionario.query.filter(
            Funcionario.id.in_(form.participantes.data)
        ).all()
        db.session.add(registro)
        db.session.commit()
        flash("DDS registrado com sucesso.", "success")
        return redirect(url_for("dds.listar"))
    return render_template("dds/form.html", form=form, titulo="Novo DDS")


@dds_bp.route("/<int:dds_id>/editar", methods=["GET", "POST"])
@login_required
def editar(dds_id):
    registro = DDS.query.get_or_404(dds_id)
    # Não usamos obj=registro: "participantes" no banco é uma lista de objetos
    # Funcionario, e o SelectMultipleField (coerce=int) espera uma lista de IDs.
    form = DDSForm()
    _preencher_selects(form)
    if form.validate_on_submit():
        registro.data = form.data.data
        registro.setor_id = form.setor_id.data
        registro.tema = form.tema.data.strip()
        registro.responsavel = form.responsavel.data.strip()
        registro.conteudo = form.conteudo.data
        registro.participantes = Funcionario.query.filter(
            Funcionario.id.in_(form.participantes.data)
        ).all()
        db.session.commit()
        flash("DDS atualizado com sucesso.", "success")
        return redirect(url_for("dds.listar"))
    elif not form.is_submitted():
        form.data.data = registro.data
        form.setor_id.data = registro.setor_id
        form.tema.data = registro.tema
        form.responsavel.data = registro.responsavel
        form.conteudo.data = registro.conteudo
        form.participantes.data = [f.id for f in registro.participantes]
    return render_template("dds/form.html", form=form, titulo="Editar DDS")


@dds_bp.route("/<int:dds_id>/excluir", methods=["POST"])
@login_required
def excluir(dds_id):
    registro = DDS.query.get_or_404(dds_id)
    db.session.delete(registro)
    db.session.commit()
    flash("DDS removido.", "info")
    return redirect(url_for("dds.listar"))


@dds_bp.route("/<int:dds_id>/pdf")
@login_required
def pdf(dds_id):
    registro = DDS.query.get_or_404(dds_id)
    pdf_buffer = gerar_pdf_dds(registro)
    return send_file(
        pdf_buffer,
        mimetype="application/pdf",
        as_attachment=True,
        download_name=f"dds-{registro.data.isoformat()}.pdf",
    )
