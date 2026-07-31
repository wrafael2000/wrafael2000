"""Localização da pasta de dados (onde ficam o banco SQLite e arquivos
relacionados: código de recuperação, anexos enviados pelo usuário etc.)."""

import os


def pasta_dados(app):
    uri = app.config["SQLALCHEMY_DATABASE_URI"]
    prefixo = "sqlite:///"
    if not uri.startswith(prefixo):
        return app.instance_path
    caminho_banco = uri[len(prefixo):]
    return os.path.dirname(os.path.abspath(caminho_banco))
