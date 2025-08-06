from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

@app.route('/')
def index():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM usuarios')
    usuarios = cursor.fetchall()
    conn.close()
    return render_template('index.html', usuarios=usuarios)


@app.route('/cadastrar', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        tipo = request.form['tipo']
        status = request.form['status']

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        cursor.execute('INSERT INTO usuarios (nome, email, tipo, status) VALUES (?, ?, ?, ?)',
                       (nome, email, tipo, status))
        conn.commit()
        conn.close()

        return redirect('/')

    return render_template('create.html')

@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        tipo = request.form['tipo']
        status = request.form['status']

        cursor.execute('''
            UPDATE usuarios SET nome = ?, email = ?, tipo = ?, status = ? WHERE id = ?
        ''', (nome, email, tipo, status, id))
        conn.commit()
        conn.close()
        return redirect('/')

    cursor.execute('SELECT * FROM usuarios WHERE id = ?', (id,))
    usuario = cursor.fetchone()
    conn.close()

    return render_template('edit.html', usuario=usuario)

@app.route('/excluir/<int:id>')
def excluir(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM usuarios WHERE id = ?', (id,))
    conn.commit()
    conn.close()
    return redirect('/')


if __name__ == '__main__':
    app.run(debug=True)

