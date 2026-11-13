from decimal import Decimal
from uuid import UUID

import httpx

from app.application.portas.gateway_pagamento import (
    GatewayPagamento,
    PagamentoSolicitado,
)


class VeiculoNaoEncontrado(Exception):
    pass


class VeiculoIndisponivel(Exception):
    pass


class ErroIntegracaoPagamento(Exception):
    pass


class GatewayPagamentoHTTP(GatewayPagamento):
    def __init__(self, url_base: str):
        self.url_base = url_base.rstrip("/")

    def solicitar_pagamento(
        self,
        veiculo_id: UUID,
        cpf: str,
    ) -> PagamentoSolicitado:
        try:
            resposta = httpx.post(
                f"{self.url_base}/pagamentos",
                json={
                    "veiculo_id": str(veiculo_id),
                    "cpf": cpf,
                },
                timeout=10.0,
            )

        except httpx.RequestError as erro:
            raise ErroIntegracaoPagamento(
                "Não foi possível conectar à API de veículos."
            ) from erro

        if resposta.status_code == 404:
            raise VeiculoNaoEncontrado("Veículo não encontrado.")

        if resposta.status_code == 409:
            raise VeiculoIndisponivel("Veículo indisponível para compra.")

        if resposta.status_code != 201:
            raise ErroIntegracaoPagamento(
                f"Erro ao solicitar pagamento: HTTP {resposta.status_code}."
            )

        dados = resposta.json()

        return PagamentoSolicitado(
            id=UUID(dados["id"]),
            valor=Decimal(str(dados["valor"])),
        )
