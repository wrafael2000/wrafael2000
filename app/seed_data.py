"""Dados iniciais (seed) dos questionários de riscos psicossociais.

IMPORTANTE: os textos das perguntas abaixo são versões próprias,
resumidas e parafraseadas, representando as dimensões de cada
instrumento (HSE-IT, COPSOQ II e CBI) — não são a tradução oficial e
validada cientificamente. Antes de aplicar formalmente a pesquisa,
substitua os itens pelos da versão oficial:

- HSE-IT: disponível gratuitamente no site do HSE (Reino Unido).
- COPSOQ II: versão validada para o Brasil pelo grupo COPSOQ Brasil.
- CBI (Copenhagen Burnout Inventory): domínio público, disponível em
  publicações acadêmicas (escolhido no lugar do MBI, que é proprietário).

A pesquisa de Clima Organizacional já é pensada para ser personalizada
livremente pela empresa.
"""

from .extensions import db
from .models import NormaRegulamentadora, Pergunta, Questionario

# Números e títulos das NRs vigentes no Brasil. Lista mantida manualmente:
# não inclui NR-2 e NR-27 (revogadas). Números a partir do NR-37 não estão
# incluídos por falta de confiança na exatidão do título — confira a lista
# completa e atualizada em:
# https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/normas-regulamentadoras
# antes de usar esta biblioteca para fins de auditoria/compliance.
LINK_PORTAL_NRS = (
    "https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/"
    "seguranca-e-saude-no-trabalho/normas-regulamentadoras"
)

NORMAS_REGULAMENTADORAS = [
    ("NR-1", "Disposições Gerais e Gerenciamento de Riscos Ocupacionais"),
    ("NR-3", "Embargo e Interdição"),
    ("NR-4", "Serviços Especializados em Engenharia de Segurança e em Medicina do Trabalho"),
    ("NR-5", "Comissão Interna de Prevenção de Acidentes e de Assédio (CIPA)"),
    ("NR-6", "Equipamento de Proteção Individual (EPI)"),
    ("NR-7", "Programa de Controle Médico de Saúde Ocupacional (PCMSO)"),
    ("NR-8", "Edificações"),
    ("NR-9", "Avaliação e Controle das Exposições Ocupacionais a Agentes Físicos, Químicos e Biológicos"),
    ("NR-10", "Segurança em Instalações e Serviços em Eletricidade"),
    ("NR-11", "Transporte, Movimentação, Armazenagem e Manuseio de Materiais"),
    ("NR-12", "Segurança no Trabalho em Máquinas e Equipamentos"),
    ("NR-13", "Caldeiras, Vasos de Pressão e Tubulações"),
    ("NR-14", "Fornos"),
    ("NR-15", "Atividades e Operações Insalubres"),
    ("NR-16", "Atividades e Operações Perigosas"),
    ("NR-17", "Ergonomia"),
    ("NR-18", "Segurança e Saúde no Trabalho na Indústria da Construção"),
    ("NR-19", "Explosivos"),
    ("NR-20", "Segurança e Saúde no Trabalho com Inflamáveis e Combustíveis"),
    ("NR-21", "Trabalho a Céu Aberto"),
    ("NR-22", "Segurança e Saúde Ocupacional na Mineração"),
    ("NR-23", "Proteção Contra Incêndios"),
    ("NR-24", "Condições Sanitárias e de Conforto nos Locais de Trabalho"),
    ("NR-25", "Resíduos Industriais"),
    ("NR-26", "Sinalização de Segurança"),
    ("NR-28", "Fiscalização e Penalidades"),
    ("NR-29", "Segurança e Saúde no Trabalho Portuário"),
    ("NR-30", "Segurança e Saúde no Trabalho Aquaviário"),
    ("NR-31", "Segurança e Saúde no Trabalho na Agricultura, Pecuária, Silvicultura, Exploração Florestal e Aquicultura"),
    ("NR-32", "Segurança e Saúde no Trabalho em Serviços de Saúde"),
    ("NR-33", "Segurança e Saúde nos Trabalhos em Espaços Confinados"),
    ("NR-34", "Condições e Meio Ambiente de Trabalho na Indústria da Construção, Reparação e Desmonte Naval"),
    ("NR-35", "Trabalho em Altura"),
    ("NR-36", "Segurança e Saúde no Trabalho em Empresas de Abate e Processamento de Carnes e Derivados"),
]

