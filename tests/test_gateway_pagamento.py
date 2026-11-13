from decimal import Decimal
from unittest.mock import Mock
from uuid import uuid4

import httpx
import pytest

from app.infrastructure.integracoes.veiculos_api import (
    ErroIntegracaoPagamento,
    GatewayPagamentoHTTP,
    VeiculoIndisponivel,
    VeiculoNaoEncontrado,
)


def criar_resposta(status_code, dados=None):
    return httpx.Response(
        status_code=status_code,
        json=dados or {},
        request=httpx.Request("POST", "http://veiculos-api/pagamentos"),
    )


def test_solicitar_pagamento_com_sucesso(monkeypatch):
    pagamento_id = uuid4()
    veiculo_id = uuid4()

    resposta = criar_resposta(
        201,
        {
            "id": str(pagamento_id),
            "veiculo_id": str(veiculo_id),
            "cpf": "12345678901",
            "valor": "50000.00",
            "status": "PENDENTE",
        },
    )

    requisicao = Mock(return_value=resposta)
    monkeypatch.setattr(httpx, "post", requisicao)

    gateway = GatewayPagamentoHTTP("http://veiculos-api")

    resultado = gateway.solicitar_pagamento(
        veiculo_id=veiculo_id,
        cpf="12345678901",
    )

    assert resultado.id == pagamento_id
    assert resultado.valor == Decimal("50000.00")

    requisicao.assert_called_once_with(
        "http://veiculos-api/pagamentos",
        json={
            "veiculo_id": str(veiculo_id),
            "cpf": "12345678901",
        },
        timeout=10.0,
    )


def test_veiculo_nao_encontrado(monkeypatch):
    resposta = criar_resposta(404)

    monkeypatch.setattr(
        httpx,
        "post",
        Mock(return_value=resposta),
    )

    gateway = GatewayPagamentoHTTP("http://veiculos-api")

    with pytest.raises(VeiculoNaoEncontrado):
        gateway.solicitar_pagamento(
            veiculo_id=uuid4(),
            cpf="12345678901",
        )


def test_veiculo_indisponivel(monkeypatch):
    resposta = criar_resposta(409)

    monkeypatch.setattr(
        httpx,
        "post",
        Mock(return_value=resposta),
    )

    gateway = GatewayPagamentoHTTP("http://veiculos-api")

    with pytest.raises(VeiculoIndisponivel):
        gateway.solicitar_pagamento(
            veiculo_id=uuid4(),
            cpf="12345678901",
        )


def test_erro_na_resposta_da_api(monkeypatch):
    resposta = criar_resposta(500)

    monkeypatch.setattr(
        httpx,
        "post",
        Mock(return_value=resposta),
    )

    gateway = GatewayPagamentoHTTP("http://veiculos-api")

    with pytest.raises(ErroIntegracaoPagamento):
        gateway.solicitar_pagamento(
            veiculo_id=uuid4(),
            cpf="12345678901",
        )


def test_falha_de_conexao_com_api(monkeypatch):
    def falhar_conexao(*args, **kwargs):
        requisicao = httpx.Request(
            "POST",
            "http://veiculos-api/pagamentos",
        )
        raise httpx.ConnectError(
            "Falha de conexão",
            request=requisicao,
        )

    monkeypatch.setattr(httpx, "post", falhar_conexao)

    gateway = GatewayPagamentoHTTP("http://veiculos-api")

    with pytest.raises(ErroIntegracaoPagamento):
        gateway.solicitar_pagamento(
            veiculo_id=uuid4(),
            cpf="12345678901",
        )
