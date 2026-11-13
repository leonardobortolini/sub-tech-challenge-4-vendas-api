
from datetime import datetime, timezone
from decimal import Decimal
from uuid import uuid4

import httpx
import pytest

from app.infrastructure.integracoes.catalogo_veiculos_api import (
    ErroIntegracaoVeiculos,
    GatewayVeiculosHTTP,
)


def criar_veiculo():
    return {
        "id": str(uuid4()),
        "marca": "Honda",
        "modelo": "Civic",
        "ano": 2025,
        "cor": "Preto",
        "preco": "120000.00",
        "status": "DISPONIVEL",
        "criado_em": datetime.now(timezone.utc).isoformat(),
        "atualizado_em": datetime.now(timezone.utc).isoformat(),
    }


def test_listar_por_status_com_sucesso(monkeypatch):
    dados = [criar_veiculo()]
    chamada = {}

    def mock_get(url, params, timeout):
        chamada["url"] = url
        chamada["params"] = params
        chamada["timeout"] = timeout
        return httpx.Response(
            200,
            json=dados,
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(httpx, "get", mock_get)

    gateway = GatewayVeiculosHTTP("http://veiculos-api:8000/")
    resultado = gateway.listar_por_status("DISPONIVEL")

    assert len(resultado) == 1
    assert resultado[0].marca == "Honda"
    assert resultado[0].modelo == "Civic"
    assert resultado[0].preco == Decimal("120000.00")
    assert resultado[0].status == "DISPONIVEL"
    assert chamada["url"] == "http://veiculos-api:8000/veiculos"
    assert chamada["params"] == {"status": "DISPONIVEL"}
    assert chamada["timeout"] == 10.0


def test_listar_por_status_com_erro_http(monkeypatch):
    def mock_get(url, params, timeout):
        return httpx.Response(
            500,
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(httpx, "get", mock_get)

    gateway = GatewayVeiculosHTTP("http://veiculos-api:8000")

    with pytest.raises(ErroIntegracaoVeiculos):
        gateway.listar_por_status("DISPONIVEL")


def test_listar_por_status_com_erro_de_conexao(monkeypatch):
    def mock_get(url, params, timeout):
        raise httpx.ConnectError("Falha de conexão")

    monkeypatch.setattr(httpx, "get", mock_get)

    gateway = GatewayVeiculosHTTP("http://veiculos-api:8000")

    with pytest.raises(ErroIntegracaoVeiculos):
        gateway.listar_por_status("DISPONIVEL")


def test_listar_por_status_com_resposta_invalida(monkeypatch):
    def mock_get(url, params, timeout):
        return httpx.Response(
            200,
            json={"erro": "resposta inválida"},
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(httpx, "get", mock_get)

    gateway = GatewayVeiculosHTTP("http://veiculos-api:8000")

    with pytest.raises(ErroIntegracaoVeiculos):
        gateway.listar_por_status("DISPONIVEL")


def test_listar_por_status_com_dados_invalidos(monkeypatch):
    def mock_get(url, params, timeout):
        return httpx.Response(
            200,
            json=[{"marca": "Honda"}],
            request=httpx.Request("GET", url),
        )

    monkeypatch.setattr(httpx, "get", mock_get)

    gateway = GatewayVeiculosHTTP("http://veiculos-api:8000")

    with pytest.raises(ErroIntegracaoVeiculos):
        gateway.listar_por_status("DISPONIVEL")
