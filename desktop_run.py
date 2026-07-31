"""Ponto de entrada para a versão "clique e use" (empacotada com PyInstaller).

Diferente de run.py (uso via `flask` / terminal, para quem está aprendendo a
desenvolver), este arquivo é pensado para quem só quer abrir o programa:
gera a chave secreta e o banco de dados automaticamente, cria o primeiro
usuário administrador por perguntas simples no console, e abre o sistema
sozinho no navegador.
"""

import os
import secrets
import sys
import threading
import time
import webbrowser
from getpass import getpass


def pasta_base():
    """Pasta onde o executável (ou este script) está, para guardar os dados ao lado."""
    if getattr(sys, "frozen", False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def preparar_ambiente():
    """Gera SECRET_KEY e aponta o banco de dados para uma pasta 'dados' ao lado do programa."""
    dados_dir = os.path.join(pasta_base(), "dados")
    os.makedirs(dados_dir, exist_ok=True)

    chave_path = os.path.join(dados_dir, "secret.key")
    if not os.path.exists(chave_path):
        with open(chave_path, "w", encoding="utf-8") as arquivo:
            arquivo.write(secrets.token_hex(32))
    with open(chave_path, encoding="utf-8") as arquivo:
        os.environ["SECRET_KEY"] = arquivo.read().strip()

    os.environ["DATABASE_URL"] = "sqlite:///" + os.path.join(dados_dir, "sst.db")


def criar_admin_se_necessario(app):
    from app.extensions import db
    from app.models import Usuario

    with app.app_context():
        if Usuario.query.first():
            return

        print()
        print("=== Primeiro uso: crie o usuário administrador ===")
        nome = input("Nome: ").strip()
        email = input("E-mail: ").strip().lower()
        senha = getpass("Senha: ")

        usuario = Usuario(nome=nome, email=email)
        usuario.set_senha(senha)
        db.session.add(usuario)
        db.session.commit()
        print("Usuário criado com sucesso! Abrindo o sistema...")
        print()


def abrir_navegador(url):
    time.sleep(1.5)
    webbrowser.open(url)


def resetar_senha(app):
    from app.extensions import db
    from app.models import Usuario

    with app.app_context():
        print()
        print("=== Redefinir senha de um usuário ===")
        email = input("E-mail do usuário: ").strip().lower()
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            print(f"\nNenhum usuário encontrado com o e-mail '{email}'.")
            todos = Usuario.query.all()
            if todos:
                print("E-mails cadastrados neste banco de dados:")
                for u in todos:
                    print(f"  - {u.email}")
                print("\nRode de novo com --resetar-senha e digite um desses e-mails.")
            else:
                print("Não há nenhum usuário cadastrado neste banco de dados.")
            return

        senha = getpass("Nova senha: ")
        confirmacao = getpass("Confirme a nova senha: ")
        if senha != confirmacao:
            print("As senhas digitadas não são iguais. Nada foi alterado.")
            return

        usuario.set_senha(senha)
        db.session.commit()
        print(f"Senha do usuário '{email}' redefinida com sucesso.")


def main():
    preparar_ambiente()

    from app import create_app

    app = create_app()

    if "--resetar-senha" in sys.argv:
        resetar_senha(app)
        input("\nPressione Enter para fechar...")
        return

    criar_admin_se_necessario(app)

    url = "http://127.0.0.1:5000"
    threading.Thread(target=abrir_navegador, args=(url,), daemon=True).start()

    print(f"Sistema disponível em {url}")
    print("NÃO FECHE esta janela enquanto estiver usando o sistema.")
    print("Para encerrar, feche esta janela ou pressione Ctrl+C.")
    print()

    app.run(host="127.0.0.1", port=5000, debug=False, use_reloader=False)


if __name__ == "__main__":
    main()
