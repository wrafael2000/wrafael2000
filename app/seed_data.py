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
from .models import Pergunta, Questionario

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
