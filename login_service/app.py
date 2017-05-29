import os
from flask import g, Flask, request, url_for, render_template, redirect, session
from models.User import User
from models.Publishing import Publishing
from models.Subscription import Subscription
from flask_login import login_user, logout_user, login_required, current_user
from config import login_manager, app, db

def render_sub():
	results_topics = db.engine.execute('SELECT DISTINCT publishings.topic FROM publishings ORDER BY topic ASC')
	results_subscriptions = Subscription.query.filter_by(user_id = current_user.id)
	return results_topics, results_subscriptions

def render_user_topics():
	subscriptions = Subscription.query.filter_by(user_id = current_user.id).all()
	return subscriptions

@login_manager.user_loader
def load_user(id):
	return User.query.get(int(id))

@app.route('/')
def root():
	return redirect(url_for('login'))

@app.route('/analistas')
@login_required
def pubs():
	if current_user.type == 1:
		return render_template('index_pub.html')
	else:
		return redirect(url_for('logout'))

@app.route('/publicacoes')
@login_required
def publishings():
	if current_user.type == 2:
		subscriptions = render_user_topics()
		print subscriptions
		return render_template('publicacoes.html', subs = subscriptions)
	else:
		return redirect(url_for('logout'))

@app.route('/inscritos',  methods = ['POST', 'GET'])
@login_required
def subs():
	if request.method == 'GET' and current_user.type == 2:
		topics, subscriptions = render_sub()
		print topics, subscriptions
		return render_template('index_sub.html', result_topics = topics, result_subs = subscriptions)

	elif request.method == 'GET' and current_user.type != 2:
		return redirect(url_for('logout'))

	elif request.method == 'POST' and current_user.type == 2:
		subscription = Subscription.query.filter_by(topic = request.form['topic'], user_id = current_user.id).first()
		if subscription is None:
			subscription = Subscription(request.form['topic'], current_user.id)
			db.session.add(subscription)
			db.session.commit()
			return redirect(url_for('subs'))
		else:
			topics, subscriptions = render_sub()
			print topics, subscriptions
			return render_template('index_sub.html', warning = 'aviso', result_topics = topics, result_subs = subscriptions)

	else:
		return redirect(url_for('logout'))

@app.route('/publicar', methods = ['POST'])
@login_required
def publish():
	if current_user.type == 1:
		publishing = Publishing(request.form['topic'], request.form['text'])
		db.session.add(publishing)
		db.session.commit()
		return redirect(url_for('pubs'))
	else:
		return redirect(url_for('logout'))

@app.route('/removerinscricao', methods = ['POST'])
@login_required
def unsubscribe():
	if current_user.type == 2:
		subscription = Subscription.query.filter_by(topic = request.form['topic'], user_id = current_user.id).first()
		db.session.remove(subscription)
		db.session.commit()
		return redirect(url_for('subscribe'))
	else:
		return redirect(url_for('logout'))


@app.route('/users/register', methods = ['GET', 'POST'])
def register():
	if request.method == 'GET':
		return render_template('register.html')
	user = User.query.filter_by(username = request.form['username'], email = request.form['email']).first()
	if user is None:
		user = User(request.form['username'], request.form['password'], request.form['email'], request.form['type'])
		db.session.add(user)
		db.session.commit()
		return redirect(url_for('register'))

	return render_template('register.html', warning = "Try another username or email.")

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
	if current_user.type == 0:
		return redirect(url_for('register'))
	if current_user.type == 1:
		return redirect(url_for('pubs'))
	elif current_user.type == 2:
		return redirect(url_for('subs'))

@app.route('/logout', methods = ['GET'])
@login_required
def logout():
	logout_user()
	return redirect(url_for('login'))


if __name__ == '__main__':
	app.run(host='0.0.0.0',port=5000)