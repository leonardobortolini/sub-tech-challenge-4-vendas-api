from dataclasses import dataclass
from decimal import Decimal
from typing import Protocol
from uuid import UUID


@dataclass(frozen=True)
class PagamentoSolicitado:
    id: UUID
    valor: Decimal


class GatewayPagamento(Protocol):
    def solicitar_pagamento(
        self,
        veiculo_id: UUID,
        cpf: str,
    ) -> PagamentoSolicitado: ...
