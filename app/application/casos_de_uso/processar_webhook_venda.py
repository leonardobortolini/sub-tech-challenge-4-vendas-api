from uuid import UUID

from app.application.casos_de_uso.consultar_venda import (
    VendaNaoEncontrada,
)
from app.domain.entidades.venda import (
    StatusVenda,
    Venda,
)
from app.domain.repositorios.venda import RepositorioVenda


class ProcessarWebhookVenda:
    def __init__(self, repositorio: RepositorioVenda):
        self.repositorio = repositorio

    def executar(
        self,
        pagamento_id: UUID,
        novo_status: StatusVenda,
    ) -> Venda:
        venda = self.repositorio.buscar_por_pagamento_id(pagamento_id)

        if venda is None:
            raise VendaNaoEncontrada(
                "Venda não encontrada para este pagamento."
            )

        venda.atualizar_status(novo_status)

        venda_atualizada = self.repositorio.atualizar(venda)

        if venda_atualizada is None:
            raise VendaNaoEncontrada("Venda não encontrada.")

        return venda_atualizada
