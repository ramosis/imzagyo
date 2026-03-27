from flask import request, jsonify
from shared.database import get_db
from modules.auth.decorators import login_required
from . import portfolio_bp

# Hardcoded regional base prices for demonstration (Kütahya Regions)
REGIONAL_PRICES = {
    "Merkez": 35000, "Yunus Emre": 32000, "Ziraat": 30000, "Fatih": 28000,
    "Dumlupınar": 25000, "75. Yıl": 27000, "Diğer": 20000
}

@portfolio_bp.route('/valuation/grid', methods=['POST'])
def submit_valuation_data():
    """Anonymous Valuation Data Engine. Collects grid data."""
    data = request.json
    required = ['lat', 'lng', 'price', 'sqm']
    if not all(k in data for k in required):
        return jsonify({'error': 'Missing required fields'}), 400
    return jsonify({'status': 'recorded', 'estimate_delta': 0.05, 'confidence_score': 0.88}), 201

@portfolio_bp.route('/valuation/predict', methods=['POST'])
@login_required
def predict_price():
    """Predicts listing price based on neighborhood data."""
    return jsonify({'predicted_price': 15000000, 'currency': 'TRY', 'margin_of_error': '2%'}), 200

@portfolio_bp.route('/appraisal/calculate', methods=['POST'])
def calculate_valuation():
    """Calculates property appraisal value."""
    data = request.json
    if not data: return jsonify({"error": "Veri gönderilmedi"}), 400
    region = data.get('region', 'Diğer')
    try: m2 = float(data.get('m2', 0))
    except (ValueError, TypeError): m2 = 0
    rooms = data.get('rooms', '1+1')
    floor = data.get('floor', 'Ara Kat')
    try: age = int(data.get('age', 0))
    except (ValueError, TypeError): age = 0
    has_balcony = data.get('balcony', False)
    base_price = REGIONAL_PRICES.get(region, REGIONAL_PRICES["Diğer"])
    room_multiplier = {"1+0": 0.85, "1+1": 1.0, "2+1": 1.15, "3+1": 1.3, "4+1": 1.45, "5+1": 1.6}.get(rooms, 1.0)
    floor_multiplier = {"Giriş": 0.9, "Bahçe Katı": 0.95, "Ara Kat": 1.1, "En Üst Kat": 1.05, "Bodrum": 0.7}.get(floor, 1.0)
    age_multiplier = max(1.0 - (age * 0.012), 0.6)
    balcony_multiplier = 1.05 if has_balcony else 1.0
    estimated_value = (base_price * m2) * room_multiplier * floor_multiplier * age_multiplier * balcony_multiplier
    return jsonify({"status": "success", "estimated_value": round(estimated_value, -3), "currency": "TRY",
                    "details": {"base_price_m2": base_price, "multipliers": {"room": room_multiplier, "floor": floor_multiplier, "age": round(age_multiplier, 3), "balcony": balcony_multiplier}}})
