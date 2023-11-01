from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# Configuração do banco de dados
DATABASE = 'agenda.db'

def conectar_bd():
    return sqlite3.connect(DATABASE)

# Criação da tabela (execute apenas uma vez)
"""with conectar_bd() as con:
    con.execute('''CREATE TABLE IF NOT EXISTS pessoa (id INTEGER PRIMARY KEY AUTOINCREMENT, nome TEXT,
email TEXT)''')
"""
# Rotas
@app.route('/')
def listar_registros():
    with conectar_bd() as con:
        registros = con.execute('SELECT * FROM pessoa').fetchall()
    return render_template('listagem.html', registros=registros)

@app.route('/adicionar')
def inserir_registro():
    return render_template('inserir.html')

@app.route('/adicionar2', methods=['POST'])
def adicionar_registro():
    nome = request.form['nome']
    email = request.form['email']
    with conectar_bd() as con:
        con.execute('INSERT INTO pessoa (nome, email) VALUES (?,?)', (nome, email))
    return redirect(url_for('listar_registros'))

@app.route('/editar/<int:id>')
def editar_registro(id):
    with conectar_bd() as con:
        registro = con.execute('SELECT * FROM pessoa WHERE id = ?', (id,)).fetchone()
    return render_template('editar.html', registro=registro)

@app.route('/atualizar/<int:id>', methods=['POST'])
def atualizar_registro(id):
    nome = request.form['nome']
    email = request.form['email']
    with conectar_bd() as con:
        con.execute('UPDATE pessoa SET nome=?, email=? WHERE id=?', (nome, email, id))
    return redirect(url_for('listar_registros'))

@app.route('/excluir/<int:id>')
def excluir_registro(id):
    with conectar_bd() as con:
        con.execute('DELETE FROM pessoa WHERE id = ?', (id,))
    return redirect(url_for('listar_registros'))


if __name__ == '__main__':
    app.run(debug=True)