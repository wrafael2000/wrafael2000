# Gestão de SST — Sistema de Saúde e Segurança do Trabalho

Sistema web para apoiar a gestão de Saúde e Segurança do Trabalho (SST) de uma
empresa: controle de funcionários e setores, EPIs, acidentes/incidentes,
exames e documentos obrigatórios, treinamentos, riscos psicossociais/clima
organizacional e relatórios em PDF.

Este projeto foi construído **em fases**, para servir também como material
de aprendizado de programação web com Python. As 7 fases do roadmap
original estão completas — veja "Próximos passos" no final deste README
para ideias de continuação.

## Stack tecnológica

| Camada | Tecnologia | Motivo |
|---|---|---|
| Backend/Web | **Python + Flask** | Sintaxe simples, ótimo para quem está aprendendo, muitas bibliotecas prontas |
| Banco de dados | **SQLite + SQLAlchemy** | Um único arquivo, sem precisar instalar servidor de banco; fácil migrar para PostgreSQL depois |
| Autenticação | **Flask-Login** + hash de senha (Werkzeug) | Login simples e seguro |
| Formulários | **Flask-WTF** | Proteção contra CSRF e validação de formulários |
| Relatórios em PDF | **ReportLab** | Geração de PDF sem dependências externas de sistema |
| Front-end | HTML + CSS simples (sem framework JS por enquanto) | Foco em aprender o backend primeiro |

## Quero só abrir o programa, não mexer no código

