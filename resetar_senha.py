"""Utilitário de emergência: redefine a senha de um usuário administrador
diretamente no banco de dados, sem apagar nenhum outro dado do sistema.

Uso (Windows, na pasta do projeto, depois de já ter rodado build_windows.bat
pelo menos uma vez — para ter o ambiente com as dependências instaladas):

    .venv_build\\Scripts\\python.exe resetar_senha.py

O script tenta localizar sozinho o arquivo dados\\sst.db (ele pode estar em
'dados\\' ao lado deste script ou em 'dist\\dados\\', dependendo de onde o
executável foi rodado). Se não encontrar, pergunta o caminho.
"""

import os
import sys
from getpass import getpass

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def localizar_banco():
    candidatos = [
        os.path.join(SCRIPT_DIR, "dados", "sst.db"),
        os.path.join(SCRIPT_DIR, "dist", "dados", "sst.db"),
        os.path.join(SCRIPT_DIR, "..", "dados", "sst.db"),
    ]
    for caminho in candidatos:
        if os.path.exists(caminho):
            return os.path.abspath(caminho)

    print("Não encontrei o banco de dados automaticamente. Locais tentados:")
    for caminho in candidatos:
        print(f"  - {os.path.abspath(caminho)}")
    print()
    digitado = input(
        "Digite o caminho completo do arquivo sst.db (ou deixe em branco para cancelar): "
    ).strip()
    if not digitado:
        return None
    return digitado if os.path.exists(digitado) else None


def main():
    caminho_banco = localizar_banco()
    if not caminho_banco:
        print("Banco de dados não encontrado. Nada foi alterado.")
        sys.exit(1)

    print(f"Usando banco de dados: {caminho_banco}\n")

    os.environ["SECRET_KEY"] = "temporaria-apenas-para-resetar-senha"
    os.environ["DATABASE_URL"] = "sqlite:///" + caminho_banco

    from app import create_app
    from app.extensions import db
    from app.models import Usuario

    app = create_app()
    with app.app_context():
        email = input("E-mail do usuário: ").strip().lower()
        usuario = Usuario.query.filter_by(email=email).first()
        if not usuario:
            print(f"Nenhum usuário encontrado com o e-mail '{email}'.")
            sys.exit(1)

        senha = getpass("Nova senha: ")
        confirmacao = getpass("Confirme a nova senha: ")
        if senha != confirmacao:
            print("As senhas digitadas não são iguais. Nada foi alterado.")
            sys.exit(1)

        usuario.set_senha(senha)
        db.session.commit()
        print(f"\nSenha do usuário '{email}' redefinida com sucesso.")


if __name__ == "__main__":
    main()
