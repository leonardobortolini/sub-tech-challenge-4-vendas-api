from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://vendas:vendas@localhost:5433/vendas"
    )

    veiculos_api_url: str = "http://localhost:8000"

    model_config = SettingsConfigDict(
        extra="ignore",
    )


configuracoes = Configuracoes()
