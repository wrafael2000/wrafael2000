"""Upload/download de arquivos anexados a registros do sistema (ex.: PDF do
PCMSO/PGR em Documentos SST).

Os arquivos ficam numa subpasta 'uploads' dentro da pasta de dados, salvos
com um nome interno aleatório — evita conflito entre arquivos de nomes
iguais enviados em momentos diferentes. O nome original (o que o usuário vê)
fica guardado à parte, no banco de dados.
"""

import os
import uuid

from flask import current_app
from werkzeug.utils import secure_filename

from .armazenamento import pasta_dados

SUBPASTA = "uploads"


def pasta_uploads():
    pasta = os.path.join(pasta_dados(current_app), SUBPASTA)
    os.makedirs(pasta, exist_ok=True)
    return pasta


def salvar_arquivo(arquivo_enviado):
    """Salva um FileStorage (de um FileField) e devolve o nome interno gerado."""
    nome_seguro = secure_filename(arquivo_enviado.filename) or "arquivo"
    extensao = os.path.splitext(nome_seguro)[1]
    nome_armazenado = f"{uuid.uuid4().hex}{extensao}"
    arquivo_enviado.save(os.path.join(pasta_uploads(), nome_armazenado))
    return nome_armazenado


def remover_arquivo(nome_armazenado):
    if not nome_armazenado:
        return
    caminho = os.path.join(pasta_uploads(), nome_armazenado)
    if os.path.exists(caminho):
        os.remove(caminho)
