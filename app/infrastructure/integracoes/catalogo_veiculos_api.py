from datetime import datetime
from decimal import Decimal, InvalidOperation
from uuid import UUID

import httpx

from app.application.portas.gateway_veiculos import (
    GatewayVeiculos,
    VeiculoCatalogo,
)


class ErroIntegracaoVeiculos(Exception):
    pass


class GatewayVeiculosHTTP(GatewayVeiculos):
    def __init__(self, url_base: str):
        self.url_base = url_base.rstrip("/")

    def listar_por_status(
        self,
        status: str,
    ) -> list[VeiculoCatalogo]:
        try:
            resposta = httpx.get(
                f"{self.url_base}/veiculos",
                params={"status": status},
                timeout=10.0,
            )

        except httpx.RequestError as erro:
            raise ErroIntegracaoVeiculos(
                "Não foi possível conectar à API de veículos."
            ) from erro

        if resposta.status_code != 200:
            raise ErroIntegracaoVeiculos(
                f"Erro ao consultar veículos: HTTP {resposta.status_code}."
            )

        try:
            dados = resposta.json()

            if not isinstance(dados, list):
                raise ValueError("Resposta inválida da API de veículos.")

            return [
                VeiculoCatalogo(
                    id=UUID(item["id"]),
                    marca=item["marca"],
                    modelo=item["modelo"],
                    ano=item["ano"],
                    cor=item["cor"],
                    preco=Decimal(str(item["preco"])),
                    status=item["status"],
                    criado_em=datetime.fromisoformat(
                        item["criado_em"].replace("Z", "+00:00")
                    ),
                    atualizado_em=datetime.fromisoformat(
                        item["atualizado_em"].replace("Z", "+00:00")
                    ),
                )
                for item in dados
            ]

        except (
            ValueError,
            KeyError,
            TypeError,
            AttributeError,
            InvalidOperation,
        ) as erro:
            raise ErroIntegracaoVeiculos(
                "Resposta inválida recebida da API de veículos."
            ) from erro
