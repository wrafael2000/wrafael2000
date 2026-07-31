"""Funções de agregação de dados usadas tanto pelo dashboard quanto pelos PDFs."""

from collections import Counter
from datetime import date, timedelta

from .models import (
    Acidente,
    DocumentoSST,
    EntregaEpi,
    Exame,
    Funcionario,
    PlanoAcaoPsicossocial,
    RealizacaoTreinamento,
    Setor,
)


def coletar_alertas_vencimento():
    """Reúne EPIs, exames, documentos e treinamentos vencidos ou vencendo."""
    alertas = []

    for entrega in EntregaEpi.query.all():
        if entrega.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": "EPI",
                    "descricao": f"{entrega.epi.nome} — {entrega.funcionario.nome}",
                    "vencimento": entrega.data_validade,
                    "status": entrega.status,
                }
            )

    for exame in Exame.query.all():
        if exame.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": "Exame (ASO)",
                    "descricao": f"{exame.tipo} — {exame.funcionario.nome}",
                    "vencimento": exame.data_validade,
                    "status": exame.status,
                }
            )

    for documento in DocumentoSST.query.all():
        if documento.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": documento.tipo,
                    "descricao": documento.nome,
                    "vencimento": documento.data_validade,
                    "status": documento.status,
                }
            )

    for realizacao in RealizacaoTreinamento.query.all():
        if realizacao.status in ("vencido", "vencendo"):
            alertas.append(
                {
                    "tipo": "Treinamento",
                    "descricao": f"{realizacao.treinamento.nome} — {realizacao.funcionario.nome}",
                    "vencimento": realizacao.data_validade,
                    "status": realizacao.status,
                }
            )

    alertas.sort(key=lambda item: item["vencimento"])
    return alertas


def coletar_dados_gerais():
    """Agrega os principais números do sistema para o dashboard e o PDF geral."""
    hoje = date.today()
    limite_30_dias = hoje - timedelta(days=30)

    funcionarios_ativos = Funcionario.query.filter_by(ativo=True).all()
    contagem_setores = Counter(f.setor.nome for f in funcionarios_ativos)
    funcionarios_por_setor = [
        {"setor": setor, "quantidade": quantidade}
        for setor, quantidade in sorted(contagem_setores.items())
    ]

    alertas = coletar_alertas_vencimento()

    contagem_planos = Counter(
        plano.status for plano in PlanoAcaoPsicossocial.query.all()
    )

    return {
        "total_funcionarios": len(funcionarios_ativos),
        "total_setores": Setor.query.count(),
        "funcionarios_por_setor": funcionarios_por_setor,
        "acidentes_recentes": Acidente.query.filter(Acidente.data >= limite_30_dias).count(),
        "total_acidentes": Acidente.query.count(),
        "total_epis_entregues": EntregaEpi.query.count(),
        "total_exames_realizados": Exame.query.count(),
        "total_treinamentos_realizados": RealizacaoTreinamento.query.count(),
        "alertas": alertas,
        "itens_vencidos": sum(1 for a in alertas if a["status"] == "vencido"),
        "itens_vencendo": sum(1 for a in alertas if a["status"] == "vencendo"),
        "planos_acao_pendentes": contagem_planos.get("Pendente", 0),
        "planos_acao_em_andamento": contagem_planos.get("Em andamento", 0),
        "planos_acao_concluidos": contagem_planos.get("Concluído", 0),
    }


def coletar_dados_acidentes():
    """Agrega os dados usados no relatório de acidentes (tela e PDF)."""
    acidentes = Acidente.query.all()

    por_gravidade = Counter(a.gravidade for a in acidentes)
    por_tipo = Counter(a.tipo for a in acidentes)
    total_dias_afastamento = sum(a.dias_afastamento or 0 for a in acidentes)

    doze_meses_atras = date.today().replace(day=1) - timedelta(days=365)
    por_mes = Counter(
        a.data.strftime("%Y-%m") for a in acidentes if a.data >= doze_meses_atras
    )

    return {
        "total": len(acidentes),
        "por_gravidade": por_gravidade,
        "por_tipo": por_tipo,
        "total_dias_afastamento": total_dias_afastamento,
        "por_mes": sorted(por_mes.items()),
    }
