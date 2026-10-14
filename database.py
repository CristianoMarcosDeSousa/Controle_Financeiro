import os
import sqlite3

CAMINHO_BANCO = os.path.join(os.path.dirname(os.path.abspath(__file__)), "financeiro.db")
conexao = sqlite3.connect(CAMINHO_BANCO, check_same_thread=False)
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS lancamentos (
id INTEGER PRIMARY KEY AUTOINCREMENT,
descricao TEXT NOT NULL,
valor REAL NOT NULL,
categoria TEXT NOT NULL,
tipo TEXT NOT NULL
)
""")

conexao.commit()

cursor.execute("""
PRAGMA table_info(lancamentos)
""")

colunas = [coluna[1] for coluna in cursor.fetchall()]

if "data" not in colunas:
    cursor.execute("""
    ALTER TABLE lancamentos
    ADD COLUMN data TEXT
    """)

    conexao.commit()

cursor.execute("""
UPDATE lancamentos
SET data = date('now', 'localtime')
WHERE data IS NULL
""")

conexao.commit()