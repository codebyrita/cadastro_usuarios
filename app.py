import os, sqlite3
from flask import Flask, render_template, request, redirect, url_for

DB_PATH = os.getenv("DB_PATH", "database.db")
os.makedirs(os.path.dirname(DB_PATH) or ".", exist_ok=True)

def get_conn():
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT NOT NULL,
                email TEXT NOT NULL,
                usuario TEXT NOT NULL,
                senha TEXT NOT NULL,
                sexo TEXT,
                telefone TEXT,
                endereco TEXT,
                cpf TEXT,
                permissao TEXT NOT NULL,
                status TEXT NOT NULL
            );
        """)
        cur.execute("CREATE UNIQUE INDEX IF NOT EXISTS idx_usuarios_email ON usuarios(email);")
        conn.commit()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY", "devsecret")

# Inicializa DB ao subir
init_db()

# ───────────── Helpers CRUD ─────────────
def listar_usuarios():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, email, usuario, senha, sexo, telefone,
                   endereco, cpf, permissao, status
            FROM usuarios
            ORDER BY id ASC
        """)
        return cur.fetchall()

def obter_usuario(uid: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, nome, email, usuario, senha, sexo, telefone,
                   endereco, cpf, permissao, status
            FROM usuarios
            WHERE id=?
        """, (uid,))
        return cur.fetchone()

def inserir_usuario(data: dict):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO usuarios
            (nome, email, usuario, senha, sexo, telefone, endereco, cpf, permissao, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data['nome'], data['email'], data['usuario'], data['senha'],
            data.get('sexo', ''), data.get('telefone', ''),
            data.get('endereco', ''), data.get('cpf', ''),
            data['permissao'], data['status']
        ))
        conn.commit()

def atualizar_usuario(uid: int, data: dict):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE usuarios
               SET nome=?, email=?, usuario=?, senha=?, sexo=?, telefone=?,
                   endereco=?, cpf=?, permissao=?, status=?
             WHERE id=?
        """, (
            data['nome'], data['email'], data['usuario'], data['senha'],
            data.get('sexo', ''), data.get('telefone', ''),
            data.get('endereco', ''), data.get('cpf', ''),
            data['permissao'], data['status'], uid
        ))
        conn.commit()

def excluir_usuario(uid: int):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("DELETE FROM usuarios WHERE id=?", (uid,))
        conn.commit()

# ───────────── Rotas ─────────────
@app.route("/")
def index():
    usuarios = listar_usuarios()
    # certifique-se de que seu template da lista chama-se "index.html"
    return render_template("index.html", usuarios=usuarios)

@app.route("/cadastrar", methods=["GET", "POST"])
def cadastrar():
    if request.method == "POST":
        inserir_usuario(request.form)
        return redirect(url_for("index"))
    # certifique-se de que o template é "create.html"
    return render_template("create.html")

@app.route("/editar/<int:id>", methods=["GET", "POST"])
def editar(id):
    if request.method == "POST":
        atualizar_usuario(id, request.form)
        return redirect(url_for("index"))
    usuario = obter_usuario(id)
    if not usuario:
        return redirect(url_for("index"))
    # certifique-se de que o template é "edit.html"
    return render_template("edit.html", usuario=usuario)

@app.route("/excluir/<int:id>", methods=["GET", "POST"])
def excluir(id):
    excluir_usuario(id)
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
