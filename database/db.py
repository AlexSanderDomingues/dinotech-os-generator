# database/db.py
import sqlite3
import os
import sys
from pathlib import Path
from datetime import datetime
def get_db_path():
    """Resolve o caminho do banco de dados corretamente para o executável"""
    if getattr(sys, 'frozen', False):
        # Se estiver rodando como executável
        base_dir = Path(sys._MEIPASS)
    else:
        # Se estiver rodando no desenvolvimento
        base_dir = Path(__file__).parent
    
    return base_dir / "database" / "usuario.db"

def get_connection():
    """Garante que a pasta database exista e retorna uma conexão"""
    db_path = get_db_path()
    db_path.parent.mkdir(parents=True, exist_ok=True)  # Cria a pasta se não existir
    return sqlite3.connect(str(db_path))

def inicializar_banco():
    """Inicializa todas as tabelas necessárias"""
    with get_connection() as conn:
        cursor = conn.cursor()
        
        # Tabela de usuários
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuario(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT NOT NULL UNIQUE, 
            senha TEXT NOT NULL
        )''')
        
        # Tabela de ordens de serviço
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS ordens_servico (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            data_criacao TEXT NOT NULL,
            nome_cliente TEXT NOT NULL,
            telefone TEXT NOT NULL,
            aparelho_modelo TEXT NOT NULL,
            problema_relatado TEXT NOT NULL,
            diagnostico TEXT,
            solucao TEXT,
            valor REAL,
            status TEXT NOT NULL,
            tecnico_responsavel TEXT,
            garantia TEXT
        )''')
        conn.commit()

def cadastrar_usuario(usuario, senha):
    """Cadastra um novo usuário no sistema"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(
                "INSERT INTO usuario (usuario, senha) VALUES (?, ?)",
                (usuario, senha)
            )
            return True
    except sqlite3.IntegrityError:
        return False

def verificar_login(usuario, senha):
    """Verifica as credenciais de login"""
    with get_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT id FROM usuario WHERE usuario = ? AND senha = ?",
            (usuario, senha)
        )
        return cursor.fetchone() is not None

def cadastrar_os(dados_os):
    """Cadastra uma nova ordem de serviço"""
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            
            cursor.execute('''
            INSERT INTO ordens_servico (
                data_criacao,
                nome_cliente,
                telefone,
                aparelho_modelo,
                problema_relatado,
                diagnostico,
                solucao,
                valor,
                status,
                tecnico_responsavel,
                garantia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            ''', (
                datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                dados_os.get('cliente', ''),
                dados_os.get('telefone', ''),
                dados_os.get('aparelho', ''),
                dados_os.get('problema', ''),
                dados_os.get('diagnostico', ''),
                dados_os.get('solucao', ''),
                dados_os.get('valor', 0.0),
                dados_os.get('status', 'Aberta'),
                dados_os.get('tecnico', ''),
                dados_os.get('garantia', '')
            ))
            return True
    except sqlite3.Error as e:
        print(f"Erro ao cadastrar OS: {e}")
        return False

def listar_os(filtro=None):
    """Lista todas as ordens de serviço com filtro opcional"""
    with get_connection() as conn:
        cursor = conn.cursor()
        if filtro:
            query = '''
            SELECT * FROM ordens_servico 
            WHERE nome_cliente LIKE ? OR telefone LIKE ? OR aparelho_modelo LIKE ?
            ORDER BY data_criacao DESC
            '''
            param = f"%{filtro}%"
            cursor.execute(query, (param, param, param))
        else:
            cursor.execute('SELECT * FROM ordens_servico ORDER BY data_criacao DESC')
        return cursor.fetchall()