import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash
import ibm_db
from expense_tracker.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        name = request.form['name']
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not name:
            error = 'Name is required.'
        if not username:
            error = 'Username is required.'
        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'

        if error is None:
            insert = "INSERT INTO user (name, username, email,  password) VALUES (?, ?, ?, ?)"
            stmt = ibm_db.prepare(db, insert)
            ibm_db.bind_param(stmt, 1, name)
            ibm_db.bind_param(stmt, 2, username)
            ibm_db.bind_param(stmt, 3, email)
            ibm_db.bind_param(stmt, 4, generate_password_hash(password))
            try:
                ibm_db.execute(stmt)
            except:
                error = "Account with username or email already exist"
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        sql = "SELECT * FROM user WHERE username=?"
        stmt = ibm_db.prepare(db, sql)
        ibm_db.bind_param(stmt, 1, username)
        ibm_db.execute(stmt)
        user = ibm_db.fetch_assoc(stmt)

        if not user:
            error = 'Incorrect username.'
        elif not check_password_hash(user['PASSWORD'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['ID']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))
