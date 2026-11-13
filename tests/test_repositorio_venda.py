from datetime import datetime, timezone
from decimal import Decimal
from unittest.mock import MagicMock
from uuid import uuid4

from app.domain.entidades.venda import StatusVenda, Venda
from app.infrastructure.models.venda import VendaModelo
from app.infrastructure.repositorios.venda import (
    RepositorioVendaSQLAlchemy,
)


def criar_venda_modelo():
    return VendaModelo(
        id=uuid4(),
        veiculo_id=uuid4(),
        cpf_comprador="12345678901",
        preco=Decimal("50000.00"),
        status=StatusVenda.PENDENTE,
        criado_em=datetime.now(timezone.utc),
        atualizado_em=datetime.now(timezone.utc),
        pagamento_id=uuid4(),
    )


def test_salvar_venda():
    sessao = MagicMock()
    repositorio = RepositorioVendaSQLAlchemy(sessao)

    venda = Venda(
        veiculo_id=uuid4(),
        pagamento_id=uuid4(),
        cpf_comprador="12345678901",
        preco=Decimal("50000.00"),
    )

    resultado = repositorio.salvar(venda)

    assert resultado.id == venda.id
    assert resultado.veiculo_id == venda.veiculo_id
    assert resultado.preco == venda.preco
    assert resultado.status == StatusVenda.PENDENTE

    sessao.add.assert_called_once()
    sessao.commit.assert_called_once()
    sessao.refresh.assert_called_once()


def test_buscar_venda_por_id():
    sessao = MagicMock()
    repositorio = RepositorioVendaSQLAlchemy(sessao)

    modelo = criar_venda_modelo()
    sessao.get.return_value = modelo

    resultado = repositorio.buscar_por_id(modelo.id)

    assert resultado is not None
    assert resultado.id == modelo.id
    assert resultado.cpf_comprador == modelo.cpf_comprador

    sessao.get.assert_called_once_with(VendaModelo, modelo.id)


def test_buscar_venda_inexistente():
    sessao = MagicMock()
    repositorio = RepositorioVendaSQLAlchemy(sessao)

    sessao.get.return_value = None

    resultado = repositorio.buscar_por_id(uuid4())

    assert resultado is None


def test_listar_vendas():
    sessao = MagicMock()
    repositorio = RepositorioVendaSQLAlchemy(sessao)

    modelos = [
        criar_venda_modelo(),
        criar_venda_modelo(),
    ]

    sessao.scalars.return_value.all.return_value = modelos

    resultado = repositorio.listar()

    assert len(resultado) == 2
    assert resultado[0].id == modelos[0].id
    assert resultado[1].id == modelos[1].id


def test_listar_vendas_vazio():
    sessao = MagicMock()
    repositorio = RepositorioVendaSQLAlchemy(sessao)

    sessao.scalars.return_value.all.return_value = []

    resultado = repositorio.listar()

    assert resultado == []
