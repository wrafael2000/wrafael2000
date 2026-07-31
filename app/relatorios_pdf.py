"""Geração de relatórios em PDF (reportlab) a partir dos dados de app/relatorios.py."""

import io
from datetime import date
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import Empresa

_COR_PRIMARIA = colors.HexColor("#1d6f42")
_COR_FUNDO_CABECALHO = colors.HexColor("#e3f3e8")

_estilos = getSampleStyleSheet()
_estilo_titulo = ParagraphStyle(
    "TituloRelatorio", parent=_estilos["Title"], textColor=_COR_PRIMARIA
)
_estilo_subtitulo = ParagraphStyle(
    "SubtituloRelatorio", parent=_estilos["Normal"], textColor=colors.grey, spaceAfter=14
)
_estilo_secao = ParagraphStyle(
    "SecaoRelatorio", parent=_estilos["Heading2"], textColor=_COR_PRIMARIA, spaceBefore=16
)
_estilo_texto = _estilos["Normal"]


def _novo_documento(buffer, titulo):
    doc = SimpleDocTemplate(
        buffer,
        pagesize=A4,
        topMargin=2 * cm,
        bottomMargin=2 * cm,
        leftMargin=2 * cm,
        rightMargin=2 * cm,
    )
    elementos = [Paragraph(titulo, _estilo_titulo)]

    empresa = Empresa.obter_ou_none()
    if empresa:
        nome_empresa = empresa.nome_fantasia or empresa.razao_social
        elementos.append(Paragraph(nome_empresa, _estilo_subtitulo))

    elementos.append(
        Paragraph(f"Gerado em {date.today().strftime('%d/%m/%Y')}", _estilo_subtitulo)
    )
    return doc, elementos


def _tabela(cabecalho, linhas, larguras=None):
    dados = [cabecalho] + linhas
    tabela = Table(dados, colWidths=larguras, repeatRows=1)
    tabela.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, 0), _COR_FUNDO_CABECALHO),
                ("TEXTCOLOR", (0, 0), (-1, 0), _COR_PRIMARIA),
                ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
                ("FONTSIZE", (0, 0), (-1, -1), 9),
                ("GRID", (0, 0), (-1, -1), 0.5, colors.HexColor("#d6ddd9")),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f4f6f5")]),
            ]
        )
    )
    return tabela


