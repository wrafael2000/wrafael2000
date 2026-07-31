import secrets

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for
from flask_login import current_user, login_required, login_user, logout_user

from ..extensions import db
from ..forms import EsqueciSenhaForm, LoginForm
from ..models import Usuario
from ..recovery import obter_codigo_recuperacao

auth_bp = Blueprint("auth", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = LoginForm()
    if form.validate_on_submit():
        usuario = Usuario.query.filter_by(email=form.email.data.lower().strip()).first()
        if usuario and usuario.checar_senha(form.senha.data):
            login_user(usuario)
            proxima = request.args.get("next")
            return redirect(proxima or url_for("main.dashboard"))
        flash("E-mail ou senha inválidos.", "danger")

    return render_template("login.html", form=form)


@auth_bp.route("/esqueci-senha", methods=["GET", "POST"])
def esqueci_senha():
    if current_user.is_authenticated:
        return redirect(url_for("main.dashboard"))

    form = EsqueciSenhaForm()
    if form.validate_on_submit():
        codigo_valido = obter_codigo_recuperacao(current_app)
        codigo_digitado = form.codigo_recuperacao.data.strip().upper()

        if not codigo_valido or not secrets.compare_digest(codigo_digitado, codigo_valido):
            flash("Código de recuperação inválido.", "danger")
            return render_template("esqueci_senha.html", form=form)

        usuario = Usuario.query.filter_by(email=form.email.data.lower().strip()).first()
        if not usuario:
            flash("Não existe usuário com esse e-mail.", "danger")
            return render_template("esqueci_senha.html", form=form)

        usuario.set_senha(form.nova_senha.data)
        db.session.commit()
        flash("Senha redefinida com sucesso. Faça login com a nova senha.", "success")
        return redirect(url_for("auth.login"))

    return render_template("esqueci_senha.html", form=form)


@auth_bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Você saiu do sistema.", "info")
    return redirect(url_for("auth.login"))
