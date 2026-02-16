from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate
from sqlalchemy import inspect
from config import Config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def _bootstrap_demo_admin(app):
    """Garante um usuário admin demo para primeiro acesso em ambientes novos."""
    auto_seed = app.config.get('AUTO_SEED_DEMO_ADMIN', True)
    if not auto_seed:
        return

    from app.models import Usuario

    inspector = inspect(db.engine)
    if not inspector.has_table('usuarios'):
        return

    if Usuario.query.filter_by(email='admin@loja.com').first():
        return

    admin = Usuario(nome='Administrador', email='admin@loja.com', tipo='admin', ativo=True)
    admin.set_senha('admin123')
    db.session.add(admin)
    db.session.commit()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Inicializar extensões
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)
    
    # Registrar blueprints
    from app.routes import auth, produtos, vendas, estoque, clientes, fornecedores, financeiro, dashboard
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(produtos.bp)
    app.register_blueprint(vendas.bp)
    app.register_blueprint(estoque.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(fornecedores.bp)
    app.register_blueprint(financeiro.bp)
    app.register_blueprint(dashboard.bp)

with app.app_context():
     _bootstrap_demo_admin(app)
    
    return app
