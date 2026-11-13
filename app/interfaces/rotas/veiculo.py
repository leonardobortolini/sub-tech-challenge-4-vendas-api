from fastapi import APIRouter, HTTPException, status

from app.application.casos_de_uso.listar_veiculos_disponiveis import (
    ListarVeiculosDisponiveis,
)
from app.application.casos_de_uso.listar_veiculos_vendidos import (
    ListarVeiculosVendidos,
)
from app.infrastructure.config import configuracoes
from app.infrastructure.integracoes.catalogo_veiculos_api import (
    ErroIntegracaoVeiculos,
    GatewayVeiculosHTTP,
)
from app.interfaces.schemas.veiculo import RespostaVeiculo

veiculos_router = APIRouter(
    prefix="/veiculos",
    tags=["Veículos"],
)


@veiculos_router.get(
    "/disponiveis",
    response_model=list[RespostaVeiculo],
    summary="Listar veículos disponíveis",
)
def listar_veiculos_disponiveis():
    gateway = GatewayVeiculosHTTP(configuracoes.veiculos_api_url)
    caso_de_uso = ListarVeiculosDisponiveis(gateway)

    try:
        return caso_de_uso.executar()

    except ErroIntegracaoVeiculos as erro:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Não foi possível consultar os veículos disponíveis.",
        ) from erro


@veiculos_router.get(
    "/vendidos",
    response_model=list[RespostaVeiculo],
    summary="Listar veículos vendidos",
)
def listar_veiculos_vendidos():
    gateway = GatewayVeiculosHTTP(configuracoes.veiculos_api_url)
    caso_de_uso = ListarVeiculosVendidos(gateway)

    try:
        return caso_de_uso.executar()

    except ErroIntegracaoVeiculos as erro:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Não foi possível consultar os veículos vendidos.",
        ) from erro
