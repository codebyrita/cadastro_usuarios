import sqlite3

conn = sqlite3.connect('database.db')
cursor = conn.cursor()

cursor.execute('DROP TABLE IF EXISTS usuarios')

cursor.execute('''
CREATE TABLE usuarios (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    email TEXT NOT NULL,
    usuario TEXT NOT NULL,
    senha TEXT NOT NULL,
    sexo TEXT,
    telefone TEXT,
    endereco TEXT,
    cpf TEXT NOT NULL,
    permissao TEXT NOT NULL,
    status TEXT NOT NULL
)
''')

conn.commit()
conn.close()

print("Banco de dados criado com sucesso.")
