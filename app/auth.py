from flask import Blueprint , render_template , redirect , url_for , request , flash 
from werkzeug.security import generate_password_hash , check_password_hash
from .app import db
from flask_login import login_required , current_user , login_user ,logout_user
from .models import User,Role
import re

auth = Blueprint('auth',__name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/sign_in',methods=['POST','GET'])
def sign_in():
    if request.method == 'POST':
        login = request.form['log_login']
        password = request.form['log_password']

        user = User.query.filter_by(login = login).first()
        if not user or not check_password_hash(user.password, password):
            error = 'Невозможно аутентифицироваться с указанными логином и паролем'
            return render_template('login.html', error = error)
        
        login_user(user)
        return redirect(url_for('main.index'))

    return render_template('login.html')

@auth.route('/reg',methods=['POST','GET'])
def reg():
    if request.method == 'POST':
        login = request.form['reg_login']
        password = request.form['reg_password']
        password2 = request.form['reg_password2']
        user_fio = request.form['reg_user_fio']

        user =  User.query.filter_by(login = login).first()
        if user:
            error = 'Логин уже занят!'
            return render_template('login.html',error=error)
        if password != password2:
            error = 'Пароли не совпадают!'
            return render_template('login.html',error=error)

        if re.match(r'\S{3,30}',password) and re.match(r'\S{3,30}',login) and re.match(r'\S{3,30}',user_fio):
            new_user = User(login=login , fullname = user_fio , password=generate_password_hash(password,method='sha256'),role_id = 3)

            db.session.add(new_user)
            db.session.commit()
        
            return redirect(url_for('auth.login'))
        else:
            error = 'Некорректные данные'
            return render_template('login.html',error=error)
    return render_template('login.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))