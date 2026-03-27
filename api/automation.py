from flask import Blueprint, jsonify, request, g
from shared.database import get_db
from .auth import require_inner_circle, login_required
import json
import datetime

automation_bp = Blueprint('automation', __name__)

@automation_bp.route('/rules', methods=['GET'])
@require_inner_circle
def get_rules():
    with get_db() as conn:
        rules = conn.execute('SELECT * FROM automation_rules ORDER BY created_at DESC').fetchall()
    return jsonify([dict(r) for r in rules])

@automation_bp.route('/rules', methods=['POST'])
@require_inner_circle
def create_rule():
    data = request.json
    name = data.get('name')
    trigger_type = data.get('trigger_type') # time_based, status_based
    condition_json = json.dumps(data.get('condition', {}))
    action_type = data.get('action_type', 'email')
    action_template_id = data.get('action_template_id')

    if not all([name, trigger_type, action_template_id]):
        return jsonify({'error': 'Eksik veri'}), 400

    with get_db() as conn:
        cursor = conn.execute('''
            INSERT INTO automation_rules (name, trigger_type, condition_json, action_type, action_template_id)
            VALUES (?, ?, ?, ?, ?)
        ''', (name, trigger_type, condition_json, action_type, action_template_id))
        rule_id = cursor.lastrowid
        conn.commit()
    return jsonify({'status': 'success', 'id': rule_id}), 201

@automation_bp.route('/run', methods=['POST'])
@require_inner_circle
def run_automation():
    """
    Tüm aktif kuralları tarar ve aksiyonları tetikler.
    Bu uç nokta bir cron job tarafından çağrılmalıdır.
    """
    with get_db() as conn:
        cursor = conn.cursor()
        
        # 1. Aktif kuralları al
        rules = cursor.execute('SELECT * FROM automation_rules WHERE is_active = 1').fetchall()
        
        execution_stats = dict(processed=0, triggered=0, errors=0)
        
        for rule in rules:
            trigger_type = rule['trigger_type']
            conditions = json.loads(rule['condition_json'])
            template_id = rule['action_template_id']
            
            # 2. Kurallara uyan lead'leri bul
            leads = []
            if trigger_type == 'time_based':
                # Örn: 3 gündür contacted olmayanlar
                days_inactive = conditions.get('days_inactive', 0)
                if days_inactive > 0:
                    leads = cursor.execute('''
                        SELECT * FROM leads 
                        WHERE (last_contacted_at IS NULL AND created_at <= datetime('now', ?))
                           OR (last_contacted_at <= datetime('now', ?))
                    ''', (f'-{days_inactive} days', f'-{days_inactive} days')).fetchall()
            
            elif trigger_type == 'status_based':
                target_status = conditions.get('status')
                if target_status:
                    leads = cursor.execute('SELECT * FROM leads WHERE status = ?', (target_status,)).fetchall()

            # 3. Aksiyonları tetikle
            for lead in leads:
                already_sent = cursor.execute('''
                    SELECT id FROM automation_logs 
                    WHERE rule_id = ? AND lead_id = ? 
                    AND created_at >= datetime('now', '-24 hours')
                ''', (rule['id'], lead['id'])).fetchone()
                
                if already_sent:
                    continue
                
                try:
                    action_desc = f"Rule: {rule['name']} | Action: {rule['action_type']} | Template: {template_id}"
                    
                    cursor.execute('''
                        INSERT INTO automation_logs (rule_id, lead_id, action_taken, status)
                        VALUES (?, ?, ?, ?)
                    ''', (rule['id'], lead['id'], action_desc, 'success'))
                    
                    if lead['assigned_user_id']:
                        try:
                            from .notifications import create_notification
                            create_notification(
                                lead['assigned_user_id'],
                                'automation',
                                f"Otomasyon: {rule['name']}",
                                f"{lead['name']} için '{rule['name']}' kuralı çalıştırıldı ({rule['action_type']})."
                            )
                        except: pass

                    execution_stats['triggered'] += 1
                except Exception as e:
                    execution_stats['errors'] += 1
                    print(f"Automation execution error: {str(e)}")
            
            execution_stats['processed'] += 1

        conn.commit()
    return jsonify({
        'status': 'finished',
        'stats': execution_stats
    })

@automation_bp.route('/logs', methods=['GET'])
@require_inner_circle
def get_logs():
    with get_db() as conn:
        logs = conn.execute('''
            SELECT al.*, ar.name as rule_name, l.name as lead_name
            FROM automation_logs al
            JOIN automation_rules ar ON al.rule_id = ar.id
            JOIN leads l ON al.lead_id = l.id
            ORDER BY al.created_at DESC
            LIMIT 100
        ''').fetchall()
    return jsonify([dict(log) for log in logs])
