from uuid import UUID

from app.application.portas.gateway_pagamento import GatewayPagamento
from app.domain.entidades.venda import Venda
from app.domain.repositorios.venda import RepositorioVenda


class SolicitarCompra:
    def __init__(
        self,
        repositorio: RepositorioVenda,
        gateway_pagamento: GatewayPagamento,
    ):
        self.repositorio = repositorio
        self.gateway_pagamento = gateway_pagamento

    def executar(
        self,
        veiculo_id: UUID,
        cpf: str,
    ) -> Venda:
        pagamento = self.gateway_pagamento.solicitar_pagamento(
            veiculo_id=veiculo_id,
            cpf=cpf,
        )

        venda = Venda(
            veiculo_id=veiculo_id,
            pagamento_id=pagamento.id,
            cpf_comprador=cpf,
            preco=pagamento.valor,
        )

        return self.repositorio.salvar(venda)
