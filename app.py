#Тут был мой первый коммит
from flask import request, Flask, render_template, flash
#pip install flask-sqlalchemy flask-migrate flask-login
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager, login_user, login_required, current_user, logout_user, UserMixin

import os

from unicodedata import category

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sgdfgzdfg'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'


#Создание БД
db = SQLAlchemy(app) #создание объекта бд
print(db.__dict__)
migrate = Migrate(app, db) #миграция таблиц/настроек/прочего в БД из приложения


class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), unique = True)
    email = db.Column(db.String(64), unique = True)
    password = db.Column(db.String(256))

#логин
login_manager = LoginManager(app)
class UserLogin():
    def is_active(self):
        return True
    def is_authorized(self):
        return True
    def is_anonymous(self):
        False
    def is_authenticated(self):
        True
    def get_id(self):
        pass

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))








@app.route('/')
def index():
    return render_template('index.html')


'''count = 0'''
'''users = { 1 : {'username' : 'Абабо',
              'email' : 'demo@mcko.ru',
              'password' : '123qwe',
              }
         }'''

###################################################################
@app.route('/logreg', methods = ['POST', 'GET'])
def logreg():
    return render_template('logreg.html')

#from flask_login import login_required, login_user#############################
@app.route('/login', methods = ['POST', 'GET'])
def login():
    if request.method == "POST":
        password = request.form.get('password')
        email = request.form.get('username')
        print(password, email)
        IN_USERS = User.query.filter_by(email=email).first()  #############
        if IN_USERS and password == IN_USERS.password:
            load_user(IN_USERS.id)
            print('ошибок нет')



        '''IN_USERS = False
        user_id = None
        for id in users:
            if users[id]['username'] == login or users[id]['email'] == login:
                IN_USERS = True
                user_id = id
                break
        if not IN_USERS:
            flash('Ошибка! Такой такого пользователя не существует', category = 'error')
        else:
            if users[user_id]['password'] == password:
                print('Успешный вход')
                #login_user(users[user_id]['username'])######################
            else:
                print('Пароль неправильный!')'''

    return render_template('logreg.html')

@app.route('/register', methods = ['POST', 'GET'])
def register():
    if request.method == "POST":
        password = request.form.get('reg-password')
        username = request.form.get('reg-username')
        email = request.form.get('email')

        print(password, username, email)
        #IN_USERS = False
        IN_USERS1 = User.query.filter_by(username=username).first()#############
        IN_USERS2 = User.query.filter_by(email=email).first()############
        print(IN_USERS1, IN_USERS2)

        #регистрация
        if not(IN_USERS1 or IN_USERS2):
            #Создать запись о пользователе
            new_user = User(username=username, email=email, password=password)
            db.session.add(new_user)
            db.session.commit()
            flash(f'Успешная регистраця, {username}', category='success')
        else:
            flash(f'Ошибка! Такой {username} или {email} уже есть', category = 'error')
        return render_template('logreg.html')
        #for id in users:
            #if users[id]['username'] == username or users[id]['email'] == email:
                #IN_USERS = True

        '''if IN_USERS:
            print('Ошибка! Такой пользователь уже есть!')
        else:
            #print('Успешная регистрация')
            users[len(users)+1] = {'username' : username,
                                    'email' : email,
                                    'password' : password,
                                    }


            flash('Успешная регистрация', category = 'success')'''
#####################################################################


@app.route('/wheel1')
def wheel1():
    return render_template('wheel1.html')

@app.route('/wheel2')
def wheel2():
    return render_template('wheel2.html')



if __name__ == "__main__":
    app.run(debug = True)