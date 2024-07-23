from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker

from fastapi_demo.config import config
from fastapi_demo.config.config import ENGINE_POOLCLASS, ENGINE_FUTURE, ENGINE_ECHO, ENGINE_POOL_SIZE, \
    ENGINE_MAX_OVERFLOW

# Sync setting
# DATABASE_URI = 'postgresql+psycopg2://%s:%s@%s/postgres' % (config.user, config.password, config.ip)
# engine = create_engine(DATABASE_URI)
# Session = sessionmaker(bind=engine)

# Async setting
DATABASE_URI = 'postgresql+asyncpg://%s:%s@%s/postgres' % (config.USER, config.PASSWORD, config.IP)
engine = create_async_engine(
    DATABASE_URI,
    future=ENGINE_FUTURE,  # Allow a seamless shift from prior versions of SQLAlchemy to the new v2.0
    echo=ENGINE_ECHO,
    poolclass=ENGINE_POOLCLASS,
    pool_size=ENGINE_POOL_SIZE,
    max_overflow=ENGINE_MAX_OVERFLOW
)
async_session = async_sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)


async def get_session() -> AsyncSession:
    async with async_session() as session:
        yield session
