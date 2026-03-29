from typing import List, Dict, Any, Optional
from shared.database import get_db

class ExpenseRepository:
    """Handles low-level SQL operations for Personnel Expenses."""
    @staticmethod
    def get_all(user_id: int = None, is_admin: bool = False) -> List[Dict[str, Any]]:
        with get_db() as conn:
            if is_admin:
                query = 'SELECT e.*, u.username as user_name FROM expenses e LEFT JOIN users u ON e.user_id = u.id ORDER BY e.date DESC'
                rows = conn.execute(query).fetchall()
            else:
                query = 'SELECT e.*, u.username as user_name FROM expenses e LEFT JOIN users u ON e.user_id = u.id WHERE e.user_id = ? ORDER BY e.date DESC'
                rows = conn.execute(query, (user_id,)).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO expenses (user_id, category, amount, description, receipt_image, date, status)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (
                data['user_id'], data.get('category'), data.get('amount'),
                data.get('description'), data.get('receipt_image'),
                data.get('date'), data.get('status', 'pending')
            ))
            conn.commit()
            return cursor.lastrowid

    @staticmethod
    def update_status(expense_id: int, status: str) -> bool:
        with get_db() as conn:
            cursor = conn.execute("UPDATE expenses SET status = ? WHERE id = ?", (status, expense_id))
            conn.commit()
            return cursor.rowcount > 0

class TaxRepository:
    """Handles low-level SQL operations for Property Taxes."""
    @staticmethod
    def get_all() -> List[Dict[str, Any]]:
        with get_db() as conn:
            query = 'SELECT t.*, p.baslik1 as property_title, p.refNo as property_ref FROM taxes t LEFT JOIN portfoyler p ON t.property_id = p.id'
            rows = conn.execute(query).fetchall()
            return [dict(r) for r in rows]

    @staticmethod
    def create(data: Dict[str, Any]) -> int:
        with get_db() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO taxes (property_id, tax_type, amount, due_date, status)
                VALUES (?, ?, ?, ?, ?)
            ''', (
                data.get('property_id'), data.get('tax_type'),
                data.get('amount'), data.get('due_date'), data.get('status')
            ))
            conn.commit()
            return cursor.lastrowid
