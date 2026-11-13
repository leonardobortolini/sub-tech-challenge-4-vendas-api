
from unittest.mock import MagicMock
from uuid import uuid4

from app.application.casos_de_uso.listar_veiculos_disponiveis import (
    ListarVeiculosDisponiveis,
)
from app.application.casos_de_uso.listar_veiculos_vendidos import (
    ListarVeiculosVendidos,
)


def test_listar_veiculos_disponiveis():
    gateway = MagicMock()
    veiculos = [MagicMock(id=uuid4())]
    gateway.listar_por_status.return_value = veiculos

    caso_de_uso = ListarVeiculosDisponiveis(gateway)

    resultado = caso_de_uso.executar()

    gateway.listar_por_status.assert_called_once_with("DISPONIVEL")
    assert resultado == veiculos


def test_listar_veiculos_vendidos():
    gateway = MagicMock()
    veiculos = [MagicMock(id=uuid4())]
    gateway.listar_por_status.return_value = veiculos

    caso_de_uso = ListarVeiculosVendidos(gateway)

    resultado = caso_de_uso.executar()

    gateway.listar_por_status.assert_called_once_with("VENDIDO")
    assert resultado == veiculos
