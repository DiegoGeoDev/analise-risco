from fastapi import FastAPI

app = FastAPI(title="Análise de Risco Georreferenciada")


@app.get("/health")
def health():
    return {"status": "ok"}
