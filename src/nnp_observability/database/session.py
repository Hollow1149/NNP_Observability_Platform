from sqlalchemy import create_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from nnp_observability.core.config import settings

DATABASE_URL: str = settings.DATABASE_URL

engine = create_engine(
    DATABASE_URL, pool_size=10, max_overflow=20, pool_pre_ping=True, pool_recycle=1800
)

SessionLocal = sessionmaker(bind=engine, autoflush=False, expire_on_commit=False)


class Base(DeclarativeBase):
    pass


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# TODO: When model is ready use it to initialize the db
def init_db():
    some: bool = True
    yield some