HSE_IT = {
    "tipo": "HSE-IT",
    "nome": "HSE Management Standards Indicator Tool (HSE-IT)",
    "descricao": (
        "Instrumento do HSE (Reino Unido) para avaliar 7 dimensões de risco "
        "psicossocial relacionadas à organização do trabalho."
    ),
    "dimensoes": {
        "Demandas": [
            "Consigo dar conta do volume de trabalho que recebo.",
            "Tenho prazos razoáveis para entregar minhas tarefas.",
            "Meu ritmo de trabalho é adequado, sem pressa excessiva.",
        ],
        "Controle": [
            "Tenho liberdade para decidir como organizar meu trabalho.",
            "Posso opinar sobre a ordem em que realizo minhas tarefas.",
            "Tenho controle sobre o ritmo do meu trabalho.",
        ],
        "Apoio da Chefia": [
            "Minha liderança me apoia quando tenho dificuldades no trabalho.",
            "Recebo feedback útil da minha chefia.",
            "Minha liderança está disponível quando preciso conversar.",
        ],
        "Apoio dos Colegas": [
            "Posso contar com meus colegas quando preciso de ajuda.",
            "Existe boa colaboração entre a minha equipe.",
            "Meus colegas me tratam com respeito.",
        ],
        "Relacionamentos": [
            "No meu ambiente de trabalho não sofro assédio ou intimidação.",
            "Os conflitos na equipe são tratados de forma adequada.",
            "Sinto-me respeitado(a) pelos colegas de trabalho.",
        ],
        "Papel (Clareza de Função)": [
            "Sei claramente quais são minhas responsabilidades no trabalho.",
            "Entendo como meu trabalho contribui para os objetivos da empresa.",
            "Não recebo demandas contraditórias de diferentes pessoas.",
        ],
        "Mudança": [
            "Sou informado(a) com antecedência sobre mudanças que afetam meu trabalho.",
            "Tenho oportunidade de opinar sobre mudanças que me afetam.",
            "As mudanças na empresa são bem explicadas para mim.",
        ],
    },
}

COPSOQ_II = {
    "tipo": "COPSOQ II",
    "nome": "COPSOQ II (Copenhagen Psychosocial Questionnaire)",
    "descricao": (
        "Questionário psicossocial de Copenhague — avalia exigências, organização "
        "do trabalho, relações sociais e bem-estar."
    ),
    "dimensoes": {
        "Exigências Quantitativas": [
            "Tenho uma quantidade de trabalho que considero excessiva.",
            "Preciso trabalhar muito rápido para dar conta das tarefas.",
        ],
        "Influência no Trabalho": [
            "Tenho influência sobre as decisões relacionadas ao meu trabalho.",
            "Posso participar da definição das minhas próprias tarefas.",
        ],
        "Possibilidades de Desenvolvimento": [
            "Meu trabalho me dá oportunidades de aprender coisas novas.",
            "Tenho chances de desenvolver minhas habilidades profissionais.",
        ],
        "Apoio Social de Colegas": [
            "Recebo ajuda e apoio dos meus colegas quando necessário.",
        ],
        "Apoio Social da Chefia": [
            "Recebo ajuda e apoio da minha chefia quando necessário.",
        ],
        "Previsibilidade": [
            "Sou informado(a) com antecedência sobre decisões importantes que afetam meu trabalho.",
        ],
        "Reconhecimento": [
            "Meu trabalho é reconhecido e valorizado pela empresa.",
        ],
        "Conflito Trabalho-Família": [
            "Consigo equilibrar minha vida profissional e pessoal.",
        ],
        "Insegurança no Trabalho": [
            "Sinto-me seguro(a) em relação à manutenção do meu emprego.",
        ],
        "Saúde Geral e Estresse": [
            "De modo geral, considero minha saúde boa.",
            "Sinto-me estressado(a) com frequência por causa do trabalho.",
        ],
    },
}

