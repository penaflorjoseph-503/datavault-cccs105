"""
routes/auth.py - Authentication routes
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
import bcrypt
import db as database

auth_bp = Blueprint('auth', __name__)


def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated


@auth_bp.route('/')
def index():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))
    return redirect(url_for('auth.login'))


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if 'user_id' in session:
        return redirect(url_for('dashboard.index'))

    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        if not username or not password:
            error = 'Username and password are required.'
        else:
            try:
                with database.get_cursor() as cur:
                    cur.execute('SELECT * FROM users WHERE username = %s', (username,))
                    user = cur.fetchone()

                if user and bcrypt.checkpw(password.encode(), user['password'].encode()):
                    session.clear()
                    session['user_id']   = user['id']
                    session['username']  = user['username']
                    session['role']      = user['role']
                    return redirect(url_for('dashboard.index'))
                else:
                    error = 'Invalid username or password.'
            except Exception as e:
                error = f'Database error: {e}'

    return render_template('auth/login.html', error=error)


@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))


@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    error = None
    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm  = request.form.get('confirm_password', '')

        if not username or not password:
            error = 'All fields are required.'
        elif password != confirm:
            error = 'Passwords do not match.'
        elif len(password) < 6:
            error = 'Password must be at least 6 characters.'
        else:
            hashed = bcrypt.hashpw(password.encode(), bcrypt.gensalt()).decode()
            try:
                with database.get_cursor() as cur:
                    cur.execute(
                        'INSERT INTO users (username, password, role) VALUES (%s, %s, %s)',
                        (username, hashed, 'user')
                    )
                flash('Account created! Please log in.', 'success')
                return redirect(url_for('auth.login'))
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    error = 'Username already exists.'
                else:
                    error = f'Error: {e}'

    return render_template('auth/register.html', error=error)
