from app.domain.entidades.venda import Venda
from app.domain.repositorios.venda import RepositorioVenda


class ListarVendas:
    def __init__(self, repositorio: RepositorioVenda):
        self.repositorio = repositorio

    def executar(self) -> list[Venda]:
        return self.repositorio.listar()
