
from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from fastapi.testclient import TestClient

from app.interfaces.rotas import veiculo as rotas_veiculo
from app.main import app

client = TestClient(app)


def criar_veiculo(status="DISPONIVEL"):
    agora = datetime.now(timezone.utc)
    return {
        "id": uuid4(),
        "marca": "Honda",
        "modelo": "Civic",
        "ano": 2025,
        "cor": "Preto",
        "preco": Decimal("120000.00"),
        "status": status,
        "criado_em": agora,
        "atualizado_em": agora,
    }


def test_listar_veiculos_disponiveis(monkeypatch):
    veiculos = [criar_veiculo("DISPONIVEL")]
    gateway = MagicMock()
    gateway.listar_por_status.return_value = veiculos

    monkeypatch.setattr(
        rotas_veiculo,
        "GatewayVeiculosHTTP",
        lambda url: gateway,
    )

    resposta = client.get("/veiculos/disponiveis")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["status"] == "DISPONIVEL"
    gateway.listar_por_status.assert_called_once_with("DISPONIVEL")


def test_listar_veiculos_vendidos(monkeypatch):
    veiculos = [criar_veiculo("VENDIDO")]
    gateway = MagicMock()
    gateway.listar_por_status.return_value = veiculos

    monkeypatch.setattr(
        rotas_veiculo,
        "GatewayVeiculosHTTP",
        lambda url: gateway,
    )

    resposta = client.get("/veiculos/vendidos")

    assert resposta.status_code == 200
    assert len(resposta.json()) == 1
    assert resposta.json()[0]["status"] == "VENDIDO"
    gateway.listar_por_status.assert_called_once_with("VENDIDO")


def test_listar_veiculos_disponiveis_com_erro_de_integracao(monkeypatch):
    gateway = MagicMock()
    gateway.listar_por_status.side_effect = (
        rotas_veiculo.ErroIntegracaoVeiculos("Falha na integração")
    )

    monkeypatch.setattr(
        rotas_veiculo,
        "GatewayVeiculosHTTP",
        lambda url: gateway,
    )

    resposta = client.get("/veiculos/disponiveis")

    assert resposta.status_code == 502
    assert resposta.json()["detail"] == (
        "Não foi possível consultar os veículos disponíveis."
    )


def test_listar_veiculos_vendidos_com_erro_de_integracao(monkeypatch):
    gateway = MagicMock()
    gateway.listar_por_status.side_effect = (
        rotas_veiculo.ErroIntegracaoVeiculos("Falha na integração")
    )

    monkeypatch.setattr(
        rotas_veiculo,
        "GatewayVeiculosHTTP",
        lambda url: gateway,
    )

    resposta = client.get("/veiculos/vendidos")

    assert resposta.status_code == 502
    assert resposta.json()["detail"] == (
        "Não foi possível consultar os veículos vendidos."
    )
