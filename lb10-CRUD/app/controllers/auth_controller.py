# controllers/auth_controller.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.book import UserRepo, User

bp = Blueprint("auth", __name__, url_prefix="/auth")

repo = UserRepo()

@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("books.list_books"))  # Если уже logged in, редирект на protected page

    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        user = repo.get_by_username(username)
        if user and user.check_password(password):
            login_user(user)
            flash("Login successful!", "success")
            return redirect(url_for("books.list_books"))
        else:
            flash("Invalid username or password", "error")
    return render_template("auth/login.html")

@bp.route("/logout")
@login_required
def logout():
    logout_user()
    flash("You have been logged out.", "info")
    return redirect(url_for("auth.login"))

@bp.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if repo.get_by_username(username):
            flash("Username already exists", "error")
        else:
            repo.add(username, password)
            flash("Registration successful! Please login.", "success")
            return redirect(url_for("auth.login"))
    return render_template("auth/register.html")