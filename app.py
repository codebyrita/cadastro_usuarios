from flask import Flask, render_template, request, redirect, url_for, get_flashed_messages
import sqlite3
import re

app = Flask(__name__)
app.secret_key = 'sua_chave_secreta'  # troque por algo forte

# ----------------- Helpers -----------------
def get_conn():
    # Se quiser, pode ativar named rows:
    # conn = sqlite3.connect('database.db'); conn.row_factory = sqlite3.Row; return conn
    return sqlite3.connect('database.db')

def senha_valida(senha: str) -> bool:
    """6–8 chars, pelo menos 1 minúscula, 1 maiúscula, 1 número e 1 símbolo."""
    pattern = r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[^\w\s]).{6,8}$'
    return re.match(pattern, senha or '') is not None

# ----------------- Rotas -------------------
@app.route('/')
def index():
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute('SELECT * FROM usuarios')
        usuarios = cur.fetchall()
    return render_template('index.html', usuarios=usuarios)

@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome         = request.form.get('nome', '').strip()
        email        = request.form.get('email', '').strip()
        usuario_nome = request.form.get('usuario', '').strip()
        senha        = request.form.get('senha', '')
        sexo         = request.form.get('sexo', '')
        telefone     = request.form.get('telefone', '').strip()
        endereco     = request.form.get('endereco', '').strip()
        cpf          = request.form.get('cpf', '').strip()
        permissao    = request.form.get('permissao', '')
        status       = request.form.get('status', '')

        # valida senha (6–8, maiúscula, minúscula, número, símbolo)
        if not senha_valida(senha):
            return render_template(
                'create.html',
                mensagem='Senha inválida. Use 6–8 caracteres com ao menos 1 maiúscula, 1 minúscula, 1 número e 1 símbolo.',
                mensagem_tipo='danger',
                redirect_after=False,
                next_url=None
            )

        # impede e-mail duplicado
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("SELECT 1 FROM usuarios WHERE email = ? LIMIT 1", (email,))
            ja_existe = cur.fetchone() is not None

        if ja_existe:
            return render_template(
                'create.html',
                mensagem='Este e-mail já está cadastrado. Use outro.',
                mensagem_tipo='danger',
                redirect_after=False,
                next_url=None
            )

        # persiste
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute("""
                INSERT INTO usuarios
                (nome, email, usuario, senha, sexo, telefone, endereco, cpf, permissao, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (nome, email, usuario_nome, senha, sexo, telefone, endereco, cpf, permissao, status))
            conn.commit()

        # sucesso -> mostra no create e JS redireciona
        return render_template(
            'create.html',
            mensagem='Cadastro realizado com sucesso!',
            mensagem_tipo='success',
            redirect_after=True,
            next_url=url_for('index')
        )

    # GET
    get_flashed_messages(with_categories=True)
    return render_template('create.html', mensagem=None, redirect_after=False, next_url=None)


@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if request.method == 'GET':
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
            usuario = cur.fetchone()
        if not usuario:
            return redirect(url_for('index'))  # ou 404
        return render_template('edit.html', usuario=usuario)

    # POST
    nome         = request.form.get('nome', '').strip()
    email        = request.form.get('email', '').strip()
    usuario_nome = request.form.get('usuario', '').strip()
    senha        = request.form.get('senha', '')
    sexo         = request.form.get('sexo', '')
    telefone     = request.form.get('telefone', '').strip()
    endereco     = request.form.get('endereco', '').strip()
    cpf          = request.form.get('cpf', '').strip()
    permissao    = request.form.get('permissao', '')
    status       = request.form.get('status', '')

    if not senha_valida(senha):
        with get_conn() as conn:
            cur = conn.cursor()
            cur.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
            usuario = cur.fetchone()
        if not usuario:
            return redirect(url_for('index'))
        return render_template(
            'edit.html',
            usuario=usuario,
            mensagem='Senha inválida. Use 6–8 caracteres com ao menos 1 maiúscula, 1 minúscula, 1 número e 1 símbolo.',
            mensagem_tipo='danger'
        )

    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute("""
            UPDATE usuarios
            SET nome=?, email=?, usuario=?, senha=?, sexo=?, telefone=?, endereco=?, cpf=?, permissao=?, status=?
            WHERE id=?
        """, (nome, email, usuario_nome, senha, sexo, telefone, endereco, cpf, permissao, status, id))
        conn.commit()

    return redirect(url_for('index'))

@app.route('/excluir/<int:id>')
def excluir(id):
    with get_conn() as conn:
        cur = conn.cursor()
        cur.execute('DELETE FROM usuarios WHERE id = ?', (id,))
        conn.commit()
    return redirect(url_for('index'))

# -------------------------------------------
if __name__ == '__main__':
    app.run(debug=True)
