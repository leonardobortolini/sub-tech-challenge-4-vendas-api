from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.casos_de_uso.solicitar_compra import (
    SolicitarCompra,
)
from app.application.portas.gateway_pagamento import (
    PagamentoSolicitado,
)
from app.domain.entidades.venda import StatusVenda


def test_solicitar_compra():
    repositorio = MagicMock()
    gateway = MagicMock()

    veiculo_id = uuid4()
    pagamento_id = uuid4()

    gateway.solicitar_pagamento.return_value = PagamentoSolicitado(
        id=pagamento_id,
        valor=Decimal("50000.00"),
    )

    repositorio.salvar.side_effect = lambda venda: venda

    caso_de_uso = SolicitarCompra(repositorio, gateway)

    resultado = caso_de_uso.executar(
        veiculo_id=veiculo_id,
        cpf="12345678901",
    )

    gateway.solicitar_pagamento.assert_called_once_with(
        veiculo_id=veiculo_id,
        cpf="12345678901",
    )

    repositorio.salvar.assert_called_once()

    assert resultado.veiculo_id == veiculo_id
    assert resultado.pagamento_id == pagamento_id
    assert resultado.preco == Decimal("50000.00")
    assert resultado.status == StatusVenda.PENDENTE


def test_nao_salvar_venda_quando_pagamento_falhar():
    repositorio = MagicMock()
    gateway = MagicMock()

    gateway.solicitar_pagamento.side_effect = Exception(
        "Falha na API de veículos"
    )

    caso_de_uso = SolicitarCompra(repositorio, gateway)

    try:
        caso_de_uso.executar(
            veiculo_id=uuid4(),
            cpf="12345678901",
        )
    except Exception as erro:
        assert str(erro) == "Falha na API de veículos"

    repositorio.salvar.assert_not_called()
