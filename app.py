from flask import Flask,render_template,url_for,request,redirect,session
from werkzeug.security import generate_password_hash, check_password_hash


from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///blog.db'
db = SQLAlchemy(app)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key='Grisha2011@'


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    

    def __repr__(self):
        return '<Article %r>' % self.id
    
@app.route('/')
def index():
    home = 'link-secondary'
    if 'user' in session:
        user = session['user']
        return render_template('index.html', home=home, user=user)
    else:
        user = None
    return render_template('index.html', home=home)


@app.route('/login', methods=['GET', 'POST'])
def login():
    log= 'link-secondary'
    if request.method == "POST":
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session['user']={
                'id': user.id,
                'username': user.username,
                'email': user.email,
                'exit': 'ldkdfngskldsnsdffbas',
            }
            return redirect(url_for('index'))
        else:
            return "Invalid credentials"
    else:
        return render_template('login.html',log=log)

@app.route('/register', methods=['GET', 'POST'])
def register():
    reg = 'link-secondary'
    if request.method == "POST":
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        # Проверка на существование пользователя
        existing_user = User.query.filter_by(username=username).first()
        if existing_user:
            return "Пользователь с таким именем уже существует"
        existing_email = User.query.filter_by(email=email).first()
        if existing_email:
            return "Пользователь с таким email уже существует"
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    else:
        return render_template('register.html', reg=reg)
    


@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect(url_for('index'))




@app.route('/Admin')
def admin():
    if 'user' in session:
        user = session['user']
        users = User.query.all()
        error = request.args.get('error')  # Получаем error из URL-параметра
        return render_template('admin.html', user=user, users=users, error=error)
    else:
        return redirect(url_for('login'))

@app.route('/<int:id>/del')
def delete_user(id):
    if 'user' not in session:
        return redirect(url_for('login'))
    else:
        if session['user']['id'] == id:
            er = 'Вы не можете удалить себя'
            return redirect(url_for('admin', error=er))
        else:
            user = User.query.get_or_404(id)
            db.session.delete(user)
            db.session.commit()
            return redirect(url_for('admin'))
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
