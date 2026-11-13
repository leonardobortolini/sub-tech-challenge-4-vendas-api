from datetime import datetime
from decimal import Decimal
from typing import Literal
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field

from app.domain.entidades.venda import StatusVenda


class SolicitacaoCompra(BaseModel):
    veiculo_id: UUID
    cpf: str = Field(
        min_length=11,
        max_length=11,
        pattern=r"^\d{11}$",
        description="CPF do comprador, contendo 11 dígitos",
    )


class RespostaCompra(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    veiculo_id: UUID
    pagamento_id: UUID
    cpf_comprador: str
    preco: Decimal
    status: StatusVenda
    criado_em: datetime
    atualizado_em: datetime


class WebhookPagamentoVenda(BaseModel):
    pagamento_id: UUID
    status: Literal["APROVADO", "CANCELADO"]
