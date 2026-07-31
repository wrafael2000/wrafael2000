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
        from .routes.aplicacoes import aplicacoes_bp
        from .routes.auth import auth_bp
        from .routes.cipa import cipa_bp
        from .routes.documentos import documentos_bp
        from .routes.entregas_epi import entregas_epi_bp
        from .routes.epis import epis_bp
        from .routes.exames import exames_bp
        from .routes.funcionarios import funcionarios_bp
        from .routes.main import main_bp
        from .routes.normas import normas_bp
        from .routes.pesquisa_publica import pesquisa_publica_bp
        from .routes.questionarios import questionarios_bp
        from .routes.realizacoes_treinamento import realizacoes_treinamento_bp
        from .routes.reunioes_cipa import reunioes_cipa_bp
        from .routes.setores import setores_bp
        from .routes.sipat import sipat_bp
        from .routes.treinamentos import treinamentos_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)
        app.register_blueprint(setores_bp)
        app.register_blueprint(funcionarios_bp)
        app.register_blueprint(epis_bp)
        app.register_blueprint(entregas_epi_bp)
        app.register_blueprint(acidentes_bp)
        app.register_blueprint(exames_bp)
        app.register_blueprint(documentos_bp)
        app.register_blueprint(treinamentos_bp)
        app.register_blueprint(realizacoes_treinamento_bp)
        app.register_blueprint(questionarios_bp)
        app.register_blueprint(aplicacoes_bp)
        app.register_blueprint(pesquisa_publica_bp)
        app.register_blueprint(cipa_bp)
        app.register_blueprint(reunioes_cipa_bp)
        app.register_blueprint(sipat_bp)
        app.register_blueprint(normas_bp)

        registrar_comandos(app)

        db.create_all()

    return app
