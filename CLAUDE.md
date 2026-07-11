# Análise de Risco Georreferenciada

Avalia se uma propriedade rural possui restrições ambientais (embargo IBAMA,
sobreposição com Unidade de Conservação, etc.) como apoio à decisão de crédito
rural — inspirado na due diligence socioambiental usada por bancos e fintechs.

## Valor de negócio

A análise é **auditável** (mantém histórico dos resultados) e **explicável**
(o score de risco sempre acompanha os fatores que o geraram — nunca caixa preta),
requisitos típicos de compliance em crédito rural.

## Stack

- **Backend:** Python · FastAPI · SQLAlchemy · Alembic
- **Banco:** PostgreSQL · PostGIS
- **Frontend:** React · TypeScript · Vite · MapLibre GL · TailwindCSS · shadcn/ui
- **Tiles:** Martin
- **Estrutura:** monorepo (`backend/`, `frontend/`)

## Estrutura

```
backend/ API FastAPI, modelos SQLAlchemy, migrations Alembic
frontend/ SPA React + MapLibre
docker-compose.yml PostgreSQL + PostGIS (e tile server)
```

## Como rodar (dev)

```bash
docker compose up -d
cd backend && uv run alembic upgrade head && uv run fastapi dev
cd frontend && npm run dev
```