def gerar_pdf_relatorio_geral(dados):
    buffer = io.BytesIO()
    doc, elementos = _novo_documento(buffer, "Relatório Geral de SST")

    elementos.append(Paragraph("Resumo geral", _estilo_secao))
    elementos.append(
        _tabela(
            ["Indicador", "Valor"],
            [
                ["Funcionários ativos", str(dados["total_funcionarios"])],
                ["Setores cadastrados", str(dados["total_setores"])],
                ["Acidentes/incidentes (últimos 30 dias)", str(dados["acidentes_recentes"])],
                ["Acidentes/incidentes (total)", str(dados["total_acidentes"])],
                ["Entregas de EPI registradas", str(dados["total_epis_entregues"])],
                ["Exames (ASO) realizados", str(dados["total_exames_realizados"])],
                ["Treinamentos realizados", str(dados["total_treinamentos_realizados"])],
                ["Itens vencendo (30 dias)", str(dados["itens_vencendo"])],
                ["Itens vencidos", str(dados["itens_vencidos"])],
            ],
            larguras=[11 * cm, 5 * cm],
        )
    )

    elementos.append(Paragraph("Funcionários por setor", _estilo_secao))
    if dados["funcionarios_por_setor"]:
        elementos.append(
            _tabela(
                ["Setor", "Funcionários ativos"],
                [[item["setor"], str(item["quantidade"])] for item in dados["funcionarios_por_setor"]],
                larguras=[11 * cm, 5 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhum funcionário ativo cadastrado.", _estilo_texto))

    elementos.append(Paragraph("Planos de ação psicossociais", _estilo_secao))
    elementos.append(
        _tabela(
            ["Status", "Quantidade"],
            [
                ["Pendentes", str(dados["planos_acao_pendentes"])],
                ["Em andamento", str(dados["planos_acao_em_andamento"])],
                ["Concluídos", str(dados["planos_acao_concluidos"])],
            ],
            larguras=[11 * cm, 5 * cm],
        )
    )

    elementos.append(Paragraph("Próximos vencimentos", _estilo_secao))
    if dados["alertas"]:
        elementos.append(
            _tabela(
                ["Tipo", "Descrição", "Vencimento", "Status"],
                [
                    [
                        a["tipo"],
                        a["descricao"],
                        a["vencimento"].strftime("%d/%m/%Y"),
                        "Vencido" if a["status"] == "vencido" else "Vencendo",
                    ]
                    for a in dados["alertas"]
                ],
                larguras=[3 * cm, 8 * cm, 2.5 * cm, 2.5 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhum item vencido ou vencendo no momento.", _estilo_texto))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


def _paragrafo_livre(texto, estilo=None):
    """Paragraph a partir de texto digitado pelo usuário (escapa &, <, > para não quebrar o XML do reportlab)."""
    texto_seguro = escape(texto).replace("\n", "<br/>")
    return Paragraph(texto_seguro, estilo or _estilo_texto)


def gerar_pdf_dds(dds):
    buffer = io.BytesIO()
    doc, elementos = _novo_documento(buffer, "Diálogo Diário de Segurança (DDS)")

    elementos.append(
        _tabela(
            ["Campo", "Valor"],
            [
                ["Data", dds.data.strftime("%d/%m/%Y")],
                ["Setor", dds.setor.nome],
                ["Tema abordado", dds.tema],
                ["Responsável pelo diálogo", dds.responsavel],
            ],
            larguras=[5 * cm, 11 * cm],
        )
    )

    if dds.conteudo:
        elementos.append(Paragraph("Conteúdo / observações", _estilo_secao))
        elementos.append(_paragrafo_livre(dds.conteudo))

    elementos.append(Paragraph("Lista de presença", _estilo_secao))
    if dds.participantes:
        elementos.append(
            _tabela(
                ["Participante", "Assinatura"],
                [[p.nome, ""] for p in dds.participantes],
                larguras=[8 * cm, 8 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhum participante registrado.", _estilo_texto))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


def gerar_pdf_apr(apr):
    buffer = io.BytesIO()
    doc, elementos = _novo_documento(buffer, "Análise Preliminar de Risco (APR)")

    linhas_cabecalho = [
        ["Atividade/tarefa", apr.titulo],
        ["Setor", apr.setor.nome],
        ["Data", apr.data.strftime("%d/%m/%Y")],
        ["Responsável pela análise", apr.responsavel],
    ]
    if apr.local:
        linhas_cabecalho.insert(2, ["Local", apr.local])
    elementos.append(_tabela(["Campo", "Valor"], linhas_cabecalho, larguras=[5 * cm, 11 * cm]))

    if apr.observacoes:
        elementos.append(Paragraph("Observações", _estilo_secao))
        elementos.append(_paragrafo_livre(apr.observacoes))

    elementos.append(Paragraph("Etapas, perigos/riscos e medidas de controle", _estilo_secao))
    if apr.etapas:
        elementos.append(
            _tabela(
                ["Etapa", "Perigo/risco", "Medida de controle"],
                [
                    [etapa.descricao_etapa, etapa.perigo_risco, etapa.medida_controle]
                    for etapa in apr.etapas
                ],
                larguras=[5.3 * cm, 5.3 * cm, 5.4 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhuma etapa cadastrada.", _estilo_texto))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


def gerar_pdf_relatorio_acidentes(dados):
    buffer = io.BytesIO()
    doc, elementos = _novo_documento(buffer, "Relatório de Acidentes e Incidentes")

    elementos.append(Paragraph("Resumo", _estilo_secao))
    elementos.append(
        _tabela(
            ["Indicador", "Valor"],
            [
                ["Total de ocorrências", str(dados["total"])],
                ["Dias de afastamento (total)", str(dados["total_dias_afastamento"])],
            ],
            larguras=[11 * cm, 5 * cm],
        )
    )

    elementos.append(Paragraph("Por gravidade", _estilo_secao))
    if dados["por_gravidade"]:
        elementos.append(
            _tabela(
                ["Gravidade", "Quantidade"],
                [[gravidade, str(qtd)] for gravidade, qtd in dados["por_gravidade"].items()],
                larguras=[11 * cm, 5 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Sem dados.", _estilo_texto))

    elementos.append(Paragraph("Por tipo", _estilo_secao))
    if dados["por_tipo"]:
        elementos.append(
            _tabela(
                ["Tipo", "Quantidade"],
                [[tipo, str(qtd)] for tipo, qtd in dados["por_tipo"].items()],
                larguras=[11 * cm, 5 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Sem dados.", _estilo_texto))

    elementos.append(Paragraph("Por mês (últimos 12 meses)", _estilo_secao))
    if dados["por_mes"]:
        elementos.append(
            _tabela(
                ["Mês", "Quantidade"],
                [[mes, str(qtd)] for mes, qtd in dados["por_mes"]],
                larguras=[11 * cm, 5 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Sem dados no período.", _estilo_texto))

    doc.build(elementos)
    buffer.seek(0)
    return buffer
