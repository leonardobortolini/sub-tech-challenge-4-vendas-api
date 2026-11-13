from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from uuid import UUID


@dataclass
class VeiculoCatalogo:
    id: UUID
    marca: str
    modelo: str
    ano: int
    cor: str
    preco: Decimal
    status: str
    criado_em: datetime
    atualizado_em: datetime


class GatewayVeiculos(ABC):
    @abstractmethod
    def listar_por_status(
        self,
        status: str,
    ) -> list[VeiculoCatalogo]:
        pass
