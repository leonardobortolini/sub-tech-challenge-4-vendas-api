from abc import ABC, abstractmethod
from uuid import UUID

from app.domain.entidades.venda import Venda


class RepositorioVenda(ABC):
    @abstractmethod
    def salvar(self, venda: Venda) -> Venda:
        raise NotImplementedError

    @abstractmethod
    def buscar_por_id(self, venda_id: UUID) -> Venda | None:
        raise NotImplementedError

    @abstractmethod
    def listar(self) -> list[Venda]:
        raise NotImplementedError


@abstractmethod
def buscar_por_pagamento_id(
    self,
    pagamento_id: UUID,
) -> Venda | None:
    raise NotImplementedError


@abstractmethod
def atualizar(self, venda: Venda) -> Venda | None:
    raise NotImplementedError
