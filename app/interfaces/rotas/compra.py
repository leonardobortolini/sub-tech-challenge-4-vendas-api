from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.application.casos_de_uso.consultar_venda import (
    ConsultarVenda,
    VendaNaoEncontrada,
)
from app.application.casos_de_uso.listar_vendas import ListarVendas
from app.application.casos_de_uso.processar_webhook_venda import (
    ProcessarWebhookVenda,
)
from app.application.casos_de_uso.solicitar_compra import (
    SolicitarCompra,
)
from app.domain.entidades.venda import (
    StatusVenda,
    TransicaoVendaInvalida,
)
from app.infrastructure.config import configuracoes
from app.infrastructure.database import get_db
from app.infrastructure.integracoes.veiculos_api import (
    ErroIntegracaoPagamento,
    GatewayPagamentoHTTP,
    VeiculoIndisponivel,
    VeiculoNaoEncontrado,
)
from app.infrastructure.repositorios.venda import (
    RepositorioVendaSQLAlchemy,
)
from app.interfaces.schemas.compra import (
    RespostaCompra,
    SolicitacaoCompra,
    WebhookPagamentoVenda,
)

compras_router = APIRouter(
    prefix="/compras",
    tags=["Compras"],
)


@compras_router.post(
    "",
    response_model=RespostaCompra,
    status_code=status.HTTP_201_CREATED,
    summary="Solicitar compra de veículo",
)
def solicitar_compra(
    dados: SolicitacaoCompra,
    banco: Session = Depends(get_db),
):
    repositorio = RepositorioVendaSQLAlchemy(banco)

    gateway = GatewayPagamentoHTTP(configuracoes.veiculos_api_url)

    caso_de_uso = SolicitarCompra(
        repositorio=repositorio,
        gateway_pagamento=gateway,
    )

    try:
        return caso_de_uso.executar(
            veiculo_id=dados.veiculo_id,
            cpf=dados.cpf,
        )

    except VeiculoNaoEncontrado:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Veículo não encontrado.",
        )

    except VeiculoIndisponivel:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Veículo indisponível para compra.",
        )

    except ErroIntegracaoPagamento:
        raise HTTPException(
            status_code=status.HTTP_502_BAD_GATEWAY,
            detail="Não foi possível processar o pagamento.",
        )


@compras_router.get(
    "",
    response_model=list[RespostaCompra],
    summary="Listar vendas",
)
def listar_vendas(
    banco: Session = Depends(get_db),
):
    repositorio = RepositorioVendaSQLAlchemy(banco)
    caso_de_uso = ListarVendas(repositorio)

    return caso_de_uso.executar()


@compras_router.get(
    "/{venda_id}",
    response_model=RespostaCompra,
    summary="Consultar venda por ID",
)
def consultar_venda(
    venda_id: UUID,
    banco: Session = Depends(get_db),
):
    repositorio = RepositorioVendaSQLAlchemy(banco)
    caso_de_uso = ConsultarVenda(repositorio)

    try:
        return caso_de_uso.executar(venda_id)
    except VendaNaoEncontrada:
        raise HTTPException(
            status_code=404,
            detail="Venda não encontrada.",
        ) from None


@compras_router.post(
    "/webhook/pagamento",
    response_model=RespostaCompra,
    summary="Receber atualização de pagamento",
)
def processar_webhook_venda(
    dados: WebhookPagamentoVenda,
    banco: Session = Depends(get_db),
):
    repositorio = RepositorioVendaSQLAlchemy(banco)

    caso_de_uso = ProcessarWebhookVenda(repositorio)

    novo_status = (
        StatusVenda.APROVADA
        if dados.status == "APROVADO"
        else StatusVenda.CANCELADA
    )

    try:
        return caso_de_uso.executar(
            pagamento_id=dados.pagamento_id,
            novo_status=novo_status,
        )

    except VendaNaoEncontrada:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Venda não encontrada.",
        ) from None

    except TransicaoVendaInvalida as erro:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(erro),
        ) from None
