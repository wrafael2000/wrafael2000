"""Geração de relatórios em PDF (reportlab) a partir dos dados de app/relatorios.py."""

import io
from datetime import date
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

from .models import Empresa, Exame

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


_estilo_aviso = ParagraphStyle(
    "AvisoRelatorio",
    parent=_estilos["Normal"],
    textColor=colors.HexColor("#8c261e"),
    backColor=colors.HexColor("#fbe4e2"),
    borderPadding=8,
    spaceBefore=10,
    spaceAfter=10,
)

_AVISO_PGR = (
    "Este documento foi gerado automaticamente pelo sistema a partir dos dados "
    "cadastrados e não substitui a elaboração, revisão e assinatura de um "
    "engenheiro de segurança do trabalho (ou profissional legalmente habilitado), "
    "conforme exige a NR-01. Revise todo o conteúdo antes de considerá-lo o PGR "
    "oficial da empresa."
)


def gerar_pdf_pgr(pgr):
    buffer = io.BytesIO()
    doc, elementos = _novo_documento(buffer, "Programa de Gerenciamento de Riscos (PGR)")

    elementos.append(_paragrafo_livre(_AVISO_PGR, _estilo_aviso))

    linhas_cabecalho = [
        ["Título", pgr.titulo],
        ["Responsável técnico", pgr.responsavel_tecnico],
        ["Data de elaboração", pgr.data_elaboracao.strftime("%d/%m/%Y")],
        ["Validade / próxima revisão", pgr.data_validade.strftime("%d/%m/%Y") if pgr.data_validade else "Não informada"],
    ]
    if pgr.responsavel_tecnico_registro:
        linhas_cabecalho.insert(2, ["Registro profissional", pgr.responsavel_tecnico_registro])
    elementos.append(_tabela(["Campo", "Valor"], linhas_cabecalho, larguras=[5 * cm, 11 * cm]))

    if pgr.introducao:
        elementos.append(Paragraph("Introdução / metodologia", _estilo_secao))
        elementos.append(_paragrafo_livre(pgr.introducao))

    elementos.append(Paragraph("Inventário de riscos", _estilo_secao))
    if pgr.itens:
        elementos.append(
            _tabela(
                ["Setor", "Função/atividade", "Categoria", "Perigo/fator de risco", "Nível"],
                [
                    [
                        item.setor.nome,
                        item.funcao_atividade or "-",
                        item.categoria_risco,
                        item.perigo_fator_risco,
                        item.nivel_risco,
                    ]
                    for item in pgr.itens
                ],
                larguras=[2.6 * cm, 2.8 * cm, 2.6 * cm, 6 * cm, 2 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhum item de risco cadastrado.", _estilo_texto))

    elementos.append(Paragraph("Plano de ação", _estilo_secao))
    if pgr.itens:
        elementos.append(
            _tabela(
                ["Setor", "Medida recomendada", "Responsável", "Prazo", "Status"],
                [
                    [
                        item.setor.nome,
                        item.medidas_recomendadas,
                        item.responsavel_acao or "-",
                        item.prazo.strftime("%d/%m/%Y") if item.prazo else "-",
                        item.status,
                    ]
                    for item in pgr.itens
                ],
                larguras=[2.6 * cm, 6.8 * cm, 2.8 * cm, 2 * cm, 1.8 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhuma ação cadastrada.", _estilo_texto))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


_AVISO_PCMSO = (
    "Este documento foi gerado automaticamente pelo sistema a partir dos dados "
    "cadastrados e não substitui a elaboração, revisão e assinatura do médico "
    "coordenador do PCMSO, conforme exige a NR-07. Revise todo o conteúdo antes "
    "de considerá-lo o PCMSO oficial da empresa."
)


def gerar_pdf_pcmso(pcmso):
    buffer = io.BytesIO()
    doc, elementos = _novo_documento(buffer, "Programa de Controle Médico de Saúde Ocupacional (PCMSO)")

    elementos.append(_paragrafo_livre(_AVISO_PCMSO, _estilo_aviso))

    linhas_cabecalho = [
        ["Título", pcmso.titulo],
        ["Médico coordenador", pcmso.medico_coordenador],
        ["Data de elaboração", pcmso.data_elaboracao.strftime("%d/%m/%Y")],
        ["Validade / próxima revisão", pcmso.data_validade.strftime("%d/%m/%Y") if pcmso.data_validade else "Não informada"],
    ]
    if pcmso.medico_coordenador_crm:
        linhas_cabecalho.insert(2, ["CRM do médico coordenador", pcmso.medico_coordenador_crm])
    elementos.append(_tabela(["Campo", "Valor"], linhas_cabecalho, larguras=[5 * cm, 11 * cm]))

    if pcmso.diretrizes:
        elementos.append(Paragraph("Diretrizes gerais", _estilo_secao))
        elementos.append(_paragrafo_livre(pcmso.diretrizes))

    elementos.append(Paragraph("Quadro de funções, riscos e exames", _estilo_secao))
    if pcmso.itens:
        elementos.append(
            _tabela(
                ["Setor", "Função", "Riscos ocupacionais", "Exames indicados", "Periodicidade"],
                [
                    [
                        item.setor.nome,
                        item.funcao,
                        item.riscos_ocupacionais,
                        item.exames_indicados,
                        f"{item.periodicidade_meses} meses",
                    ]
                    for item in pcmso.itens
                ],
                larguras=[2.3 * cm, 2.7 * cm, 4.3 * cm, 4.3 * cm, 2.4 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhum item cadastrado.", _estilo_texto))

    elementos.append(Paragraph("Exames ocupacionais já registrados no sistema", _estilo_secao))
    exames = Exame.query.join(Exame.funcionario).order_by(Exame.data_exame.desc()).limit(100).all()
    if exames:
        elementos.append(
            _tabela(
                ["Funcionário", "Tipo", "Data", "Resultado", "Validade"],
                [
                    [
                        exame.funcionario.nome,
                        exame.tipo,
                        exame.data_exame.strftime("%d/%m/%Y"),
                        exame.resultado,
                        exame.data_validade.strftime("%d/%m/%Y") if exame.data_validade else "-",
                    ]
                    for exame in exames
                ],
                larguras=[5 * cm, 3.5 * cm, 2.5 * cm, 2.5 * cm, 2.5 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhum exame (ASO) registrado no sistema ainda.", _estilo_texto))

    doc.build(elementos)
    buffer.seek(0)
    return buffer


_AVISO_LTCAT = (
    "Este documento foi gerado automaticamente pelo sistema a partir dos dados "
    "cadastrados e não substitui a elaboração, as medições técnicas, a revisão e "
    "a assinatura de um engenheiro de segurança do trabalho (ou profissional "
    "legalmente habilitado). As intensidades/concentrações e conclusões sobre "
    "direito a aposentadoria especial devem ser confirmadas por esse profissional "
    "antes de considerar este o LTCAT oficial da empresa."
)


def gerar_pdf_ltcat(ltcat):
    buffer = io.BytesIO()
    doc, elementos = _novo_documento(buffer, "Laudo Técnico das Condições do Ambiente de Trabalho (LTCAT)")

    elementos.append(_paragrafo_livre(_AVISO_LTCAT, _estilo_aviso))

    linhas_cabecalho = [
        ["Título", ltcat.titulo],
        ["Responsável técnico", ltcat.responsavel_tecnico],
        ["Data de elaboração", ltcat.data_elaboracao.strftime("%d/%m/%Y")],
        ["Validade / próxima revisão", ltcat.data_validade.strftime("%d/%m/%Y") if ltcat.data_validade else "Não informada"],
    ]
    if ltcat.responsavel_tecnico_registro:
        linhas_cabecalho.insert(2, ["Registro profissional", ltcat.responsavel_tecnico_registro])
    elementos.append(_tabela(["Campo", "Valor"], linhas_cabecalho, larguras=[5 * cm, 11 * cm]))

    if ltcat.metodologia:
        elementos.append(Paragraph("Metodologia de avaliação", _estilo_secao))
        elementos.append(_paragrafo_livre(ltcat.metodologia))

    elementos.append(Paragraph("Agentes nocivos avaliados", _estilo_secao))
    if ltcat.itens:
        elementos.append(
            _tabela(
                ["Setor", "Função", "Agente/tipo", "Intensidade", "Limite", "EPI/EPC eficaz", "Conclusão"],
                [
                    [
                        item.setor.nome,
                        item.funcao,
                        f"{item.agente_nocivo} ({item.tipo_agente})",
                        item.intensidade_concentracao or "-",
                        item.limite_tolerancia or "-",
                        item.epi_epc_eficaz,
                        item.conclusao,
                    ]
                    for item in ltcat.itens
                ],
                larguras=[1.8 * cm, 2 * cm, 4 * cm, 2 * cm, 2 * cm, 2.2 * cm, 2 * cm],
            )
        )
    else:
        elementos.append(Paragraph("Nenhum agente nocivo cadastrado.", _estilo_texto))

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
