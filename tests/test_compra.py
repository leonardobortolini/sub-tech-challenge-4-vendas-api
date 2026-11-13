from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

import pytest
from fastapi.testclient import TestClient

from app.application.portas.gateway_pagamento import (
    PagamentoSolicitado,
)
from app.infrastructure.database import get_db
from app.infrastructure.integracoes.veiculos_api import (
    ErroIntegracaoPagamento,
    VeiculoIndisponivel,
    VeiculoNaoEncontrado,
)
from app.main import app


@pytest.fixture
def client():
    app.dependency_overrides[get_db] = lambda: MagicMock()

    with TestClient(app) as cliente:
        yield cliente

    app.dependency_overrides.clear()


def test_solicitar_compra_com_sucesso(client, monkeypatch):
    veiculo_id = uuid4()
    pagamento_id = uuid4()

    class GatewayFake:
        def __init__(self, url_base):
            pass

        def solicitar_pagamento(self, veiculo_id, cpf):
            return PagamentoSolicitado(
                id=pagamento_id,
                valor=Decimal("50000.00"),
            )

    class RepositorioFake:
        def __init__(self, sessao):
            pass

        def salvar(self, venda):
            return venda

    monkeypatch.setattr(
        "app.interfaces.rotas.compra.GatewayPagamentoHTTP",
        GatewayFake,
    )

    monkeypatch.setattr(
        "app.interfaces.rotas.compra.RepositorioVendaSQLAlchemy",
        RepositorioFake,
    )

    resposta = client.post(
        "/compras",
        json={
            "veiculo_id": str(veiculo_id),
            "cpf": "12345678901",
        },
    )

    assert resposta.status_code == 201

    dados = resposta.json()

    assert dados["veiculo_id"] == str(veiculo_id)
    assert dados["pagamento_id"] == str(pagamento_id)
    assert dados["cpf_comprador"] == "12345678901"
    assert Decimal(dados["preco"]) == Decimal("50000.00")
    assert dados["status"] == "PENDENTE"


@pytest.mark.parametrize(
    ("erro", "status_code"),
    [
        (VeiculoNaoEncontrado, 404),
        (VeiculoIndisponivel, 409),
        (ErroIntegracaoPagamento, 502),
    ],
)
def test_tratamento_de_erros_na_compra(
    client,
    monkeypatch,
    erro,
    status_code,
):
    class GatewayFake:
        def __init__(self, url_base):
            pass

        def solicitar_pagamento(self, veiculo_id, cpf):
            raise erro("Falha simulada")

    monkeypatch.setattr(
        "app.interfaces.rotas.compra.GatewayPagamentoHTTP",
        GatewayFake,
    )

    resposta = client.post(
        "/compras",
        json={
            "veiculo_id": str(uuid4()),
            "cpf": "12345678901",
        },
    )

    assert resposta.status_code == status_code


def test_solicitar_compra_com_cpf_invalido(client):
    resposta = client.post(
        "/compras",
        json={
            "veiculo_id": str(uuid4()),
            "cpf": "123",
        },
    )

    assert resposta.status_code == 422
