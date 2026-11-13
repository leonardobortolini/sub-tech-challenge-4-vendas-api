from uuid import UUID

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.domain.entidades.venda import Venda
from app.domain.repositorios.venda import RepositorioVenda
from app.infrastructure.models.venda import VendaModelo


class RepositorioVendaSQLAlchemy(RepositorioVenda):
    def __init__(self, sessao: Session):
        self.sessao = sessao

    def salvar(self, venda: Venda) -> Venda:
        modelo = VendaModelo(
            id=venda.id,
            veiculo_id=venda.veiculo_id,
            cpf_comprador=venda.cpf_comprador,
            preco=venda.preco,
            status=venda.status,
            criado_em=venda.criado_em,
            atualizado_em=venda.atualizado_em,
            pagamento_id=venda.pagamento_id,
        )

        self.sessao.add(modelo)
        self.sessao.commit()
        self.sessao.refresh(modelo)

        return self._converter_para_entidade(modelo)

    def buscar_por_id(self, venda_id: UUID) -> Venda | None:
        modelo = self.sessao.get(VendaModelo, venda_id)

        if modelo is None:
            return None

        return self._converter_para_entidade(modelo)

    def buscar_por_pagamento_id(
        self,
        pagamento_id: UUID,
    ) -> Venda | None:
        consulta = select(VendaModelo).where(
            VendaModelo.pagamento_id == pagamento_id
        )

        modelo = self.sessao.scalar(consulta)

        if modelo is None:
            return None

        return self._converter_para_entidade(modelo)

    def atualizar(self, venda: Venda) -> Venda | None:
        modelo = self.sessao.get(VendaModelo, venda.id)

        if modelo is None:
            return None

        modelo.status = venda.status
        modelo.atualizado_em = venda.atualizado_em

        self.sessao.commit()
        self.sessao.refresh(modelo)

        return self._converter_para_entidade(modelo)

    def listar(self) -> list[Venda]:
        consulta = select(VendaModelo).order_by(VendaModelo.criado_em.desc())

        modelos = self.sessao.scalars(consulta).all()

        return [self._converter_para_entidade(modelo) for modelo in modelos]

    @staticmethod
    def _converter_para_entidade(modelo: VendaModelo) -> Venda:
        return Venda(
            id=modelo.id,
            veiculo_id=modelo.veiculo_id,
            cpf_comprador=modelo.cpf_comprador,
            preco=modelo.preco,
            status=modelo.status,
            criado_em=modelo.criado_em,
            atualizado_em=modelo.atualizado_em,
            pagamento_id=modelo.pagamento_id,
        )
