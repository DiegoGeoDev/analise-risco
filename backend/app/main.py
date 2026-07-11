from fastapi import FastAPI

from app.routers import analises, propriedades

app = FastAPI(title="Análise de Risco Georreferenciada")

app.include_router(propriedades.router)
app.include_router(analises.router)


@app.get("/health")
def health():
    return {"status": "ok"}
