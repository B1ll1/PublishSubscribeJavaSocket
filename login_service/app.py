import os
from flask import Flask, request, url_for, render_template, redirect
from models.User import User
from flask_login import login_user, logout_user, login_required
from config import login_manager, app, db

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
@login_required
def hello():
	return render_template('index.html')

@app.route('/users/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')

	user = User(request.form['username'], request.form['password'], request.form['email'])
	db.session.add(user)
	db.session.commit()

	return redirect(url_for('login'))


@app.route('/login', methods = ['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	user = User.query.filter_by(username = request.form['username']).first()

	if user is None:
		return redirect(url_for('login'))
	if not user.checkPassword(request.form['password']):
		return redirect(url_for('login'))

	login_user(user)
	return redirect(url_for('hello'))

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))	


if __name__ == '__main__':
	app.run()