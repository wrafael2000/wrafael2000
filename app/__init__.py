import os

from flask import Flask

from config import Config

from .extensions import csrf, db, login_manager


def create_app(config_class=Config):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(config_class)
    os.makedirs(app.instance_path, exist_ok=True)

    db.init_app(app)
    login_manager.init_app(app)
    csrf.init_app(app)

    with app.app_context():
        from . import models  # noqa: F401  (garante que os models sejam registrados)
        from .cli import registrar_comandos
        from .routes.acidentes import acidentes_bp
        from .routes.auth import auth_bp
        from .routes.documentos import documentos_bp
        from .routes.entregas_epi import entregas_epi_bp
        from .routes.epis import epis_bp
        from .routes.exames import exames_bp
        from .routes.funcionarios import funcionarios_bp
        from .routes.main import main_bp
        from .routes.setores import setores_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(setores_bp)
        app.register_blueprint(funcionarios_bp)
        app.register_blueprint(epis_bp)
        app.register_blueprint(entregas_epi_bp)
        app.register_blueprint(acidentes_bp)
        app.register_blueprint(exames_bp)
        app.register_blueprint(documentos_bp)

        registrar_comandos(app)

        db.create_all()

    return app