CBI = {
    "tipo": "CBI (Burnout)",
    "nome": "CBI - Copenhagen Burnout Inventory",
    "descricao": (
        "Avalia esgotamento profissional (burnout) em três dimensões: pessoal, "
        "relacionado ao trabalho e relacionado ao público/clientes. Usado no "
        "lugar do MBI por ser um instrumento de domínio público."
    ),
    "dimensoes": {
        "Exaustão Pessoal": [
            "Sinto-me fisicamente exausto(a) com frequência.",
            "Sinto-me emocionalmente esgotado(a).",
            "Sinto que não tenho mais energia no final do dia de trabalho.",
            "Acordo cansado(a) mesmo após dormir bem.",
        ],
        "Exaustão Relacionada ao Trabalho": [
            "Meu trabalho me deixa emocionalmente exausto(a).",
            "Sinto-me frustrado(a) com o meu trabalho.",
            "Meu trabalho consome toda a minha energia.",
            "Sinto que estou chegando ao limite com o meu trabalho.",
        ],
        "Exaustão Relacionada ao Público/Clientes": [
            "Lidar com clientes/usuários no trabalho me deixa exausto(a).",
            "Sinto que dou mais do que recebo no contato com clientes/usuários.",
            "Fico impaciente ao lidar com clientes/usuários por causa do cansaço.",
            "Prefiro evitar contato direto com clientes/usuários quando estou cansado(a).",
        ],
    },
}

CLIMA = {
    "tipo": "Clima Organizacional",
    "nome": "Pesquisa de Clima Organizacional",
    "descricao": (
        "Ponto de partida personalizável — edite, remova ou adicione perguntas "
        "conforme a realidade da sua empresa."
    ),
    "dimensoes": {
        "Comunicação": [
            "As informações importantes chegam até mim de forma clara.",
            "Sinto-me à vontade para expressar minha opinião no trabalho.",
        ],
        "Reconhecimento": [
            "Meu trabalho é valorizado pela empresa.",
            "Recebo feedback sobre o meu desempenho.",
        ],
        "Liderança": [
            "Confio nas decisões da liderança da empresa.",
            "Minha liderança trata a equipe com justiça.",
        ],
        "Ambiente de Trabalho": [
            "O ambiente físico de trabalho é adequado.",
            "Sinto-me seguro(a) fisicamente no meu local de trabalho.",
        ],
        "Desenvolvimento Profissional": [
            "Vejo oportunidades de crescimento profissional na empresa.",
            "Recebo treinamento adequado para exercer minha função.",
        ],
    },
}

QUESTIONARIOS_PADRAO = [HSE_IT, COPSOQ_II, CBI, CLIMA]


def seed_questionarios():
    """Cria os questionários padrão se ainda não existirem (idempotente)."""
    criados = []
    for dados in QUESTIONARIOS_PADRAO:
        existente = Questionario.query.filter_by(tipo=dados["tipo"]).first()
        if existente:
            continue

        questionario = Questionario(
            tipo=dados["tipo"], nome=dados["nome"], descricao=dados["descricao"]
        )
        db.session.add(questionario)
        db.session.flush()  # garante questionario.id antes de criar as perguntas

        ordem = 0
        for dimensao, perguntas in dados["dimensoes"].items():
            for texto in perguntas:
                ordem += 1
                db.session.add(
                    Pergunta(
                        texto=texto, dimensao=dimensao, ordem=ordem, questionario_id=questionario.id
                    )
                )

        criados.append(dados["tipo"])

    db.session.commit()
    return criados


def seed_normas_regulamentadoras():
    """Cria o catálogo de NRs se ainda não existir (idempotente)."""
    criadas = []
    for numero, titulo in NORMAS_REGULAMENTADORAS:
        if NormaRegulamentadora.query.filter_by(numero=numero).first():
            continue
        db.session.add(
            NormaRegulamentadora(
                numero=numero, titulo=titulo, aplicavel=True, link_oficial=LINK_PORTAL_NRS
            )
        )
        criadas.append(numero)

    db.session.commit()
    return criadas
