from flask import Blueprint, jsonify, request, g
from shared.database import get_db_connection
from .auth import require_inner_circle, login_required
import datetime

pipeline_bp = Blueprint('pipeline', __name__)

@pipeline_bp.route('/api/pipeline/leads', methods=['GET'])
@require_inner_circle
def get_pipeline_leads():
    """
    Tüm aşamaları ve içindeki adayları Kanban formatında döndürür.
    Real-time AI Score entegrasyonu ile.
    """
    conn = get_db_connection()
    
    # 1. Aşamaları al
    stages = conn.execute('SELECT * FROM pipeline_stages ORDER BY order_index').fetchall()
    stages_list = [dict(s) for s in stages]
    
    # 2. Adayları al
    leads = conn.execute('''
        SELECT l.id, l.name, l.phone, l.email, l.pipeline_stage_id, l.ai_score, l.status,
               l.interest_property_id, p.baslik1 as property_title, u.username as assigned_to
        FROM leads l
        LEFT JOIN portfoyler p ON l.interest_property_id = p.id
        LEFT JOIN users u ON l.assigned_user_id = u.id
        ORDER BY l.ai_score DESC
    ''').fetchall()
    
    # 3. LMetrics Entegrasyonu (Real-time scoring)
    from .lmetrics import calculate_intent_score
    
    processed_leads = []
    for l in leads:
        lead_dict = dict(l)
        # Session eşleşmesi üzerinden anlık skor çekmeyi dene
        session_row = conn.execute('SELECT session_id FROM lead_interactions WHERE lead_id = ? LIMIT 1', (lead_dict['id'],)).fetchone()
        if session_row:
            score, interest = calculate_intent_score(session_row['session_id'])
            lead_dict['ai_score'] = score
            lead_dict['intent_category'] = interest
        else:
            lead_dict['intent_category'] = "Genel"
            
        processed_leads.append(lead_dict)

    # Gruplama
    for stage in stages_list:
        # DB status vs id eşleşmesi (pipeline.html status stringi bekliyor olabilir)
        # pipeline.html'de renderLeads columns[lead.status] kullanıyor.
        # Bizim leads tablomuzdaki status 'new', 'contacted' vb.
        # pipeline.html'deki data-status değerleri: 'New', 'Contacted', 'Proposal', 'Closed'
        # Bu mapping'i backend'de yapalım.
        status_map = {
            1: 'New',
            2: 'Contacted',
            3: 'Proposal',
            4: 'Proposal', # Genişletilebilir
            5: 'Closed'
        }
        stage['leads'] = []
        for l in processed_leads:
            mapped_status = status_map.get(l['pipeline_stage_id'], 'New')
            if mapped_status.lower() == stage['name'].lower() or \
               (stage['id'] == l['pipeline_stage_id']):
                l['status_label'] = mapped_status
                stage['leads'].append(l)
    
    conn.close()
    return jsonify(processed_leads), 200

# Eski endpoint'i de uyumluluk için tutuyoruz
@pipeline_bp.route('/api/pipeline', methods=['GET'])
@require_inner_circle
def get_pipeline_legacy():
    return get_pipeline_leads()

@pipeline_bp.route('/api/pipeline/stages', methods=['GET'])
@require_inner_circle
def get_stages():
    """Sadece aşama listesini döner."""
    conn = get_db_connection()
    stages = conn.execute('SELECT * FROM pipeline_stages ORDER BY order_index').fetchall()
    conn.close()
    return jsonify([dict(s) for s in stages])

@pipeline_bp.route('/api/pipeline/leads/<int:lead_id>', methods=['PUT'])
@login_required
def update_lead_status_route(lead_id):
    """pipeline.html tarafından kullanılan put rotası."""
    data = request.json
    new_status_str = data.get('status') # 'New', 'Contacted' vb.
    
    status_to_id = {
        'New': 1,
        'Contacted': 2,
        'Proposal': 3,
        'Closed': 5
    }
    
    target_stage_id = status_to_id.get(new_status_str, 1)
    
    # move_lead fonksiyonunu manuel çağırmak yerine iç mantığı buraya koyabiliriz veya onu refaktör edebiliriz.
    # Şimdilik direkt güncelleme yapalım.
    conn = get_db_connection()
    conn.execute('UPDATE leads SET pipeline_stage_id = ? WHERE id = ?', (target_stage_id, lead_id))
    conn.commit()
    conn.close()
    return jsonify({'status': 'success'})

@pipeline_bp.route('/api/leads/<int:lead_id>/move', methods=['PUT'])
@login_required
def move_lead(lead_id):
    """
    Bir adayı başka bir aşamaya taşır ve tarihçeye kaydeder.
    """
    data = request.json
    new_stage_id = data.get('stage_id')
    reason = data.get('reason', 'Manuel geçiş')
    user_id = g.user['id']

    if not new_stage_id:
        return jsonify({'error': 'stage_id gereklidir'}), 400

    conn = get_db_connection()
    
    # Mevcut aşamayı al (Tarihçe için)
    lead = conn.execute('SELECT pipeline_stage_id FROM leads WHERE id = ?', (lead_id,)).fetchone()
    if not lead:
        conn.close()
        return jsonify({'error': 'Aday bulunamadı'}), 404
    
    old_stage_id = lead['pipeline_stage_id']
    
    # Güncelleme
    conn.execute('UPDATE leads SET pipeline_stage_id = ? WHERE id = ?', (new_stage_id, lead_id))
    
    # --- Akıllı Bildirim: Danışmana Bilgi Ver ---
    lead_data = conn.execute('SELECT name, assigned_user_id FROM leads WHERE id = ?', (lead_id,)).fetchone()
    if lead_data and lead_data['assigned_user_id']:
        from .notifications import create_notification
        stage_row = conn.execute('SELECT name FROM pipeline_stages WHERE id = ?', (new_stage_id,)).fetchone()
        stage_name = stage_row['name'] if stage_row else 'Bilinmeyen'
        create_notification(
            lead_data['assigned_user_id'], 
            'pipeline', 
            'Huni Aşama Geçişi', 
            f"{lead_data['name']} adlı aday '{stage_name}' aşamasına taşındı."
        )
    
    # Tarihçe Logu
    conn.execute('''
        INSERT INTO pipeline_history (lead_id, old_stage_id, new_stage_id, user_id, reason)
        VALUES (?, ?, ?, ?, ?)
    ''', (lead_id, old_stage_id, new_stage_id, user_id, reason))
    
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Aday başarıyla taşındı'})

@pipeline_bp.route('/api/pipeline/insights', methods=['GET'])
@require_inner_circle
def get_pipeline_insights():
    """
    Hunideki tıkanıklıkları ve verimliliği analiz eder.
    """
    conn = get_db_connection()
    
    # Aşama bazlı sayısal dağılım
    stats = conn.execute('''
        SELECT s.name, COUNT(l.id) as count
        FROM pipeline_stages s
        LEFT JOIN leads l ON s.id = l.pipeline_stage_id
        GROUP BY s.id
        ORDER BY s.order_index
    ''').fetchall()
    
    # Ortalama geçiş süresi (Örn: İlk Temas -> Randevu)
    # Bu analiz için pipeline_history verisi kullanılabilir (İleri seviye)
    
    conn.close()
    return jsonify({
        'distribution': [dict(row) for row in stats],
        'total_leads': sum(row['count'] for row in stats)
    })
