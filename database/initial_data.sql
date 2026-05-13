-- ============================================================
-- initial_data.sql
-- DBMS Project - Seed / Sample Data
-- ============================================================

USE CCCS105;

-- Default admin user  (password: admin123)
INSERT INTO users (username, password, role) VALUES
('admin', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQyCgE8Wn4OxKcJC3pZx1FOOG', 'admin'),
('jdoe',  '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQyCgE8Wn4OxKcJC3pZx1FOOG', 'user');

-- Sample employees
INSERT INTO employees (first_name, last_name, email, department, position, salary, hire_date, status) VALUES
('Alice',   'Santos',    'alice.santos@company.com',   'Engineering',  'Senior Developer',    95000.00, '2020-03-15', 'active'),
('Bob',     'Reyes',     'bob.reyes@company.com',      'Engineering',  'Junior Developer',    58000.00, '2022-07-01', 'active'),
('Carol',   'Dela Cruz', 'carol.dc@company.com',       'Marketing',    'Marketing Manager',   72000.00, '2019-11-20', 'active'),
('Dan',     'Lim',       'dan.lim@company.com',        'HR',           'HR Specialist',       55000.00, '2021-04-10', 'active'),
('Eva',     'Garcia',    'eva.garcia@company.com',     'Finance',      'Accountant',          67000.00, '2020-09-05', 'active'),
('Frank',   'Torres',    'frank.torres@company.com',   'Engineering',  'DevOps Engineer',     88000.00, '2021-01-12', 'active'),
('Grace',   'Chua',      'grace.chua@company.com',     'Marketing',    'Content Strategist',  60000.00, '2022-02-28', 'active'),
('Hector',  'Ramos',     'hector.ramos@company.com',   'Finance',      'Finance Director',   110000.00, '2018-06-01', 'active'),
('Iris',    'Flores',    'iris.flores@company.com',    'HR',           'Recruiter',           52000.00, '2023-01-15', 'inactive'),
('James',   'Navarro',   'james.navarro@company.com',  'Engineering',  'QA Engineer',         64000.00, '2021-08-22', 'active');

-- Sample products
INSERT INTO products (name, sku, category, price, stock, description) VALUES
('Wireless Mouse',         'PRD-001', 'Electronics',  29.99,  150, 'Ergonomic wireless mouse with long battery life'),
('Mechanical Keyboard',    'PRD-002', 'Electronics', 120.00,   75, 'Tactile mechanical switches, RGB backlit'),
('USB-C Hub',              'PRD-003', 'Electronics',  45.50,  200, '7-in-1 USB-C hub with HDMI and SD card reader'),
('Monitor Stand',          'PRD-004', 'Furniture',    55.00,   60, 'Adjustable aluminum monitor riser'),
('Office Chair',           'PRD-005', 'Furniture',   320.00,   20, 'Ergonomic mesh office chair with lumbar support'),
('Laptop Bag',             'PRD-006', 'Accessories',  49.99,  100, '15.6" waterproof laptop bag with pockets'),
('Notebook (A5)',          'PRD-007', 'Stationery',    8.99,  500, 'Dotted grid A5 notebook, 200 pages'),
('Ballpen Set',            'PRD-008', 'Stationery',    4.50, 1000, 'Pack of 10 ballpens, assorted colors'),
('Desk Lamp',              'PRD-009', 'Electronics',  35.00,   80, 'LED desk lamp with adjustable color temperature'),
('Cable Management Kit',   'PRD-010', 'Accessories',  18.75,  300, 'Velcro straps and cable clips bundle');
