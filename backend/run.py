from app import create_app, db
from app.models import *
import os

app = create_app()

# Inicializar banco automaticamente
if os.environ.get('FLASK_ENV') == 'production':
    with app.app_context():
        try:
            db.create_all()
            print("✅ Banco de dados verificado/criado!")
        except Exception as e:
            print(f"⚠️  Aviso: {e}")

@app.route('/')
def index():
    return {
        'mensagem': '🛍️ ERP Roupas Infantis - API',
        'versao': '1.0.0',
        'status': 'online',
        'init_url': '/init-db'
    }

@app.route('/init-db')
def init_database():
    """Inicializa banco com dados de exemplo - execute UMA VEZ apenas!"""
    try:
        from datetime import datetime, timedelta
        import random
        from werkzeug.security import generate_password_hash
        
        # Verificar se já tem dados
        if Usuario.query.first():
            return {'erro': 'Banco já inicializado!'}, 400
        
        # Criar usuários
        admin = Usuario(
            nome='Administrador',
            email='admin@loja.com',
            tipo='admin',
        )

        admin.set_senha('admin123')
        
        db.session.add(admin)
        
        # Criar categorias
        categorias = [
            Categoria(nome='Bodies', descricao='Bodies para bebês'),
            Categoria(nome='Macacões', descricao='Macacões infantis'),
            Categoria(nome='Conjuntos', descricao='Conjuntos de roupas'),
        ]
        for cat in categorias:
            db.session.add(cat)
        
        db.session.commit()
        
        # Criar produtos
        produtos_data = [
            {'nome': 'Body Manga Curta', 'categoria_id': 1, 'preco': 29.90},
            {'nome': 'Macacão Longo', 'categoria_id': 2, 'preco': 79.90},
            {'nome': 'Conjunto Verão', 'categoria_id': 3, 'preco': 59.90},
        ]
        
        for p_data in produtos_data:
            produto = Produto(
                codigo=f'PROD{random.randint(1000,9999)}',
                nome=p_data['nome'],
                descricao='Produto de qualidade',
                categoria_id=p_data['categoria_id'],
                preco_custo=p_data['preco'] * 0.5,
                preco_venda=p_data['preco'],
                estoque_atual=50,
                estoque_minimo=10,
                genero='unissex',
                faixa_etaria='0-6 meses',
                ativo=True
            )
            db.session.add(produto)
        
        db.session.commit()
        
        return {
            'sucesso': True,
            'mensagem': '✅ Banco inicializado com sucesso!',
            'usuarios': 1,
            'categorias': len(categorias),
            'produtos': len(produtos_data)
        }
        
    except Exception as e:
        db.session.rollback()
        return {'erro': str(e)}, 500

@app.route('/health')
def health():
    return {'status': 'ok'}

@app.shell_context_processor
def make_shell_context():
    return {
        'db': db,
        'Usuario': Usuario,
        'Cliente': Cliente,
        'Fornecedor': Fornecedor,
        'Produto': Produto,
        'Categoria': Categoria,
        'Venda': Venda,
        'ItemVenda': ItemVenda,
        'MovimentacaoEstoque': MovimentacaoEstoque,
        'Financeiro': Financeiro
    }

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
