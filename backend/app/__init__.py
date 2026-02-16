from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_migrate import Migrate

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    
    # Carregar configurações
    from config import Config
    app.config.from_object(Config)
    
    # Inicializar extensões
    db.init_app(app)
    jwt.init_app(app)
    CORS(app)
    migrate.init_app(app, db)
    
    # Registrar blueprints
    from app.routes import auth, produtos, vendas, clientes, fornecedores, estoque, financeiro, dashboard
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(produtos.bp)
    app.register_blueprint(vendas.bp)
    app.register_blueprint(clientes.bp)
    app.register_blueprint(fornecedores.bp)
    app.register_blueprint(estoque.bp)
    app.register_blueprint(financeiro.bp)
    app.register_blueprint(dashboard.bp)
    
    return app

