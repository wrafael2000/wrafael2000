"""Migração leve para bancos SQLite já existentes.

O projeto não usa Flask-Migrate/Alembic de propósito — para não exigir mais
um comando de terminal de quem só quer abrir o programa. Quando um model
ganha uma coluna nova, ela é listada aqui; na inicialização, o sistema
confere se a coluna já existe na tabela e, se não existir, adiciona com
ALTER TABLE, sem apagar nenhuma linha existente.
"""

from sqlalchemy import inspect, text

COLUNAS_NOVAS = {
    "documentos_sst": [
        ("arquivo_nome_original", "VARCHAR(255)"),
        ("arquivo_nome_armazenado", "VARCHAR(255)"),
    ],
    "aplicacoes": [
        ("descricao", "TEXT"),
        ("multisetorial", "BOOLEAN DEFAULT 0 NOT NULL"),
        ("empresa_id", "INTEGER REFERENCES empresa(id)"),
    ],
}


def aplicar_migracoes_leves(db):
    inspetor = inspect(db.engine)
    tabelas_existentes = set(inspetor.get_table_names())

    for tabela, colunas in COLUNAS_NOVAS.items():
        if tabela not in tabelas_existentes:
            continue  # tabela nova: db.create_all() já cria com as colunas certas

        colunas_atuais = {c["name"] for c in inspetor.get_columns(tabela)}
        for nome_coluna, tipo_sql in colunas:
            if nome_coluna in colunas_atuais:
                continue
            with db.engine.begin() as conexao:
                conexao.execute(
                    text(f"ALTER TABLE {tabela} ADD COLUMN {nome_coluna} {tipo_sql}")
                )
