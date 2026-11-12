from fastapi import FastAPI

app = FastAPI(
    title="Vendas API"
)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "vendas-api"}