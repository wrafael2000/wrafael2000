# Gestão de SST — Sistema de Saúde e Segurança do Trabalho

Sistema web para apoiar a gestão de Saúde e Segurança do Trabalho (SST) de uma
empresa: controle de funcionários e setores, EPIs, acidentes/incidentes,
exames e documentos obrigatórios, treinamentos, e (em fases futuras) módulos
de riscos psicossociais.

Este projeto está sendo construído **em fases**, para servir também como
material de aprendizado de programação web com Python.

## Stack tecnológica

| Camada | Tecnologia | Motivo |
|---|---|---|
| Backend/Web | **Python + Flask** | Sintaxe simples, ótimo para quem está aprendendo, muitas bibliotecas prontas |
| Banco de dados | **SQLite + SQLAlchemy** | Um único arquivo, sem precisar instalar servidor de banco; fácil migrar para PostgreSQL depois |
| Autenticação | **Flask-Login** + hash de senha (Werkzeug) | Login simples e seguro |
| Formulários | **Flask-WTF** | Proteção contra CSRF e validação de formulários |
| Front-end | HTML + CSS simples (sem framework JS por enquanto) | Foco em aprender o backend primeiro |

## Estrutura do projeto

```
.
├── run.py              # ponto de entrada da aplicação
├── config.py            # configurações (lidas de variáveis de ambiente)
├── requirements.txt
├── app/
│   ├── __init__.py      # application factory (cria e configura o Flask app)
│   ├── extensions.py     # instâncias do SQLAlchemy, Flask-Login, CSRF
│   ├── forms.py          # formulários (Flask-WTF)
│   ├── cli.py             # comando `flask create-admin`
│   ├── models/            # tabelas do banco (Usuario, Setor, Funcionario)
│   ├── routes/             # rotas agrupadas por blueprint (auth, setores, funcionarios, main)
│   ├── templates/          # páginas HTML (Jinja2)
│   └── static/css/          # estilos
```

## Como rodar localmente

```bash
# 1. Criar e ativar um ambiente virtual
python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate

# 2. Instalar as dependências
pip install -r requirements.txt

# 3. Copiar o arquivo de variáveis de ambiente
cp .env.example .env
# edite o .env e troque SECRET_KEY por um valor aleatório

# 4. Criar o primeiro usuário administrador
export FLASK_APP=run.py          # Windows (PowerShell): $env:FLASK_APP="run.py"
flask create-admin

# 5. Rodar o servidor de desenvolvimento
python run.py
```

Acesse **http://127.0.0.1:5000** e faça login com o usuário criado no passo 4.

O banco de dados SQLite é criado automaticamente em `instance/sst.db` na
primeira execução.

## Módulos implementados

**Fase 1 — Base**
- Login de administrador
- Cadastro, edição e remoção de **setores**
- Cadastro, edição e remoção de **funcionários** (vinculados a um setor)

**Fase 2 — Controle de EPIs**
- Catálogo de EPIs (nome, CA, vida útil em dias)
- Registro de entregas de EPI a funcionários, com cálculo automático da data
  de validade a partir da vida útil do equipamento
- Status por entrega: válido / vencendo (30 dias) / vencido / sem validade
- Dashboard com totais gerais e alertas de EPIs vencidos/vencendo

**Fase 3 — Acidentes e incidentes**
- Registro de ocorrências (funcionário, data, local, tipo, gravidade,
  descrição, causa, medidas tomadas, dias de afastamento)
- Relatório com totais por gravidade, por tipo e por mês (últimos 12 meses),
  além do total acumulado de dias de afastamento
- Dashboard com contador de acidentes nos últimos 30 dias

## Roadmap (próximas fases)

- **Fase 4 — Exames e documentos obrigatórios**: controle de ASO, PCMSO, PGR
  e prazos de validade, com alertas.
- **Fase 5 — Treinamentos e certificações**: controle de treinamentos de NRs
  por funcionário, com validade e alertas de renovação.
- **Fase 6 — Riscos psicossociais e clima organizacional**: aplicação dos
  questionários **HSE-IT** e **COPSOQ II** (uso livre/acadêmico) com plano de
  ação, pesquisa de clima organizacional personalizável, e avaliação de
  esgotamento profissional com o **CBI (Copenhagen Burnout Inventory)** —
  escolhido no lugar do MBI por ser um instrumento cientificamente validado e
  de domínio público (o MBI é proprietário e exige licenciamento da Mind
  Garden).
- **Fase 7 — Dashboard consolidado e exportação de relatórios em PDF**.

## Aprendendo com este projeto

Cada fase é implementada de forma incremental, com commits organizados, para
que seja possível acompanhar como o sistema cresce peça por peça:
models → rotas → formulários → templates. Sinta-se à vontade para ler o
código de uma fase antes de pedir a próxima.
