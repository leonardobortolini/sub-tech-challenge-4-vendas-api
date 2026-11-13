from app.application.portas.gateway_veiculos import (
    GatewayVeiculos,
    VeiculoCatalogo,
)


class ListarVeiculosVendidos:
    def __init__(self, gateway: GatewayVeiculos):
        self.gateway = gateway

    def executar(self) -> list[VeiculoCatalogo]:
        return self.gateway.listar_por_status("VENDIDO")
