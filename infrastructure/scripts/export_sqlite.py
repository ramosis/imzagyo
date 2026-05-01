#!/usr/bin/env python3
"""
Export SQLite data to JSON for PostgreSQL import.
Run this BEFORE switching to PostgreSQL.
"""

import json
import sqlite3
import os
from datetime import datetime
from decimal import Decimal

class JSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        if isinstance(obj, Decimal):
            return float(obj)
        return super().default(obj)

def export_table(conn, table_name):
    """Export a table to JSON."""
    cursor = conn.cursor()
    try:
        cursor.execute(f"SELECT * FROM {table_name}")
    except sqlite3.OperationalError as e:
        print(f"  ⚠️ Error exporting {table_name}: {e}")
        return None
    
    columns = [description[0] for description in cursor.description]
    rows = []
    
    for row in cursor.fetchall():
        row_dict = {}
        for i, col in enumerate(columns):
            value = row[i]
            row_dict[col] = value
        rows.append(row_dict)
    
    return {
        'table': table_name,
        'columns': columns,
        'rows': rows,
        'count': len(rows)
    }

def main():
    sqlite_path = 'data/imza_database.db'
    output_path = 'data/export.json'
    
    if not os.path.exists(sqlite_path):
        print(f"❌ SQLite file not found at {sqlite_path}")
        return

    conn = sqlite3.connect(sqlite_path)
    conn.row_factory = sqlite3.Row
    
    # Get all tables
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")
    tables = [row[0] for row in cursor.fetchall()]
    
    export_data = {
        'exported_at': datetime.now().isoformat(),
        'source': sqlite_path,
        'tables': []
    }
    
    for table in tables:
        print(f"Exporting {table}...")
        table_data = export_table(conn, table)
        if table_data:
            export_data['tables'].append(table_data)
            print(f"  → {table_data['count']} rows")
    
    conn.close()
    
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(export_data, f, cls=JSONEncoder, ensure_ascii=False, indent=2)
    
    print(f"\n✅ Export complete: {output_path}")
    total_rows = sum(t['count'] for t in export_data['tables'])
    print(f"   Total: {len(export_data['tables'])} tables, {total_rows} rows")

if __name__ == '__main__':
    main()
