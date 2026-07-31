import click

from .extensions import db
from .models import Usuario
from .seed_data import seed_normas_regulamentadoras, seed_questionarios


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

    @app.cli.command("seed-questionarios")
    def seed_questionarios_command():
        """Cria os questionários padrão (HSE-IT, COPSOQ II, CBI, Clima)."""
        criados = seed_questionarios()
        if criados:
            click.echo(f"Questionários criados: {', '.join(criados)}")
        else:
            click.echo("Nenhum questionário novo (todos já existiam).")

    @app.cli.command("seed-normas")
    def seed_normas_command():
        """Cria o catálogo padrão de Normas Regulamentadoras (NR-1 a NR-38)."""
        criadas = seed_normas_regulamentadoras()
        if criadas:
            click.echo(f"Normas criadas: {', '.join(criadas)}")
        else:
            click.echo("Nenhuma norma nova (todas já existiam).")
