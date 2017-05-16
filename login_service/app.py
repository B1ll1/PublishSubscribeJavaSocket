import os
from flask import Flask, request, url_for, render_template, redirect
from models.User import User
from flask_login import login_user, logout_user, login_required
from config import login_manager, app, db

# Pega o usuario que está logado
@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

# Rota index para quem está logado
@app.route('/')
@login_required
def hello():
	return render_template('index.html')

# Rota de registro de usuário
@app.route('/users/register', methods = ['GET', 'POST'])
# Se o método for GET o usuário vai para tela de registro e se for POST vai para o método de registro
def register():
	if request.method == 'GET':
		return render_template('register.html')

	# Inicio do método de registro
	# Checa se já existe um usuário com os mesmos valores de username e email
	user = User.query.filter_by(username = request.form['username'], email = request.form['email']).first()
	# Se nenhum usuário for encontrado, um novo usuário é criado com os dados inseridos com no formulário
	if user is None:
		user = User(request.form['username'], request.form['password'], request.form['email'])
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('login'))

	return render_template('register.html', warning = "Try another username or email.")

# Rota de login
@app.route('/login', methods = ['GET', 'POST'])
# Se o metodo for GET o usuário vai para tela de login se for POST ele entra no metódo de login
def login():
	if request.method == 'GET':
		return render_template('login.html')

	# Inicio do método de login
	# O username é unico então se o usuário existe ele vai ser encontrado
	user = User.query.filter_by(username = request.form['username']).first()

	# Caso não exista usuário com esse username
	if user is None:
		return redirect(url_for('login'))
	# Checa se a senha está certa
	if not user.checkPassword(request.form['password']):
		return redirect(url_for('login'))

	# Loga o usuário no sistema	
	login_user(user)
	# Fim do método de login
	
	return redirect(url_for('hello'))

# Rota de logout
@app.route('/logout', methods = ['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))	


if __name__ == '__main__':
	app.run()