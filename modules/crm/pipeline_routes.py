from flask import request, jsonify, g
from shared.database import get_db
from modules.auth.decorators import require_inner_circle, login_required
from . import crm_bp

@crm_bp.route('/pipeline/leads', methods=['GET'])
@require_inner_circle
def get_pipeline_leads():
    with get_db() as conn:
        stages = conn.execute('SELECT * FROM pipeline_stages ORDER BY order_index').fetchall()
        stages_list = [dict(s) for s in stages]
        leads = conn.execute('''
            SELECT l.*, p.baslik1 as property_title, u.username as assigned_to
            FROM leads l LEFT JOIN portfoyler p ON l.interest_property_id = p.id
            LEFT JOIN users u ON l.assigned_user_id = u.id ORDER BY l.ai_score DESC
        ''').fetchall()
    
    from modules.ai.routes import calculate_intent_score
    status_map = {1: 'New', 2: 'Contacted', 3: 'Proposal', 4: 'Proposal', 5: 'Closed'}
    
    processed_leads = []
    for l in leads:
        lead_dict = dict(l)
        with get_db() as conn:
            session_row = conn.execute('SELECT session_id FROM lead_interactions WHERE lead_id = ? LIMIT 1', (lead_dict['id'],)).fetchone()
        if session_row:
            score, interest = calculate_intent_score(session_row['session_id'])
            lead_dict['ai_score'] = score
            lead_dict['intent_category'] = interest
        else:
            lead_dict['intent_category'] = "Genel"
        processed_leads.append(lead_dict)

    for stage in stages_list:
        stage['leads'] = []
        for l in processed_leads:
            mapped_status = status_map.get(l['pipeline_stage_id'], 'New')
            if mapped_status.lower() == stage['name'].lower() or (stage['id'] == l['pipeline_stage_id']):
                l['status_label'] = mapped_status
                stage['leads'].append(l)
    return jsonify(processed_leads), 200

@crm_bp.route('/pipeline/stages', methods=['GET'])
@require_inner_circle
def get_stages():
    with get_db() as conn:
        stages = conn.execute('SELECT * FROM pipeline_stages ORDER BY order_index').fetchall()
    return jsonify([dict(s) for s in stages])

@crm_bp.route('/leads/<int:lead_id>/move', methods=['PUT'])
@login_required
def move_lead(lead_id):
    data = request.json
    new_stage_id = data.get('stage_id')
    reason = data.get('reason', 'Manuel geçiş')
    if not new_stage_id: return jsonify({'error': 'stage_id required'}), 400
    with get_db() as conn:
        lead = conn.execute('SELECT pipeline_stage_id, name, assigned_user_id FROM leads WHERE id = ?', (lead_id,)).fetchone()
        if not lead: return jsonify({'error': 'Lead not found'}), 404
        old_stage_id = lead['pipeline_stage_id']
        conn.execute('UPDATE leads SET pipeline_stage_id = ? WHERE id = ?', (new_stage_id, lead_id))
        conn.execute('INSERT INTO pipeline_history (lead_id, old_stage_id, new_stage_id, user_id, reason) VALUES (?, ?, ?, ?, ?)', 
                     (lead_id, old_stage_id, new_stage_id, g.user['id'], reason))
        conn.commit()
    return jsonify({'status': 'success'})
