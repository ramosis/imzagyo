import urllib.request
import urllib.error
from bs4 import BeautifulSoup
from flask import Blueprint, jsonify

finance_bp = Blueprint('finance', __name__)

TCMB_URL = "https://www.tcmb.gov.tr/wps/wcm/connect/TR/TCMB+TR/Main+Menu/Istatistikler/Bankacilik+Verileri/Degisken+Faizli+Konut+Finansmani+Sozlesmelerinde+Kullanilacak+Referans+Faizler+ve+Endeksler/"

@finance_bp.route('/api/tcmb-rates', methods=['GET'])
def get_tcmb_rates():
    try:
        req = urllib.request.Request(
            TCMB_URL, 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        html = urllib.request.urlopen(req).read()
        soup = BeautifulSoup(html, 'html.parser')
        
        # Sayfada tabloları bulalım
        tables = soup.find_all('table')
        if not tables:
            return jsonify({'error': 'TCMB sayfasında veri tablosu bulunamadı.'}), 500
            
        rate_table = tables[0]
        # İlk veri satırını (indeks 1, index 0 genelde başlıktır) alalım
        rows = rate_table.find_all('tr')
        if len(rows) < 2:
            return jsonify({'error': 'Tablo içeriği anlaşılamadı.'}), 500
            
        latest_row = rows[1]
        cols = latest_row.find_all('td')
        
        # Kullanıcının verdiği veriye göre: 
        # [0] Sözleşme Düzenlenirken Esas Alınacak Oran (%)
        # [1] Geçerlilik Dönemi
        # [2] Faiz Oranı Ayarlaması Yapılırken Esas Alınacak Oran (%) 
        # [3] Geçerlilik Dönemi
        if len(cols) >= 4:
            rate_str = cols[2].text.strip()
            date_str = cols[3].text.strip()
            
            # rate_str formatı genelde "61,78" şeklinde olur, sayısala çevirelim
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
            
    except urllib.error.URLError as e:
        return jsonify({'error': f'Ağa erişim hatası: {str(e)}'}), 500
    except Exception as e:
        return jsonify({'error': f'Beklenmeyen hata: {str(e)}'}), 500