Se você não vai programar, pule para a seção
["Versão desktop (clique e use)"](#versão-desktop-clique-e-use) mais abaixo —
é bem mais simples que as instruções de desenvolvimento a seguir.

## Estrutura do projeto

```
.
├── run.py              # ponto de entrada da aplicação (uso via terminal/desenvolvimento)
├── desktop_run.py       # ponto de entrada da versão desktop (.exe, "clique e use")
├── build_windows.bat    # gera o .exe a partir do desktop_run.py (rodar 1x no Windows)
├── resetar_senha.py      # utilitário para redefinir senha sem apagar dados
├── config.py               # configurações (lidas de variáveis de ambiente)
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

# 5. (Opcional) Criar os questionários padrão de riscos psicossociais
flask seed-questionarios

# 6. (Opcional) Criar o catálogo padrão de Normas Regulamentadoras
flask seed-normas

# 7. Rodar o servidor de desenvolvimento
python run.py
```

Acesse **http://127.0.0.1:5000** e faça login com o usuário criado no passo 4.

## Versão desktop (clique e use)

Para quem só quer usar o sistema, sem mexer com terminal toda vez: dá para
gerar um único arquivo `.exe` (Windows) que abre o programa sozinho, sem
precisar instalar Python, ativar ambiente virtual nem digitar comandos.

**Isso exige um passo único de preparação** (só uma vez, e ainda usa o
terminal nessa etapa — depois disso, nunca mais):

1. Baixe/clone este repositório no seu computador.
2. Instale o [Python](https://www.python.org/downloads/) se ainda não tiver
   (marque "Add Python to PATH" durante a instalação).
3. Dentro da pasta do projeto, dê **dois cliques** no arquivo
   `build_windows.bat`.
4. Aguarde — ele vai instalar tudo sozinho e gerar o programa. Pode levar
   alguns minutos.
5. Ao final, vai aparecer o arquivo
   `dist\SST-Saude-Seguranca-Trabalho.exe`. Copie **só esse arquivo** para
   onde quiser (ex.: Área de Trabalho).

**A partir daí, é só clicar duas vezes nesse `.exe` toda vez que quiser usar
o sistema.** Ele abre uma janela preta (deixe aberta enquanto usa o
programa) e o navegador sozinho, em `http://127.0.0.1:5000`.

No primeiro uso, a própria janela do programa vai perguntar o nome, e-mail e
senha do administrador — é o seu login. Nas próximas vezes, ele pula direto
para a tela de login do sistema.

Os dados ficam salvos numa pasta `dados` ao lado do `.exe` — não apague essa
pasta, é onde estão os cadastros. Para levar o sistema para outro
computador, copie o `.exe` **e** a pasta `dados` juntos.

### Esqueci a senha do administrador

Sem apagar nenhum dado, dá para redefinir a senha de um usuário já existente.
Duas formas, dependendo se você já gerou o `.exe` mais recente ou não:

**Se você já reconstruiu o `.exe` depois desta atualização:**
```
.\dist\SST-Saude-Seguranca-Trabalho.exe --resetar-senha
```
(rode isso no PowerShell, na pasta onde está o `.exe`)

**Se ainda não reconstruiu** (ou quer resolver sem esperar o build de novo):
na pasta do projeto, use o Python que já ficou instalado durante o build:
```
.venv_build\Scripts\python.exe resetar_senha.py
```
O script procura o banco de dados sozinho (em `dados\` ou `dist\dados\`) e
pergunta o e-mail e a nova senha.

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

**Fase 4 — Exames e documentos obrigatórios**
- Exames (ASO) por funcionário: tipo, data, validade, resultado (apto/inapto)
  e médico responsável
- Documentos SST da empresa (PCMSO, PGR, outros): tipo, emissão, validade e
  responsável técnico
- Dashboard reformulado com uma tabela única de **próximos vencimentos**,
  reunindo EPIs, exames e documentos vencidos/vencendo, ordenados pelo mais
  urgente

**Fase 5 — Treinamentos e certificações**
- Catálogo de treinamentos/NRs (nome, carga horária, validade/reciclagem)
- Registro de realizações por funcionário, com validade calculada
  automaticamente a partir do treinamento
- Treinamentos vencidos/vencendo passam a aparecer também na tabela de
  próximos vencimentos do dashboard, junto com EPIs, exames e documentos

**Fase 6 — Riscos psicossociais e clima organizacional**
- Motor genérico de questionários (`Questionario` → `Pergunta`), reutilizado
  para os 4 instrumentos: **HSE-IT**, **COPSOQ II**, **CBI (Copenhagen
  Burnout Inventory** — usado no lugar do MBI, que é proprietário) e
  **Clima Organizacional** (livremente personalizável)
- Comando `flask seed-questionarios` cria os 4 questionários com itens
  representativos por dimensão. **Importante:** os textos são uma versão
  própria e resumida, não a tradução oficial validada — antes de aplicar
  formalmente, edite as perguntas (`Questionários → Ver/editar perguntas`)
  com os itens oficiais do HSE-IT (site do HSE-UK) e do COPSOQ II (grupo
  COPSOQ Brasil)
- **Respostas anônimas por padrão**: cada "Aplicação" (rodada de pesquisa)
  gera um link público (`/responder/<token>`) que não exige login — o
  funcionário responde sem se identificar, só podendo indicar o setor
  (opcional). Dado psicossocial é sensível pela LGPD.
- Tela de resultados mostra médias por dimensão e total de respondentes,
  **sem inventar pontos de corte de risco** — a classificação (baixo/médio/
  alto) depende do manual oficial de cada instrumento e deve ser feita por
  um profissional qualificado (médico do trabalho, psicólogo, engenheiro de
  segurança)
- Plano de ação simples vinculado a cada aplicação (ação, responsável,
  prazo, status)

**Fase 7 — Dashboard consolidado e relatórios em PDF**
- Dashboard ampliado com funcionários por setor, totais gerais (acidentes,
  EPIs entregues, exames e treinamentos realizados) e resumo dos planos de
  ação psicossociais
- Botão "Baixar relatório geral (PDF)" no dashboard, com os mesmos dados da
  tela
- Botão "Baixar PDF" no relatório de acidentes
- Toda a lógica de agregação de dados foi centralizada em
  `app/relatorios.py`, reaproveitada tanto pelas telas HTML quanto pelos
  PDFs (`app/relatorios_pdf.py`) — evita ter a mesma conta feita em dois
  lugares que podem ficar dessincronizados

**Fase 8 — CIPA (Comissão Interna de Prevenção de Acidentes)**
- Mandatos (gestões, geralmente anuais conforme a NR-5), com opção de
  encerrar/reabrir
- Membros por mandato: funcionário, representação (empregador/empregado) e
  cargo (presidente, vice-presidente, titular, suplente)
- Atas de reunião (ordinária/extraordinária): pauta, deliberações e registro
  de quais membros estiveram presentes
- SIPAT: edições anuais com tema e período, e programação de atividades
  (título, data, horário, responsável, local)

**Fase 9 — Biblioteca de Normas Regulamentadoras (NRs)**
- Catálogo de NRs (`flask seed-normas` popula NR-1 a NR-38, exceto NR-2 e
  NR-27, que foram revogadas). **Importante:** os números e títulos foram
  digitados manualmente e podem estar desatualizados — confira sempre a
  lista oficial e vigente no
  [portal do governo](https://www.gov.br/trabalho-e-emprego/pt-br/assuntos/inspecao-do-trabalho/seguranca-e-saude-no-trabalho/normas-regulamentadoras)
  antes de usar para fins de auditoria. Não reproduzimos o texto legal
  completo de cada norma, só um catálogo com link para a fonte oficial
- Cada norma pode ser marcada como aplicável ou não à empresa, e recebe um
  checklist de itens de conformidade (descrição, status — conforme/não
  conforme/em andamento/não aplicável —, responsável e prazo)
- Catálogo e checklist são totalmente editáveis pela interface, então é
  possível corrigir qualquer norma e adicionar as que não vieram no seed
  (ex.: normas mais recentes)

## Próximos passos (ideias para continuar)

O roadmap original (7 fases) mais os módulos de CIPA e biblioteca de NRs
estão completos. Algumas ideias para quem quiser continuar evoluindo o
projeto:

- Login para funcionários (hoje só existe usuário administrador)
- Upload de arquivos (anexar o PDF do PGR/PCMSO, fotos de acidentes, lista
  de presença assinada da SIPAT)
- Notificações por e-mail quando um item estiver vencendo
- Gráficos no dashboard (ex.: Chart.js) além das tabelas atuais
- Migrar de SQLite para PostgreSQL para uso em produção
- Testes automatizados (pytest) cobrindo as rotas principais
- **Integração com o eSocial** (eventos S-2210/CAT, S-2220, S-2240): exige
  certificado digital e acesso ao webservice do governo, que não é possível
  configurar/testar neste ambiente. O caminho realista é modelar os campos
  dos eventos e gerar o XML no leiaute oficial, deixando a assinatura e
  transmissão para fora do sistema (ou para uma integração futura com
  certificado real)

## Aprendendo com este projeto

Cada fase é implementada de forma incremental, com commits organizados, para
que seja possível acompanhar como o sistema cresce peça por peça:
models → rotas → formulários → templates. Sinta-se à vontade para ler o
código de uma fase antes de pedir a próxima.
