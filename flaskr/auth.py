import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():# create an account
    if request.method == 'POST':
        username = request.form['username']#get info from user
        password = request.form['password']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            try:
                db.execute(#create the user in the db
                    "INSERT INTO user (username, password) VALUES (?, ?)",
                    (username, generate_password_hash(password)),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} is already registered."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():#login
    if request.method == 'POST':
        username = request.form['username']#get user info
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(#see is user exists
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:#if no user give error
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):#if wrong password give wrong password error
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']#log the user in
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():#maneges session ids
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM user WHERE id = ?', (user_id,)
        ).fetchone()
        
@bp.route('/logout')
def logout():
    session.clear()#clears the user from the session
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))## if they arent logged in, bring them to the login page

        return view(**kwargs)

    return wrapped_view