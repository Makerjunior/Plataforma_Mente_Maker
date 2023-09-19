import os
from flask import Flask, request, send_from_directory, render_template, jsonify, g, redirect
from werkzeug.security import generate_password_hash, check_password_hash
from lista_arquivos import get_file_list
from galeria_imagens import get_image_gallery
from banco_dados import UserDatabase
from usuarios import User
import time

app = Flask(__name__)


def get_user_db():
    if 'user_db' not in g:
        g.user_db = UserDatabase('database/users.db')
    return g.user_db

user_db = UserDatabase('database/users.db')

@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    user = User.login(username, password)
    
    if user:
        file_list = get_file_list()
        image_gallery = get_image_gallery()
        client_ip = request.remote_addr
        # Diretório onde suas músicas estão localizadas
        MUSIC_DIR = "static/musicas"

# Lista de músicas disponíveis
        playlist = []

# Preencha a lista de reprodução com arquivos .mp3 no diretório
        for root, dirs, files in os.walk(MUSIC_DIR):
          for file in files:
            if file.endswith(".mp3"):
             playlist.append(file)
        return render_template('index.html', file_list=file_list, image_gallery=image_gallery,playlist=playlist, client_ip=client_ip)
    else:
        file_list = get_file_list()
        image_gallery = get_image_gallery()

        return render_template('erro.html')
    
@app.route('/upload_file', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join('./static/uploads', file.filename))
        file_list = get_file_list()
        image_gallery = get_image_gallery()
        return render_template('index.html', file_list=file_list, image_gallery=image_gallery)
    else:
        return jsonify({'message': 'Envie um arquivo usando POST.'})

@app.route('/static/uploads/<filename>')
def download(filename):
    return send_from_directory('./static/uploads', filename)

@app.route('/')
def form():
    return render_template('login.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastrar():
    if request.method == 'POST':
        nome = request.form['nome']
        telefone = request.form['telefone']
        email = request.form['email']
        password = request.form['password']
        if user_db.add_user(nome, telefone, email, password):
            success_message = "Usuário criado com sucesso!"
            return render_template('login.html', success_message=success_message)
        else:
            return render_template('erro.html')
    return render_template('cadastro.html')

@app.route('/recuperar_senha', methods=['GET', 'POST'])
def recuperar_senha():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        user = user_db.get_user_by_data(nome, email, telefone)
        if user is None:
            mensagem_erro = "Os dados fornecidos não correspondem a um usuário."
            return render_template('recuperar_senha.html', mensagem_erro=mensagem_erro)
        chave_redefinicao = 'chave_gerada_aleatoriamente'
        user_db.set_chave_redefinicao(user['id'], chave_redefinicao)

        return render_template('redefinir_senha.html', id_usuario=user['id'], chave_redefinicao=chave_redefinicao)
    return render_template('recuperar_senha.html')

@app.route('/verificar_dados_usuario', methods=['POST'])
def verificar_dados_usuario_post():
    if request.method == 'POST':
        data = request.get_json()
        nome = data['nome']
        email = data['email']
        telefone = data['telefone']
        user = user_db.get_user_by_data(nome, email, telefone)

        if user is not None:
            return jsonify({'valid': True})
        else:
            return jsonify({'valid': False})

@app.route('/redefinir_senha', methods=['POST'])
def redefinir_senha():
    data = request.get_json()
    nova_senha = data['novaSenha']  # Obtém a nova senha do JSON

    # Recupere o nome do usuário (você pode adicionar esse campo ao seu formulário HTML)
    nome = data['nome']

    # Verifique se o nome de usuário e a nova senha foram fornecidos
    if not nome or not nova_senha:
        return jsonify({'success': False, 'message': 'Nome de usuário e nova senha são obrigatórios'})

    # Atualize a senha no banco de dados
    user_db = UserDatabase('database/users.db')
    if user_db.update_user_password(nome, nova_senha):
        return jsonify({'success': True, 'message': 'Senha redefinida com sucesso!'})
    else:
        return jsonify({'success': False, 'message': 'Não foi possível redefinir a senha'})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
