from dataclasses import dataclass
from datetime import datetime, timezone
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4


class StatusVenda(str, Enum):
    PENDENTE = "PENDENTE"
    APROVADA = "APROVADA"
    CANCELADA = "CANCELADA"


class TransicaoVendaInvalida(Exception):
    pass


@dataclass
class Venda:
    veiculo_id: UUID
    pagamento_id: UUID
    cpf_comprador: str
    preco: Decimal
    id: UUID = None
    status: StatusVenda = StatusVenda.PENDENTE
    criado_em: datetime = None
    atualizado_em: datetime = None

    def __post_init__(self) -> None:
        if self.id is None:
            self.id = uuid4()

        agora = datetime.now(timezone.utc)

        if self.criado_em is None:
            self.criado_em = agora

        if self.atualizado_em is None:
            self.atualizado_em = agora

    def atualizar_status(self, novo_status: StatusVenda) -> None:
        if novo_status == self.status:
            return

        if self.status != StatusVenda.PENDENTE:
            raise TransicaoVendaInvalida(
                "Não é possível alterar uma venda já finalizada."
            )

        if novo_status == StatusVenda.PENDENTE:
            raise TransicaoVendaInvalida(
                "O webhook não pode definir a venda como pendente."
            )

        self.status = novo_status
        self.atualizado_em = datetime.now(timezone.utc)
