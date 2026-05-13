"""
generate_diagrams.py
Run once to produce docs/diagrams/erd.png and docs/diagrams/rm.png
Requires: pip install matplotlib
"""
import os, math
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch

os.makedirs('docs/diagrams', exist_ok=True)

# ────────────────────────────────────────
# Colour palette
# ────────────────────────────────────────
BG       = '#0d0f14'
CARD     = '#13161d'
BORDER   = '#2a2e3f'
ACCENT   = '#5b8dee'
TEXT     = '#e8eaf0'
TEXT2    = '#9096b0'
GREEN    = '#34d399'
RED      = '#f87171'
YELLOW   = '#fbbf24'


def draw_entity(ax, x, y, w, title, pk_fields, fields, color=ACCENT):
    """Draw an ER entity box."""
    row_h = 0.32
    header_h = 0.44
    n = len(pk_fields) + len(fields)
    total_h = header_h + n * row_h + 0.12

    # Shadow
    ax.add_patch(FancyBboxPatch((x+0.06, y-total_h-0.06), w, total_h,
                                boxstyle='round,pad=0.04', linewidth=0,
                                facecolor='#00000060', zorder=2))
    # Body
    ax.add_patch(FancyBboxPatch((x, y-total_h), w, total_h,
                                boxstyle='round,pad=0.04', linewidth=1.5,
                                edgecolor=color, facecolor=CARD, zorder=3))
    # Header band
    ax.add_patch(FancyBboxPatch((x, y-header_h), w, header_h,
                                boxstyle='round,pad=0.04', linewidth=0,
                                facecolor=color+'33', zorder=4))

    ax.text(x + w/2, y - header_h/2, title,
            ha='center', va='center', fontsize=9.5, fontweight='bold',
            color=color, zorder=5, fontfamily='monospace')

    cur_y = y - header_h - 0.06
    for f in pk_fields:
        ax.text(x + 0.14, cur_y - row_h/2, f'🔑 {f}',
                ha='left', va='center', fontsize=7.5, color=YELLOW, zorder=5, fontfamily='monospace')
        cur_y -= row_h
    for f in fields:
        ax.text(x + 0.14, cur_y - row_h/2, f'   {f}',
                ha='left', va='center', fontsize=7.5, color=TEXT2, zorder=5, fontfamily='monospace')
        cur_y -= row_h

    return (x + w/2, y - total_h/2)   # center


def arrow(ax, x1, y1, x2, y2, label='', color=ACCENT):
    ax.annotate('', xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle='->', color=color, lw=1.3),
                zorder=6)
    if label:
        mx, my = (x1+x2)/2, (y1+y2)/2
        ax.text(mx + 0.06, my, label, fontsize=7, color=color, fontfamily='monospace')


# ════════════════════════════════════════
#  ERD
# ════════════════════════════════════════
fig, ax = plt.subplots(figsize=(13, 8))
fig.patch.set_facecolor(BG)
ax.set_facecolor(BG)
ax.axis('off')
ax.set_xlim(0, 13); ax.set_ylim(0, 8)

ax.text(6.5, 7.7, 'Entity Relationship Diagram — DataVault DBMS',
        ha='center', va='center', fontsize=13, fontweight='bold',
        color=TEXT, fontfamily='monospace')

# users
draw_entity(ax, 0.4, 7.1, 3.2, 'USERS',
            ['id  INT  PK'],
            ['username  VARCHAR(50)  UNIQUE',
             'password  VARCHAR(255)',
             'role  ENUM(admin, user)',
             'created_at  TIMESTAMP'],
            color=ACCENT)

# employees
draw_entity(ax, 4.8, 7.1, 3.5, 'EMPLOYEES',
            ['id  INT  PK'],
            ['first_name  VARCHAR(50)',
             'last_name   VARCHAR(50)',
             'email  VARCHAR(100)  UNIQUE',
             'department  VARCHAR(50)',
             'position  VARCHAR(80)',
             'salary  DECIMAL(10,2)',
             'hire_date  DATE',
             'status  ENUM(active, inactive)',
             'created_at / updated_at'],
            color=GREEN)

# products
draw_entity(ax, 4.8, 2.6, 3.5, 'PRODUCTS',
            ['id  INT  PK'],
            ['name  VARCHAR(120)',
             'sku  VARCHAR(50)  UNIQUE',
             'category  VARCHAR(50)',
             'price  DECIMAL(10,2)',
             'stock  INT',
             'description  TEXT',
             'created_at / updated_at'],
            color=YELLOW)

# audit_log
draw_entity(ax, 9.4, 7.1, 3.2, 'AUDIT_LOG',
            ['id  INT  PK'],
            ['user_id  INT  FK→users.id',
             'action  VARCHAR(20)',
             'table_name  VARCHAR(50)',
             'record_id  INT',
             'description  TEXT',
             'created_at  TIMESTAMP'],
            color=RED)

