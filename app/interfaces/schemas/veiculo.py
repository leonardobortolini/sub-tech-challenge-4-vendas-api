from datetime import datetime
from decimal import Decimal
from uuid import UUID

from pydantic import BaseModel, ConfigDict


class RespostaVeiculo(BaseModel):
    id: UUID
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal
    status: str
    criado_em: datetime
    atualizado_em: datetime

    model_config = ConfigDict(from_attributes=True)
