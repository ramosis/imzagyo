from flask import Blueprint, jsonify
from shared.database import get_db

team_bp = Blueprint('team', __name__)

@team_bp.route('', methods=['GET'])
def get_team():
    """
    Returns the list of team members (Audit Fix Phase 13).
    Standardized to English endpoint name.
    """
    with get_db() as conn:
        rows = conn.execute('SELECT * FROM ekip').fetchall()
    
    import json
    result = []
    for row in rows:
        d = dict(row)
        # Standardize JSON fields
        if d.get('detaylar'):
            try: d['details'] = json.loads(d.pop('detaylar'))
            except: d['details'] = []
        if d.get('uzmanlikAlanlari'):
            try: d['specialties'] = json.loads(d.pop('uzmanlikAlanlari'))
            except: d['specialties'] = []
            
        # Map Turkish columns to English for consistency (DX Phase 13)
        d['name'] = d.pop('isim')
        d['title'] = d.pop('unvan')
        d['image'] = d.pop('resim')
        d['phone'] = d.pop('telefon')
        d['type'] = d.pop('tip')
        
        result.append(d)
        
    return jsonify(result)
