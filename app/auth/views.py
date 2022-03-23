from crypt import methods
import imp
from multiprocessing import context

from app.models import UserData
from . import auth
from flask import flash, redirect, render_template, session, url_for
from app.forms import LoginForm


from app.firestore_service import get_user, user_put
from app.models import UserModel,UserData
from flask_login import login_required, login_user, logout_user
from werkzeug.security import generate_password_hash


@auth.route("/login", methods=["GET", "POST"])
def login():
    login_form = LoginForm()
    context = {"login_form": login_form}
    if login_form.validate_on_submit():
        username = login_form.username.data
        password = login_form.password.data
        user_doc = get_user(username)
        if user_doc.to_dict() is not None:
            password_from_db = user_doc.to_dict()["password"]
            if password == password_from_db:
                user_data = UserData(username,password)
                user=UserModel(user_data)
                login_user(user)
                flash('Bienvenido de nuevo') 
                redirect(url_for('hello'))
            else:
                flash('la información no coincide') 
        else :
            flash('el usuario no existe!!!') 
            return redirect(url_for("index"))
        return redirect(url_for("index"))
    return render_template("login.html", **context)

@auth.route("logout")
@login_required
def logout():
    logout_user()
    flash('Regresa pronto')
    return redirect(url_for('auth.login'))


@auth.route('signup', methods=['GET','POST'])
def signup():
    signup_form=LoginForm()
    context={
        'signup_form':signup_form
    }
    if signup_form.validate_on_submit():
        username=signup_form.username.data
        password=signup_form.password.data
        user_doc=get_user(username)

        if user_doc.to_dict() is None:
            password_hash=generate_password_hash(password)
            user_data=UserData(username,password_hash)
            user_put(user_data)

            user=UserModel(user_data)
            login_user(user)
            flash('Bienvenido')

            return redirect(url_for('hello'))
        else:
            flash('el usuario ya existe')

    return render_template('signup.html',**context)

