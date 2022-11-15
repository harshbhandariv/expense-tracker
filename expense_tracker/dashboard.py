from flask import Blueprint, render_template, g
import ibm_db
import ibm_db_dbi

from expense_tracker.auth import login_required
from expense_tracker.db import get_db

bp = Blueprint('dashboard', __name__, url_prefix='/dashboard')


@bp.route('/')
@login_required
def index():
    return render_template('dashboard/index.html')
