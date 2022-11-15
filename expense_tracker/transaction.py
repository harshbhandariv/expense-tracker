from flask import Blueprint, flash, g, render_template, request, redirect, url_for
import ibm_db
import ibm_db_dbi
import random
from expense_tracker.auth import login_required
from expense_tracker.db import get_db

bp = Blueprint('transaction', __name__, url_prefix='/transaction')


@bp.route('/')
@login_required
def index():
    db = get_db()
    user_id = g.user["ID"]
    query = f"SELECT transaction.amount, transaction.description, transaction.category, transaction.date, transaction.receipt FROM transaction INNER JOIN user ON transaction.user_id=user.id where user.id={user_id} ORDER BY transaction.id DESC"
    conn = ibm_db_dbi.Connection(db)
    curr = conn.cursor()
    curr.execute(query)
    transactions = curr.fetchall()
    return render_template('transaction/index.html', transactions=transactions)


@bp.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        db = get_db()
        user_id = g.user["ID"]
        category = request.form["category"]
        description = request.form["description"]
        amount = request.form["amount"]
        date = request.form["date"]
        receipt = random.randint(0, 100000)
        insert = "INSERT INTO transaction (user_id, category, amount, description, date, receipt) VALUES (?, ?, ?, ?, ?, ?)"
        stmt = ibm_db.prepare(db, insert)
        ibm_db.bind_param(stmt, 1, user_id)
        ibm_db.bind_param(stmt, 2, category)
        ibm_db.bind_param(stmt, 3, amount)
        ibm_db.bind_param(stmt, 4, description)
        ibm_db.bind_param(stmt, 5, date)
        ibm_db.bind_param(stmt, 6, receipt)
        error = None
        try:
            ibm_db.execute(stmt)
        except:
            error = "Error occurred while adding transaction"
        else:
            return redirect(url_for('transaction.index'))
        flash(error)
    return render_template('transaction/add.html')


@bp.route('/limit', methods=["GET", "POST"])
@login_required
def limit():
    if request.method == "POST":
        db = get_db()
        id = g.user["ID"]
        limit = request.form["limit"]
        insert = f"UPDATE USER SET limit=? WHERE ID={id}"
        stmt = ibm_db.prepare(db, insert)
        ibm_db.bind_param(stmt, 1, limit)
        error = None
        try:
            ibm_db.execute(stmt)
        except:
            error = "Error occurred while setting limit"
        else:
            flash("Limit updated successfully")
            return redirect(url_for('dashboard.index'))
        flash(error)
    return render_template('transaction/limit.html')
