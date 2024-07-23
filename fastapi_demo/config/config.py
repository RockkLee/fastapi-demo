# DATABASE_URI = 'postgresql+psycopg2://postgres:1234@localhost/postgres'
from sqlalchemy import QueuePool

ENGINE_FUTURE = True
ENGINE_ECHO = True
ENGINE_POOLCLASS = QueuePool
ENGINE_POOL_SIZE = 10
ENGINE_MAX_OVERFLOW = 0

# 測試用"localhost"，docker用"db"
USER = "postgres"
PASSWORD = "1234"
# ip = "db"
IP = "localhost"
