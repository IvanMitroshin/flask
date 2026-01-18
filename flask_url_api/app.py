from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
app.config['SECRET_KEY'] = 'key'
db = SQLAlchemy(app)
migrate = Migrate(app, db)


class Notes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    text = db.Column(db.Text, nullable=False)
    subtitle = db.Column(db.String(100))


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route('/home')
def home():
    return render_template('home.html')


@app.route('/')
def main():
    if 'user_id' not in session:
        return redirect(url_for('home'))
    return render_template('index.html', username=session.get('username'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')

        if Users.query.filter_by(username=username).first() or Users.query.filter_by(email=email).first():
            return 'Пользователь уже существует! <a href="/register">Назад</a>'

        new_user = Users(username=username, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        user = Users.query.filter_by(username=username).first()

        if user and user.password == password:
            session['user_id'] = user.id
            session['username'] = user.username
            return redirect(url_for('main'))
        else:
            return 'Неверный логин или пароль! <a href="/login">Попробуйте снова</a>'

    return render_template('login.html')


@app.route('/notes', methods=['GET', 'POST'])
def notes():
    if 'user_id' not in session:
        return redirect(url_for('home'))

    if request.method == 'POST':
        title = request.form.get('title')
        subtitle = request.form.get('subtitle', '')
        text = request.form.get('text')

        new_note = Notes(title=title, subtitle=subtitle, text=text)
        db.session.add(new_note)
        db.session.commit()
        return redirect(url_for('notes'))

    all_notes = Notes.query.all()
    return render_template('notes.html', notes=all_notes, username=session.get('username'))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)