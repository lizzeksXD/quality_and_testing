from flask import Flask, render_template, session, redirect, url_for
from flask_login import LoginManager, current_user
from controllers.books_controller import bp as books_bp
from controllers.auth_controller import bp as auth_bp
from models.book import db, User, UserRepo

app = Flask(__name__, template_folder="views", static_folder="static")
app.secret_key = "replace-this-with-a-secure-random-key"

# Настройка базы данных
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:852411@localhost/flask_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'auth.login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

with app.app_context():
    db.create_all()

    repo = UserRepo()
    if not repo.get_by_username('admin'):
        repo.add('admin', '123')

app.register_blueprint(books_bp)
app.register_blueprint(auth_bp)

@app.get("/")
def index():
    return render_template("index.html")

@app.get("/login")
def login():
    session['user'] = "demo_user"
    return redirect(url_for("auth.login"))

@app.get("/logout")
def logout():
    session.pop('user', None)
    return redirect(url_for("auth.login "))

if __name__ == "__main__":
    app.run(debug=True, port=5001)
