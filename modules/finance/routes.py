import urllib.request
from bs4 import BeautifulSoup
from flask import request, jsonify, g
from shared.database import get_db
from modules.auth.decorators import require_inner_circle, login_required
from . import finance_bp

TCMB_URL = "https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Bankacilik+Verileri/Degisken+Faizli+Konut+Finansmani+Sozlesmelerinde+Kullanilacak+Referans+Faizler+ve+Endeksler/"

@finance_bp.route('/tcmb-rates', methods=['GET'])
def get_tcmb_rates():
    """Fetches real-time reference mortgage rates from TCMB."""
    try:
        req = urllib.request.Request(TCMB_URL, headers={'User-Agent': 'Mozilla/5.0'})
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        tables = soup.find_all('table')
        if not tables: return jsonify({'error': 'Table not found'}), 500
        cols = tables[0].find_all('tr')[1].find_all('td')
        if len(cols) >= 4:
            return jsonify({'source': 'TCMB', 'date': cols[3].text.strip(), 'rate': cols[2].text.strip()})
        return jsonify({'error': 'Matrix mismatch'}), 500
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@finance_bp.route('/summary', methods=['GET'])
@require_inner_circle
def get_financial_summary():
    """Generates high-level corporate financial summary."""
    with get_db() as conn:
        portfolios = conn.execute('SELECT fiyat FROM portfoyler').fetchall()
        total_value = 0
        for p in portfolios:
            try: total_value += int(''.join(filter(str.isdigit, p['fiyat'])))
            except: continue
        expenses = conn.execute('SELECT SUM(amount) as total FROM expenses WHERE status = "approved"').fetchone()
        commissions = conn.execute('SELECT SUM(amount) as total FROM commissions WHERE status = "pending"').fetchone()
        contracts_count = conn.execute('SELECT COUNT(*) as count FROM contracts WHERE status = "active"').fetchone()['count']
    return jsonify({
        'total_portfolio_value': total_value,
        'approved_expenses': expenses['total'] or 0,
        'pending_commissions': commissions['total'] or 0,
        'active_contracts': contracts_count,
        'currency': 'TRY'
    })
