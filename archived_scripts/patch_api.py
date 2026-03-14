import sys

with open('api/contracts.py', 'r', encoding='utf-8') as f:
    content = f.read()

# Replace the get_contracts endpoint
new_get = """@contracts_bp.route('/api/contracts', methods=['GET'])
@admin_required
def get_contracts():
    conn = get_db_connection()
    # Join with users, portfoyler, and parties to get full information
    query = '''
        SELECT c.*, p.baslik1, p.refNo, u.username, u.role,
               sp.name as seller_name, bp.name as buyer_name
        FROM contracts c
        LEFT JOIN portfoyler p ON c.property_id = p.id
        LEFT JOIN users u ON c.user_id = u.id
        LEFT JOIN parties sp ON c.seller_id = sp.id
        LEFT JOIN parties bp ON c.buyer_id = bp.id
        ORDER BY c.created_at DESC
    '''
    contracts = conn.execute(query).fetchall()
    conn.close()
    return jsonify([dict(c) for c in contracts]), 200"""

# Replace the add_contract endpoint
new_post = """@contracts_bp.route('/api/contracts', methods=['POST'])
@admin_required
def add_contract():
    data = request.json
    conn = get_db_connection()
    cur = conn.cursor()
    user_id = data.get('user_id', 1)
    
    cur.execute('''
        INSERT INTO contracts (
            property_id, user_id, seller_id, buyer_id, contract_type, special_conditions, status
        )
        VALUES (?,?,?,?,?,?,?)
    ''', (
        data.get('property_id'), 
        user_id, 
        data.get('seller_id'), 
        data.get('buyer_id'), 
        data.get('contract_type'),
        data.get('special_conditions'),
        data.get('status', 'draft')
    ))
    conn.commit()
    conn.close()
    return jsonify({'status': 'created'}), 201"""

old_get_start = content.find("@contracts_bp.route('/api/contracts', methods=['GET'])")
old_get_end = content.find("@contracts_bp.route('/api/contracts', methods=['POST'])")

old_post_start = content.find("@contracts_bp.route('/api/contracts', methods=['POST'])")
old_post_end = content.find("@contracts_bp.route('/api/contracts/<int:id>', methods=['PUT'])")

if old_get_start != -1 and old_post_start != -1:
    before = content[:old_get_start]
    after = content[old_post_end:]
    final_content = before + new_get + "\n\n" + new_post + "\n\n" + after
    with open('api/contracts.py', 'w', encoding='utf-8') as f:
        f.write(final_content)
    print("Updated api/contracts.py successfully.")
else:
    print("Could not find the endpoints.")
