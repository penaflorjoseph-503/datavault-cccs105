"""
routes/products.py - Full CRUD for products table
"""
from flask import Blueprint, render_template, request, redirect, url_for, flash, session, jsonify
from routes.auth import login_required
import db as database

products_bp = Blueprint('products', __name__, url_prefix='/products')

CATEGORIES = ['Electronics', 'Furniture', 'Accessories', 'Stationery', 'Software', 'Other']


def _log(cur, action, record_id, description):
    cur.execute(
        'INSERT INTO audit_log (user_id, action, table_name, record_id, description) VALUES (%s, %s, %s, %s, %s)',
        (session.get('user_id'), action, 'products', record_id, description)
    )


def _validate(form):
    errors = []
    if not form.get('name', '').strip():
        errors.append('Product name is required.')
    if not form.get('sku', '').strip():
        errors.append('SKU is required.')
    try:
        price = float(form.get('price', ''))
        if price < 0:
            raise ValueError
    except ValueError:
        errors.append('Price must be a positive number.')
    try:
        stock = int(form.get('stock', ''))
        if stock < 0:
            raise ValueError
    except ValueError:
        errors.append('Stock must be a non-negative integer.')
    return errors


@products_bp.route('/')
@login_required
def index():
    q        = request.args.get('q', '').strip()
    category = request.args.get('category', '')
    page     = max(1, int(request.args.get('page', 1)))
    per      = 10
    offset   = (page - 1) * per

    conditions, params = [], []

    if q:
        conditions.append('(name LIKE %s OR sku LIKE %s OR description LIKE %s)')
        like = f'%{q}%'
        params += [like, like, like]
    if category:
        conditions.append('category = %s')
        params.append(category)

    where = ('WHERE ' + ' AND '.join(conditions)) if conditions else ''

    try:
        with database.get_cursor() as cur:
            cur.execute(f'SELECT COUNT(*) AS cnt FROM products {where}', params)
            total = cur.fetchone()['cnt']

            cur.execute(
                f'SELECT * FROM products {where} ORDER BY id DESC LIMIT %s OFFSET %s',
                params + [per, offset]
            )
            rows = cur.fetchall()
    except Exception as e:
        flash(f'Database error: {e}', 'danger')
        rows, total = [], 0

    total_pages = (total + per - 1) // per
    return render_template(
        'products/index.html',
        rows=rows, q=q, category=category,
        categories=CATEGORIES,
        page=page, total_pages=total_pages, total=total
    )


@products_bp.route('/create', methods=['GET', 'POST'])
@login_required
def create():
    errors, form = [], {}

    if request.method == 'POST':
        form   = request.form.to_dict()
        errors = _validate(form)

        if not errors:
            try:
                with database.get_cursor() as cur:
                    cur.execute('''
                        INSERT INTO products (name, sku, category, price, stock, description)
                        VALUES (%s, %s, %s, %s, %s, %s)
                    ''', (
                        form['name'].strip(), form['sku'].strip().upper(),
                        form['category'], float(form['price']),
                        int(form['stock']), form.get('description', '').strip()
                    ))
                    _log(cur, 'INSERT', cur.lastrowid, f"Added product {form['name']}")
                flash('Product added successfully!', 'success')
                return redirect(url_for('products.index'))
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    errors.append('A product with this SKU already exists.')
                else:
                    errors.append(f'Database error: {e}')

    return render_template(
        'products/form.html',
        title='Add Product', action=url_for('products.create'),
        form=form, errors=errors, categories=CATEGORIES
    )


@products_bp.route('/<int:pid>/edit', methods=['GET', 'POST'])
@login_required
def edit(pid):
    errors = []

    try:
        with database.get_cursor() as cur:
            cur.execute('SELECT * FROM products WHERE id = %s', (pid,))
            product = cur.fetchone()
    except Exception as e:
        flash(f'Error: {e}', 'danger')
        return redirect(url_for('products.index'))

    if not product:
        flash('Product not found.', 'warning')
        return redirect(url_for('products.index'))

    form = dict(product)

    if request.method == 'POST':
        form   = request.form.to_dict()
        errors = _validate(form)

        if not errors:
            try:
                with database.get_cursor() as cur:
                    cur.execute('''
                        UPDATE products
                        SET name=%s, sku=%s, category=%s, price=%s, stock=%s, description=%s
                        WHERE id=%s
                    ''', (
                        form['name'].strip(), form['sku'].strip().upper(),
                        form['category'], float(form['price']),
                        int(form['stock']), form.get('description', '').strip(), pid
                    ))
                    _log(cur, 'UPDATE', pid, f"Updated product ID {pid}")
                flash('Product updated successfully!', 'success')
                return redirect(url_for('products.index'))
            except Exception as e:
                if 'Duplicate entry' in str(e):
                    errors.append('SKU already used by another product.')
                else:
                    errors.append(f'Database error: {e}')

    return render_template(
        'products/form.html',
        title='Edit Product',
        action=url_for('products.edit', pid=pid),
        form=form, errors=errors, categories=CATEGORIES, product=product
    )


@products_bp.route('/<int:pid>/delete', methods=['POST'])
@login_required
def delete(pid):
    try:
        with database.get_cursor() as cur:
            cur.execute('SELECT name FROM products WHERE id = %s', (pid,))
            prod = cur.fetchone()
            if prod:
                cur.execute('DELETE FROM products WHERE id = %s', (pid,))
                _log(cur, 'DELETE', pid, f"Deleted product {prod['name']}")
                flash('Product deleted.', 'success')
            else:
                flash('Product not found.', 'warning')
    except Exception as e:
        flash(f'Error: {e}', 'danger')

    return redirect(url_for('products.index'))


@products_bp.route('/<int:pid>/json')
@login_required
def get_json(pid):
    try:
        with database.get_cursor() as cur:
            cur.execute('SELECT * FROM products WHERE id = %s', (pid,))
            row = cur.fetchone()
        if row:
            for key in ('created_at', 'updated_at'):
                if row.get(key):
                    row[key] = str(row[key])
            return jsonify(row)
        return jsonify({'error': 'Not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500
