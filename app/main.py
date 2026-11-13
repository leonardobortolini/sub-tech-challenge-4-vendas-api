from fastapi import FastAPI

from app.interfaces.rotas.compra import compras_router

app = FastAPI(title="Vendas API")

app.include_router(compras_router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "healthy", "service": "vendas-api"}
