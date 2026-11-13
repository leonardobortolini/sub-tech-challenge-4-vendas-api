from collections.abc import Generator

from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, Session, sessionmaker

from app.infrastructure.config import configuracoes

engine = create_engine(
    configuracoes.database_url,
    pool_pre_ping=True,
)


SessaoBanco = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine,
)


class Base(DeclarativeBase):
    pass


def get_db() -> Generator[Session, None, None]:
    banco = SessaoBanco()

    try:
        yield banco
    finally:
        banco.close()
