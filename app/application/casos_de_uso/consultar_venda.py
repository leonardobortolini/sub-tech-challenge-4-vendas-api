from uuid import UUID

from app.domain.entidades.venda import Venda
from app.domain.repositorios.venda import RepositorioVenda


class VendaNaoEncontrada(Exception):
    pass


class ConsultarVenda:
    def __init__(self, repositorio: RepositorioVenda):
        self.repositorio = repositorio

    def executar(self, venda_id: UUID) -> Venda:
        venda = self.repositorio.buscar_por_id(venda_id)

        if venda is None:
            raise VendaNaoEncontrada("Venda não encontrada.")

        return venda
