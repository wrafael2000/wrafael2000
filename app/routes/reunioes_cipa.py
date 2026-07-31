from flask import Blueprint, flash, redirect, render_template, url_for
from flask_login import login_required

from ..extensions import db
from ..forms import ReuniaoCipaForm
from ..models import MandatoCipa, MembroCipa, ReuniaoCipa

reunioes_cipa_bp = Blueprint("reunioes_cipa", __name__, url_prefix="/reunioes-cipa")


def _preencher_selects(form):
    form.mandato_id.choices = [
        (m.id, f"{m.data_inicio.strftime('%d/%m/%Y')} a {m.data_fim.strftime('%d/%m/%Y')}")
        for m in MandatoCipa.query.order_by(MandatoCipa.data_inicio.desc()).all()
    ]
    form.presentes.choices = [
        (m.id, f"{m.funcionario.nome} ({m.cargo})")
        for m in MembroCipa.query.join(MembroCipa.funcionario).order_by(MembroCipa.cargo).all()
    ]


@reunioes_cipa_bp.route("/")
@login_required
def listar():
    reunioes = ReuniaoCipa.query.order_by(ReuniaoCipa.data.desc()).all()
    return render_template("reunioes_cipa/listar.html", reunioes=reunioes)


@reunioes_cipa_bp.route("/<int:reuniao_id>")
@login_required
def ver(reuniao_id):
    reuniao = ReuniaoCipa.query.get_or_404(reuniao_id)
    return render_template("reunioes_cipa/ver.html", reuniao=reuniao)


@reunioes_cipa_bp.route("/nova", methods=["GET", "POST"])
@login_required
def nova():
    form = ReuniaoCipaForm()
    _preencher_selects(form)
    if form.validate_on_submit():
        reuniao = ReuniaoCipa(
            mandato_id=form.mandato_id.data,
            data=form.data.data,
            tipo=form.tipo.data,
            pauta=form.pauta.data,
            ata=form.ata.data,
        )
        reuniao.presentes = MembroCipa.query.filter(MembroCipa.id.in_(form.presentes.data)).all()
        db.session.add(reuniao)
        db.session.commit()
        flash("Ata registrada com sucesso.", "success")
        return redirect(url_for("reunioes_cipa.ver", reuniao_id=reuniao.id))
    return render_template("reunioes_cipa/form.html", form=form, titulo="Nova reunião da CIPA")


@reunioes_cipa_bp.route("/<int:reuniao_id>/editar", methods=["GET", "POST"])
@login_required
def editar(reuniao_id):
    reuniao = ReuniaoCipa.query.get_or_404(reuniao_id)
    # Não usamos obj=reuniao aqui: "presentes" no banco é uma lista de objetos
    # MembroCipa, e o SelectMultipleField (coerce=int) espera uma lista de IDs.
    form = ReuniaoCipaForm()
    _preencher_selects(form)
    if form.validate_on_submit():
        reuniao.mandato_id = form.mandato_id.data
        reuniao.data = form.data.data
        reuniao.tipo = form.tipo.data
        reuniao.pauta = form.pauta.data
        reuniao.ata = form.ata.data
        reuniao.presentes = MembroCipa.query.filter(MembroCipa.id.in_(form.presentes.data)).all()
        db.session.commit()
        flash("Ata atualizada com sucesso.", "success")
        return redirect(url_for("reunioes_cipa.ver", reuniao_id=reuniao.id))
    elif not form.is_submitted():
        form.mandato_id.data = reuniao.mandato_id
        form.data.data = reuniao.data
        form.tipo.data = reuniao.tipo
        form.pauta.data = reuniao.pauta
        form.ata.data = reuniao.ata
        form.presentes.data = [m.id for m in reuniao.presentes]
    return render_template("reunioes_cipa/form.html", form=form, titulo="Editar reunião da CIPA")


@reunioes_cipa_bp.route("/<int:reuniao_id>/excluir", methods=["POST"])
@login_required
def excluir(reuniao_id):
    reuniao = ReuniaoCipa.query.get_or_404(reuniao_id)
    db.session.delete(reuniao)
    db.session.commit()
    flash("Ata removida.", "info")
    return redirect(url_for("reunioes_cipa.listar"))
