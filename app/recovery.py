"""Código de recuperação de senha.

Gerado uma única vez e salvo em um arquivo de texto ao lado do banco de
dados, para permitir redefinir a senha pela própria tela de login, sem
precisar configurar envio de e-mail. Quem tem acesso a esse arquivo já tem
acesso ao computador onde o sistema roda — o mesmo nível de acesso que já
permitiria usar os utilitários resetar_senha.py / --resetar-senha.
"""

import os
import secrets
import string

from .armazenamento import pasta_dados

NOME_ARQUIVO = "codigo_recuperacao.txt"
# Sem O/0/I/1 para evitar confusão ao digitar o código.
ALFABETO = "ABCDEFGHJKLMNPQRSTUVWXYZ23456789"


def garantir_codigo_recuperacao(app):
    pasta = pasta_dados(app)
    os.makedirs(pasta, exist_ok=True)
    caminho = os.path.join(pasta, NOME_ARQUIVO)

    if not os.path.exists(caminho):
        codigo = "".join(secrets.choice(ALFABETO) for _ in range(8))
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(codigo)

    app.config["CAMINHO_CODIGO_RECUPERACAO"] = caminho


def obter_codigo_recuperacao(app):
    caminho = app.config.get("CAMINHO_CODIGO_RECUPERACAO")
    if not caminho or not os.path.exists(caminho):
        return None
    with open(caminho, encoding="utf-8") as arquivo:
        return arquivo.read().strip()
