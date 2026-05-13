"""
routes/dashboard.py - Dashboard / home
"""
from flask import Blueprint, render_template, session
from routes.auth import login_required
import db as database

dashboard_bp = Blueprint('dashboard', __name__)


@dashboard_bp.route('/dashboard')
@login_required
def index():
    stats = {}
    try:
        with database.get_cursor() as cur:
            cur.execute('SELECT COUNT(*) AS cnt FROM employees')
            stats['total_employees'] = cur.fetchone()['cnt']

            cur.execute("SELECT COUNT(*) AS cnt FROM employees WHERE status = 'active'")
            stats['active_employees'] = cur.fetchone()['cnt']

            cur.execute('SELECT COUNT(*) AS cnt FROM products')
            stats['total_products'] = cur.fetchone()['cnt']

            cur.execute('SELECT SUM(stock) AS total FROM products')
            row = cur.fetchone()
            stats['total_stock'] = row['total'] or 0

            cur.execute('''
                SELECT department, COUNT(*) AS cnt
                FROM employees
                GROUP BY department
                ORDER BY cnt DESC
            ''')
            stats['by_dept'] = cur.fetchall()

            cur.execute('''
                SELECT al.*, u.username
                FROM audit_log al
                LEFT JOIN users u ON al.user_id = u.id
                ORDER BY al.created_at DESC LIMIT 10
            ''')
            stats['recent_activity'] = cur.fetchall()
    except Exception as e:
        stats['error'] = str(e)

    return render_template('dashboard.html', stats=stats)
