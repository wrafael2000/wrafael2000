import click

from .extensions import db
from .models import Usuario


def registrar_comandos(app):
    @app.cli.command("create-admin")
    @click.option("--nome", prompt="Nome")
    @click.option("--email", prompt="E-mail")
    @click.option("--senha", prompt="Senha", hide_input=True, confirmation_prompt=True)
    def create_admin(nome, email, senha):
        """Cria o primeiro usuário administrador do sistema."""
        email = email.lower().strip()
        if Usuario.query.filter_by(email=email).first():
            click.echo(f"Já existe um usuário com o e-mail {email}.")
            return

        usuario = Usuario(nome=nome, email=email)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        click.echo(f"Usuário administrador '{email}' criado com sucesso.")
