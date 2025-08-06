import sqlite3

# Cria ou conecta ao banco
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Cria a tabela de usuários
cursor.execute('''
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        email TEXT NOT NULL,
        tipo TEXT NOT NULL,
        status TEXT NOT NULL
    )
''')

conn.commit()
conn.close()

print("Banco de dados criado com sucesso!")
