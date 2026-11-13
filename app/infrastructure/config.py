
from pydantic_settings import BaseSettings, SettingsConfigDict


class Configuracoes(BaseSettings):
    database_url: str = (
        "postgresql+psycopg://vendas:vendas@localhost:5433/vendas"
    )

    model_config = SettingsConfigDict(
        extra="ignore",
    )


configuracoes = Configuracoes()
