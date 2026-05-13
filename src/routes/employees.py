"""
routes/employees.py - Full CRUD for employees table
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from routes.auth import login_required
import db as database

employees_bp = Blueprint('employees', __name__, url_prefix='/employees')

DEPARTMENTS = ['Engineering', 'Marketing', 'HR', 'Finance', 'Operations', 'Sales', 'Legal', 'IT']
POSITIONS   = [
    'Junior Developer', 'Senior Developer', 'DevOps Engineer', 'QA Engineer',
    'Marketing Manager', 'Content Strategist', 'HR Specialist', 'Recruiter',
    'Accountant', 'Finance Director', 'Operations Manager', 'Sales Representative',
]


def _log(cur, action, record_id, description):
    cur.execute(
        'INSERT INTO audit_log (user_id, action, table_name, record_id, description) VALUES (%s, %s, %s, %s, %s)',
        (session.get('user_id'), action, 'employees', record_id, description)
    )


def _validate(form):
    errors = []
    if not form.get('first_name', '').strip():
        errors.append('First name is required.')
    if not form.get('last_name', '').strip():
        errors.append('Last name is required.')
    email = form.get('email', '').strip()
    if not email or '@' not in email:
        errors.append('Valid email is required.')
    try:
        salary = float(form.get('salary', ''))
        if salary < 0:
            raise ValueError
    except ValueError:
        errors.append('Salary must be a positive number.')
    if not form.get('hire_date'):
        errors.append('Hire date is required.')
    return errors


@employees_bp.route('/')
@login_required
def index():
    q    = request.args.get('q', '').strip()
    dept = request.args.get('dept', '')
    page = max(1, int(request.args.get('page', 1)))
    per  = 10
    offset = (page - 1) * per

    conditions = []
    params     = []

    if q:
        conditions.append(
            '(first_name LIKE %s OR last_name LIKE %s OR email LIKE %s OR position LIKE %s)'
        )
        like = f'%{q}%'
        params += [like, like, like, like]
    if dept:
        conditions.append('department = %s')
        params.append(dept)

    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    try:
        with database.get_cursor() as cur:
            cur.execute(f'SELECT COUNT(*) AS cnt FROM employees {where}', params)
            total = cur.fetchone()['cnt']

            cur.execute(
                f'SELECT * FROM employees {where} ORDER BY id DESC LIMIT %s OFFSET %s',
                params + [per, offset]
            )
            rows = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {e}', 'danger')
        rows, total = [], 0

    total_pages = (total + per - 1) // per

    return render_template(
        'employees/index.html',
        rows=rows, q=q, dept=dept,
        departments=DEPARTMENTS,
        page=page, total_pages=total_pages, total=total
    )


@employees_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    errors = []
    form   = {}

    if request.method == 'POST':
        form   = request.form.to_dict()
        errors = _validate(form)

        if not errors:
            try:
                with database.get_cursor() as cur:
                    cur.execute('''
                        INSERT INTO employees
                            (first_name, last_name, email, department, position, salary, hire_date, status)
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
                    ''', (
                        form['first_name'].strip(), form['last_name'].strip(),
                        form['email'].strip(), form['department'], form['position'],
                        float(form['salary']), form['hire_date'],
                        form.get('status', 'active')
                    ))
                    _log(cur, 'INSERT', cur.lastrowid,
                         f"Added employee {form['first_name']} {form['last_name']}")
                flash('Employee added successfully!', 'success')
                return redirect(url_for('employees.index'))
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    errors.append('An employee with this email already exists.')
                else:
                    errors.append(f'Database error: {e}')

    return render_template(
        'employees/form.html',
        title='Add Employee', action=url_for('employees.create'),
        form=form, errors=errors,
        departments=DEPARTMENTS, positions=POSITIONS
    )


@employees_bp.route('/<int:emp_id>/edit', methods=['GET', 'POST'])
@login_required
def edit(emp_id):
    errors = []

    try:
        with database.get_cursor() as cur:
            cur.execute('SELECT * FROM employees WHERE id = %s', (emp_id,))
            employee = cur.fetchone()
    except Exception as e:
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('employees.index'))

    if not employee:
        flash('Employee not found.', 'warning')
        return redirect(url_for('employees.index'))

    form = dict(employee)

    if request.method == 'POST':
        form   = request.form.to_dict()
        errors = _validate(form)

        if not errors:
            try:
                with database.get_cursor() as cur:
                    cur.execute('''
                        UPDATE employees
                        SET first_name=%s, last_name=%s, email=%s, department=%s,
                            position=%s, salary=%s, hire_date=%s, status=%s
                        WHERE id=%s
                    ''', (
                        form['first_name'].strip(), form['last_name'].strip(),
                        form['email'].strip(), form['department'], form['position'],
                        float(form['salary']), form['hire_date'],
                        form.get('status', 'active'), emp_id
                    ))
                    _log(cur, 'UPDATE', emp_id,
                         f"Updated employee ID {emp_id}")
                flash('Employee updated successfully!', 'success')
                return redirect(url_for('employees.index'))
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    errors.append('Email already used by another employee.')
                else:
                    errors.append(f'Database error: {e}')

    return render_template(
        'employees/form.html',
        title='Edit Employee',
        action=url_for('employees.edit', emp_id=emp_id),
        form=form, errors=errors,
        departments=DEPARTMENTS, positions=POSITIONS,
        employee=employee
    )


@employees_bp.route('/<int:emp_id>/delete', methods=['POST'])
@login_required
def delete(emp_id):
    try:
        with database.get_cursor() as cur:
            cur.execute('SELECT first_name, last_name FROM employees WHERE id = %s', (emp_id,))
            emp = cur.fetchone()
            if emp:
                cur.execute('DELETE FROM employees WHERE id = %s', (emp_id,))
                _log(cur, 'DELETE', emp_id,
                     f"Deleted employee {emp['first_name']} {emp['last_name']}")
                flash('Employee deleted.', 'success')
            else:
                flash('Employee not found.', 'warning')
    except Exception as e:
        flash(f'Error: {e}', 'danger')

    return redirect(url_for('employees.index'))


@employees_bp.route('/<int:emp_id>/json')
@login_required
def get_json(emp_id):
    """Return employee as JSON (used by modal view)."""
    try:
        with database.get_cursor() as cur:
            cur.execute('SELECT * FROM employees WHERE id = %s', (emp_id,))
            row = cur.fetchone()
        if row:
            # Convert date to string
            if row.get('hire_date'):
                row['hire_date'] = str(row['hire_date'])
            if row.get('created_at'):
                row['created_at'] = str(row['created_at'])
            if row.get('updated_at'):
                row['updated_at'] = str(row['updated_at'])
            return jsonify(row)
        return jsonify({'error': 'Not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
