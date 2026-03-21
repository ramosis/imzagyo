import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify, request, g
from database import get_db_connection
from api.auth import require_inner_circle, login_required
import datetime

finance_bp = Blueprint('finance', __name__)

TCMB_URL = "https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Bankacilik+Verileri/Degisken+Faizli+Konut+Finansmani+Sozlesmelerinde+Kullanilacak+Referans+Faizler+ve+Endeksler/"

@finance_bp.route('/api/tcmb-rates', methods=['GET'])
def get_tcmb_rates():
    """TCMB'den güncel faiz oranlarını çeker."""
    try:
        req = urllib.request.Request(
            TCMB_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        tables = soup.find_all('table')
        if not tables:
            return jsonify({'error': 'TCMB sayfasında veri tablosu bulunamadı.'}), 500
            
        rate_table = tables[0]
        rows = rate_table.find_all('tr')
        if len(rows) < 2:
            return jsonify({'error': 'Tablo içeriği anlaşılamadı.'}), 500
            
        latest_row = rows[1]
        cols = latest_row.find_all('td')
        
        if len(cols) >= 4:
            rate_str = cols[2].text.strip()
            date_str = cols[3].text.strip()
            
            try:
                rate_value = float(rate_str.replace(',', '.'))
            except ValueError:
                rate_value = rate_str
                
            return jsonify({
                'source': 'TCMB',
                'date': date_str,
                'rate': rate_value,
                'raw_rate_str': rate_str
            })
        else:
            return jsonify({'error': 'Matris uyumsuzluğu.'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# --- PERSONEL HARCAMA YÖNETİMİ ---

@finance_bp.route('/api/finance/expenses', methods=['GET'])
@require_inner_circle
def get_expenses():
    """Personel harcamalarını listeler."""
    status = request.args.get('status', 'pending')
    conn = get_db_connection()
    expenses = conn.execute('''
        SELECT e.*, u.username 
        FROM expenses e
        JOIN users u ON e.user_id = u.id
        WHERE e.status = ?
    ''', (status,)).fetchall()
    conn.close()
    return jsonify([dict(row) for row in expenses])

@finance_bp.route('/api/finance/expenses', methods=['POST'])
@login_required
def add_expense():
    """Yeni bir harcama talebi oluşturur."""
    data = request.json
    user_id = g.user['id']
    category = data.get('category')
    amount = data.get('amount')
    description = data.get('description')
    date = data.get('date', datetime.datetime.now().strftime('%Y-%m-%d'))
    
    if not all([category, amount]):
        return jsonify({'error': 'Kategori ve miktar gereklidir'}), 400
        
    conn = get_db_connection()
    conn.execute('''
        INSERT INTO expenses (user_id, category, amount, description, date, status)
        VALUES (?, ?, ?, ?, ?, 'pending')
    ''', (user_id, category, amount, description, date))
    conn.commit()
    conn.close()
    
    return jsonify({'status': 'success', 'message': 'Harcama talebi oluşturuldu'}), 201

# --- FİNANSAL ÖZET VE RAPORLAMA ---

@finance_bp.route('/api/finance/summary', methods=['GET'])
@require_inner_circle
def get_financial_summary():
    """Şirket genel finansal özetini getirir."""
    conn = get_db_connection()
    
    # 1. Toplam Portföy Değeri (Basit bir toplama, fiyatlar string olduğu için temizleme gerekebilir)
    # Burada fiyat formatı "₺35.000.000" şeklinde olduğu için sadece sayısal olmayanları temizliyoruz.
    portfolios = conn.execute('SELECT fiyat FROM portfoyler').fetchall()
    total_value = 0
    for p in portfolios:
        try:
            val = int(''.join(filter(str.isdigit, p['fiyat'])))
            total_value += val
        except:
            continue
            
    # 2. Onaylanmış Harcamalar
    expenses = conn.execute('SELECT SUM(amount) as total FROM expenses WHERE status = "approved"').fetchone()
    total_expenses = expenses['total'] or 0
    
    # 3. Bekleyen Komisyonlar
    commissions = conn.execute('SELECT SUM(amount) as total FROM commissions WHERE status = "pending"').fetchone()
    pending_commissions = commissions['total'] or 0
    
    # 4. Aktif Sözleşme Sayısı
    contracts_count = conn.execute('SELECT COUNT(*) as count FROM contracts WHERE status = "active"').fetchone()['count']
    
    conn.close()
    
    return jsonify({
        'total_portfolio_value': total_value,
        'approved_expenses': total_expenses,
        'pending_commissions': pending_commissions,
        'active_contracts': contracts_count,
        'currency': 'TRY'
    })
