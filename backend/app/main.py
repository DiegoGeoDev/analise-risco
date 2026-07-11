from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers import analises, propriedades

app = FastAPI(title="Análise de Risco Georreferenciada")

# CORS: o navegador bloqueia chamadas cross-origin por padrão. O dev server do
# Vite (5173) precisa de permissão explícita para chamar esta API.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(propriedades.router)
app.include_router(analises.router)


@app.get("/health")
def health():
    return {"status": "ok"}