# Relationships
arrow(ax, 3.6, 5.5, 4.8, 5.5, '1 logs N', color=RED)
arrow(ax, 9.4, 5.5, 3.6+0.04, 5.5)   # back-ref
ax.text(3.7, 5.75, 'user_id FK', fontsize=6.5, color=RED)

fig.savefig('docs/diagrams/erd.png', dpi=130, bbox_inches='tight',
            facecolor=BG)
plt.close(fig)
print('✓ ERD saved to docs/diagrams/erd.png')


# ════════════════════════════════════════
#  Relational Model
# ════════════════════════════════════════
fig2, ax2 = plt.subplots(figsize=(13, 6))
fig2.patch.set_facecolor(BG)
ax2.set_facecolor(BG)
ax2.axis('off')
ax2.set_xlim(0, 13); ax2.set_ylim(0, 6)

ax2.text(6.5, 5.75, 'Relational Model Diagram — DataVault DBMS',
         ha='center', va='center', fontsize=13, fontweight='bold',
         color=TEXT, fontfamily='monospace')


def rm_table(ax, x, y, w, title, rows, color=ACCENT):
    row_h = 0.28
    hdr_h = 0.38
    total_h = hdr_h + len(rows)*row_h + 0.1

    ax.add_patch(FancyBboxPatch((x, y-total_h), w, total_h,
                                boxstyle='round,pad=0.03', linewidth=1.5,
                                edgecolor=color, facecolor=CARD, zorder=3))
    ax.add_patch(FancyBboxPatch((x, y-hdr_h), w, hdr_h,
                                boxstyle='round,pad=0.03', linewidth=0,
                                facecolor=color+'33', zorder=4))
    ax.text(x+w/2, y-hdr_h/2, title,
            ha='center', va='center', fontsize=9, fontweight='bold',
            color=color, zorder=5, fontfamily='monospace')

    cy = y - hdr_h - 0.05
    for name, attrs in rows:
        style = 'bold' if 'PK' in attrs else 'normal'
        col = YELLOW if 'PK' in attrs else (RED if 'FK' in attrs else TEXT2)
        ax.text(x+0.12, cy-row_h/2, name,
                fontsize=7, color=col, fontweight=style,
                zorder=5, fontfamily='monospace')
        ax.text(x+w-0.12, cy-row_h/2, attrs,
                fontsize=6.5, color=TEXT2, ha='right',
                zorder=5, fontfamily='monospace')
        cy -= row_h

    return (x+w, y-total_h/2), (x, y-total_h/2)   # right-edge, left-edge


r_users, _ = rm_table(ax2, 0.3, 5.3, 2.8, 'users', [
    ('id',         'INT  PK'),
    ('username',   'VARCHAR(50)  UNIQUE'),
    ('password',   'VARCHAR(255)'),
    ('role',       'ENUM'),
    ('created_at', 'TIMESTAMP'),
], color=ACCENT)

r_emp, l_emp = rm_table(ax2, 4.7, 5.3, 3.5, 'employees', [
    ('id',         'INT  PK'),
    ('first_name', 'VARCHAR(50)'),
    ('last_name',  'VARCHAR(50)'),
    ('email',      'VARCHAR(100)  UNIQUE'),
    ('department', 'VARCHAR(50)'),
    ('position',   'VARCHAR(80)'),
    ('salary',     'DECIMAL(10,2)'),
    ('hire_date',  'DATE'),
    ('status',     'ENUM'),
], color=GREEN)

_, l_prod = rm_table(ax2, 4.7, 1.8, 3.5, 'products', [
    ('id',          'INT  PK'),
    ('name',        'VARCHAR(120)'),
    ('sku',         'VARCHAR(50)  UNIQUE'),
    ('category',    'VARCHAR(50)'),
    ('price',       'DECIMAL(10,2)'),
    ('stock',       'INT'),
    ('description', 'TEXT'),
], color=YELLOW)

r_audit, l_audit = rm_table(ax2, 9.4, 5.3, 3.3, 'audit_log', [
    ('id',          'INT  PK'),
    ('user_id',     'INT  FK → users.id'),
    ('action',      'VARCHAR(20)'),
    ('table_name',  'VARCHAR(50)'),
    ('record_id',   'INT'),
    ('description', 'TEXT'),
    ('created_at',  'TIMESTAMP'),
], color=RED)

# FK arrows
ax2.annotate('', xy=(l_audit[0]-0.02, l_audit[1]),
             xytext=(r_users[0]+0.02, r_users[1]),
             arrowprops=dict(arrowstyle='->', color=RED, lw=1.2,
                             connectionstyle='arc3,rad=0.1'), zorder=6)
ax2.text(6.2, 4.1, 'user_id FK', fontsize=7, color=RED, fontfamily='monospace')

fig2.savefig('docs/diagrams/rm.png', dpi=130, bbox_inches='tight',
             facecolor=BG)
plt.close(fig2)
print('✓ Relational Model saved to docs/diagrams/rm.png')
