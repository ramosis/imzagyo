from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import require_inner_circle
from . import automation_bp

# HR Management
@automation_bp.route('/hr/personnel', methods=['GET'])
@require_inner_circle
def get_personnel():
    with get_db() as conn:
        personnel = conn.execute('SELECT * FROM hr_personnel ORDER BY name').fetchall()
    return jsonify([dict(p) for p in personnel])

@automation_bp.route('/hr/personnel', methods=['POST'])
@require_inner_circle
def add_personnel():
    data = request.json
    with get_db() as conn:
        cur = conn.cursor()
        cur.execute('INSERT INTO hr_personnel (name, role, department, salary, hire_date) VALUES (?,?,?,?,?)',
                    (data.get('name'), data.get('role'), data.get('department'), 
                     data.get('salary'), data.get('hire_date')))
        conn.commit()
    return jsonify({'status': 'created'}), 201

# Team Collaboration
@automation_bp.route('/team', methods=['GET'])
@require_inner_circle
def get_team():
    with get_db() as conn:
        team = conn.execute('SELECT u.id, u.username, u.role FROM users u').fetchall()
    return jsonify([dict(t) for t in team])
