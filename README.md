# Zeladoria SJP — MVP

Plataforma de registro e gestão de reclamações e solicitações de zeladoria urbana para a Prefeitura de **São José dos Pinhais (PR)**.

Permite que o cidadão relate problemas de infraestrutura urbana (iluminação, pavimentação, coleta de lixo, riscos de segurança, etc.) com geolocalização e fotos, e que a gestão municipal acompanhe, roteie para a secretaria responsável e monitore prazos de atendimento.

## Stack tecnológica

| Camada | Tecnologia | Motivo |
|---|---|---|
| Mobile (Cidadão) | **React Native + Expo** (TypeScript) | Deploy rápido em Android/iOS, acesso simples a GPS/câmera, curva de aprendizado baixa, forte ecossistema de bibliotecas (`expo-location`, `expo-image-picker`) |
| Backend / API | **Node.js + Express** (TypeScript) | Simplicidade, tipagem forte, fácil de hospedar em qualquer PaaS (Railway, Render, AWS) |
| Banco de dados | **PostgreSQL + Prisma ORM** | Dados relacionais (usuários, chamados, secretarias, histórico de status), migrations versionadas, suporte a geolocalização (`lat`/`lng`) |
| Armazenamento de fotos | **S3-compatible (AWS S3 / Supabase Storage / Cloudinary)** | Evidências fotográficas dos chamados, fora do banco relacional |
| Autenticação | **JWT** (com bcrypt para hash de senha) | Simples, stateless, fácil de integrar no app mobile |
| Painel administrativo | **Next.js (React)** | Dashboard web para gestão municipal, SSR para métricas |

> **Alternativa "serverless" para acelerar ainda mais o MVP:** trocar Node.js/Postgres/S3 por **Supabase** (Postgres gerenciado + Auth + Storage + Realtime em um único serviço) ou **Firebase** (Firestore + Auth + Storage). O modelo de dados deste repositório (`backend/prisma/schema.prisma`) foi desenhado para migrar com poucas mudanças para qualquer uma dessas opções.

## Estrutura do repositório

```
.
├── backend/     # API REST (Node.js + Express + Prisma)
├── mobile/      # App do cidadão (React Native + Expo)
├── admin/       # Painel de gestão municipal (Next.js) — dashboard e roteamento de tickets
└── docs/        # Documentação de arquitetura e modelagem
```

Veja o detalhamento completo em [`docs/ARQUITETURA.md`](docs/ARQUITETURA.md) e a modelagem de dados em [`backend/prisma/schema.prisma`](backend/prisma/schema.prisma).

## Módulos desta primeira iteração

### Cidadão (mobile)
- Autenticação (login/cadastro) — `mobile/src/screens/LoginScreen.tsx`, `CadastroScreen.tsx`
- Nova ocorrência com GPS automático + fotos — `mobile/src/screens/NovaOcorrenciaScreen.tsx`
- Histórico e status do chamado — `mobile/src/screens/HistoricoScreen.tsx`

### Administrativo (web)
- Estrutura de dados para roteamento de chamados por secretaria (`Secretaria`, `Chamado.secretariaId`)
- Dashboard inicial de métricas — `admin/src/pages/dashboard.tsx`

### API
- `POST /api/chamados` — cria um chamado (recebe geolocalização, categoria, descrição, fotos)
- `GET /api/chamados` — lista chamados (com filtro por status/cidadão)
- `PATCH /api/chamados/:id/status` — atualiza status (uso administrativo)

## Como rodar localmente

### Backend
```bash
cd backend
cp .env.example .env   # ajuste DATABASE_URL e JWT_SECRET
npm install
npx prisma migrate dev --name init
npm run dev             # http://localhost:3333
```

### Mobile
```bash
cd mobile
cp .env.example .env    # ajuste EXPO_PUBLIC_API_URL
npm install
npx expo start
```

## Roadmap (próximas iterações)

- **Triagem automática com IA**: classificar a descrição do chamado via LLM para sugerir categoria/secretaria automaticamente, reduzindo o tempo até o primeiro atendimento.
- **Gamificação cívica**: pontuação para cidadãos com chamados verificados e resolvidos, ranking de bairros mais colaborativos.
- **Mapa de calor público**: visualização web aberta com densidade de chamados por região/categoria, promovendo transparência.
- **Notificações push** de mudança de status do chamado.
- **SLA por secretaria** com alertas de atraso no painel administrativo.
