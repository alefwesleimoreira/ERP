from app import create_app, db
from app.models import *
import os

print("🔧 Verificando banco de dados...")

app = create_app()

with app.app_context():
    try:
        # Tentar acessar tabela de usuários
        from sqlalchemy import inspect
        inspector = inspect(db.engine)
        tables = inspector.get_table_names()
        
        if not tables:
            print("⚠️  Banco vazio! Criando tabelas...")
            db.create_all()
            print("✅ Tabelas criadas!")
            
            # Popular com dados
            print("📦 Populando com dados de exemplo...")
            import seed_data
            print("✅ Dados inseridos!")
        else:
            print(f"✅ Banco já inicializado! {len(tables)} tabelas encontradas.")
    except Exception as e:
        print(f"❌ Erro: {e}")
        print("🔧 Tentando criar tabelas...")
        db.create_all()
        print("✅ Tabelas criadas!")
