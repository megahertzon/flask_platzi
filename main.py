from crypt import methods
from multiprocessing import context
import unittest
from flask import (
    Flask,
    request,
    make_response,
    redirect,
    render_template,
    session,
    url_for,
    flash,
)
import unittest
from app import create_app
from app.forms import LoginForm, TodoForm
from app.firestore_service import get_users, get_todos, put_todo
from flask_login import current_user, login_required

app = create_app()

todos = ["comprar cafe", "solicitud compra", "entregar producto"]


@app.cli.command()
def test():
    tests = unittest.TestLoader().discover("tests")
    unittest.TextTestRunner().run(tests)


@app.errorhandler(404)
def not_found(error):
    return render_template("404.html", error=error)


@app.route("/")
def index():
    user_ip = request.remote_addr

    response = make_response(redirect("hello"))
    # response.set_cookie("user_ip", user_ip)
    session["user_ip"] = user_ip
    return response


@app.route("/hello", methods=["GET", "POST"])
@login_required
def hello():
    user_ip = session.get("user_ip")
    login_form = LoginForm()
    username = current_user.id

    todo_form = TodoForm()

    context = {
        "user_ip": user_ip,
        "todos": get_todos(user_id=username),
        "username": username,
        "todo_form": todo_form,
    }
    if todo_form.validate_on_submit():
        put_todo(user_id=username, description=todo_form.description.data)
        flash('tu tarea se creo con éxito')
        return redirect(url_for('hello'))

    # users = get_users()
    # for user in users:
    #     print(user.id)
    #     print(user.to_dict()["password"])
    return render_template("hello.html", **context)
