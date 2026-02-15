cd /workspaces/ERP/backend

# Fazer backup
cp config.py config.py.backup

# Substituir conteúdo
cat > config.py << 'EOF'
import os
from datetime import timedelta

class Config:
    # Configurações gerais
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    
    # Configurações do banco de dados PostgreSQL (psycopg3)
    database_url = os.environ.get('DATABASE_URL') or \
        'postgresql://postgres:senha@localhost/erp_roupas_infantis'
    
    # Ajustar para psycopg3
    if database_url and database_url.startswith('postgres://'):
        database_url = database_url.replace('postgres://', 'postgresql+psycopg://')
    elif database_url and database_url.startswith('postgresql://'):
        database_url = database_url.replace('postgresql://', 'postgresql+psycopg://')
    
    SQLALCHEMY_DATABASE_URI = database_url
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    
    # Configurações JWT
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-key-change-in-production'
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    
    # Configurações de upload
    UPLOAD_FOLDER = 'uploads/produtos'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Configurações do e-commerce
    MOEDA = 'BRL'
    FRETE_GRATIS_ACIMA = 200.00
    ESTOQUE_MINIMO_ALERTA = 5
EOF


