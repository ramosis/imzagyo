from typing import Optional, List, Dict, Any
from dataclasses import dataclass
import uuid
import json
import bleach
from flask import Blueprint, request, jsonify, g
from database import get_db
from api.ai import translate_content
from api.utils import sanitize_input, sanitize_html
from extensions import cache
from .schemas import portfolio_schema, ValidationError
from .auth import require_permission

portfolio_bp = Blueprint('portfolio', __name__)

class PortfolioRepository:
    """Handles low-level SQL operations for Portfolios (Section 5.3)."""
    
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            rows = conn.execute('SELECT * FROM portfoyler').fetchall()
            return [dict(row) for row in rows]

    @staticmethod
    def get_by_id(portfolio_id: str) -> Optional[Dict[str, Any]]:
        with get_db() as conn:
            row = conn.execute('SELECT * FROM portfoyler WHERE id = ?', (portfolio_id,)).fetchone()
            return dict(row) if row else None

    @staticmethod
    def create(data: Dict[str, Any]) -> str:
        with get_db() as conn:
            # Generate UUID if not provided
            if not data.get('id'):
                data['id'] = str(uuid.uuid4())
            
            # Map ozellikler_arr to ozellikler (DB column)
            if 'ozellikler_arr' in data:
                data['ozellikler'] = json.dumps(data.pop('ozellikler_arr'))
            
            columns = ', '.join(data.keys())
            placeholders = ', '.join(['?' for _ in data])
            query = f"INSERT INTO portfoyler ({columns}) VALUES ({placeholders})"
            
            conn.execute(query, list(data.values()))
            conn.commit()
            return data['id']

    @staticmethod
    def update(portfolio_id: str, update_data: Dict[str, Any]) -> bool:
        with get_db() as conn:
            if 'ozellikler_arr' in update_data:
                update_data['ozellikler'] = json.dumps(update_data.pop('ozellikler_arr'))
                
            fields = [f"{k} = ?" for k in update_data.keys()]
            if not fields:
                return False
                
            values = list(update_data.values()) + [portfolio_id]
            query = f"UPDATE portfoyler SET {', '.join(fields)} WHERE id = ?"
            cursor = conn.execute(query, values)
            conn.commit()
            return cursor.rowcount > 0

    @staticmethod
    def get_owner_id(portfolio_id: str) -> Optional[int]:
        with get_db() as conn:
            row = conn.execute('SELECT owner_id FROM portfoyler WHERE id = ?', (portfolio_id,)).fetchone()
            return row['owner_id'] if row else None

    @staticmethod
    def delete(portfolio_id: str) -> bool:
        with get_db() as conn:
            cursor = conn.execute('DELETE FROM portfoyler WHERE id = ?', (portfolio_id,))
            conn.commit()
            return cursor.rowcount > 0

class PortfolioService:
    """Handles business logic and transformations for Portfolios (Section 5.3)."""

    @staticmethod
    def process_and_create(data: Dict[str, Any]) -> Dict[str, Any]:
        # 1. Validation & Basic Sanitization (Audit Section 6.2)
        sanitized_data = sanitize_input(data) # Recursive strip by default
        validated_data = portfolio_schema.load(sanitized_data)
        
        # 2. Rich Text Sanitization (Overriding 'hikaye' with allowed tags)
        if 'hikaye' in validated_data:
             validated_data['hikaye'] = sanitize_html(validated_data['hikaye'])
        
        # 3. AI Automation (Phase 4)
        target_fields = ['baslik1', 'baslik2', 'lokasyon', 'hikaye']
        for field in target_fields:
            if field in validated_data:
                source = validated_data[field]
                validated_data[f'{field}_en'] = translate_content(source, 'İngilizce')
                validated_data[f'{field}_ar'] = translate_content(source, 'Arapça')

        # 4. Persistence
        new_id = PortfolioRepository.create(validated_data)
        return PortfolioRepository.get_by_id(new_id)

    @staticmethod
    def can_manage_portfolio(user: Dict[str, Any], portfolio_id: str) -> bool:
        """Checks if a user has authority over a specific portfolio (Audit 5.2)."""
        if user.get('role') in ['admin', 'super_admin', 'broker']:
            return True # Inner circle has global access
        
        owner_id = PortfolioRepository.get_owner_id(portfolio_id)
        return owner_id == user.get('id')

@portfolio_bp.route('/api/portfoyler', methods=['GET'])
@cache.cached(timeout=300, query_string=True)
def get_portfolios():
    """
    List all portfolios
    ---
    responses:
      200:
        description: A list of portfolios
    """
    return jsonify(PortfolioRepository.get_all())

@portfolio_bp.route('/api/portfoyler/<id>', methods=['GET'])
@cache.memoize(timeout=600)
def get_portfolio(id):
    """
    Get a single portfolio by ID
    ---
    parameters:
      - name: id
        in: path
        type: string
        required: true
    responses:
      200:
        description: Portfolio details
      404:
        description: Portfolio not found
    """
    portfolio = PortfolioRepository.get_by_id(id)
    if not portfolio:
        return jsonify({"error": "Portföy bulunamadı"}), 404
    return jsonify(portfolio)

@portfolio_bp.route('/api/portfoyler', methods=['POST'])
@require_permission('portfolio.create')
def add_portfolio():
    try:
        portfolio = PortfolioService.process_and_create(request.json)
        return jsonify(portfolio), 201
    except ValidationError as err:
        return jsonify({"error": "Geçersiz veri", "details": err.messages}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@portfolio_bp.route('/api/portfoyler/<id>', methods=['PUT'])
@require_permission('portfolio.edit')
def update_portfolio(id):
    user = g.user
    if not PortfolioService.can_manage_portfolio(user, id):
        return jsonify({'error': 'Unauthorized - Owner only (Section 6.2)'}), 403
        
    if PortfolioRepository.update(id, request.json):
        return jsonify({'status': 'updated'}), 200
    return jsonify({'error': 'Portföy bulunamadı'}), 404

@portfolio_bp.route('/api/portfoyler/<id>', methods=['DELETE'])
@require_permission('portfolio.delete')
def delete_portfolio(id):
    user = g.user
    if not PortfolioService.can_manage_portfolio(user, id):
        return jsonify({'error': 'Unauthorized - Owner only (Section 6.2)'}), 403

    if PortfolioRepository.delete(id):
        return jsonify({"status": "deleted"}), 200
    return jsonify({"error": "Portföy bulunamadı"}), 404
