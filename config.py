import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))


class Config:
    """Configurações da aplicação, lidas de variáveis de ambiente."""

    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-somente-para-desenvolvimento")
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        "DATABASE_URL", f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'sst.db')}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False
