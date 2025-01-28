import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, "glossary.db")

# Можно задать переменную окружения, если захотим
SQLALCHEMY_DATABASE_URL = f"sqlite:///{DB_PATH}"

# Флаг, указывающий, надо ли инициализировать БД при старте
INIT_DB = os.getenv("INIT_DB", "False").lower() in ("true", "1", "yes")
