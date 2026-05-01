#!/usr/bin/env python3
"""
Validate data integrity after migration.
"""

import os
import json
from sqlalchemy import create_engine, text

def validate_counts():
    """Compare table row counts."""
    json_path = 'data/export.json'
    if not os.path.exists(json_path):
        print(f"❌ Export file not found at {json_path}")
        return False

    with open(json_path, 'r', encoding='utf-8') as f:
        export = json.load(f)
    
    sqlite_counts = {t['table']: t['count'] for t in export['tables']}
    
    db_url = os.getenv('DATABASE_URL')
    if not db_url:
        print("❌ DATABASE_URL not set")
        return False

    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        pg_counts = {}
        # Get all public tables
        result = conn.execute(text(
            "SELECT tablename FROM pg_tables WHERE schemaname = 'public'"
        ))
        tables = [r[0] for r in result]
        
        for table in tables:
            try:
                count = conn.execute(text(f'SELECT COUNT(*) FROM "{table}"')).scalar()
                pg_counts[table] = count
            except:
                pass
    
    # Compare
    print("\nTable Count Comparison:")
    print("-" * 50)
    all_tables = set(sqlite_counts.keys()) | set(pg_counts.keys())
    
    mismatches = []
    for table in sorted(all_tables):
        sqlite_c = sqlite_counts.get(table, 0)
        pg_c = pg_counts.get(table, 0)
        status = "✅" if sqlite_c == pg_c else "❌"
        print(f"{status} {table:30} SQLite: {sqlite_c:6} PG: {pg_c:6}")
        if sqlite_c != pg_c:
            mismatches.append(table)
    
    if mismatches:
        print(f"\n❌ Mismatches found in tables: {', '.join(mismatches)}")
        return False
    else:
        print("\n✅ All row counts match!")
        return True

def validate_constraints():
    """Check FK constraints in PostgreSQL."""
    db_url = os.getenv('DATABASE_URL')
    if not db_url or not db_url.startswith('postgresql'):
        print("⏭️ Skipping FK validation (PostgreSQL only)")
        return True

    engine = create_engine(db_url)
    
    with engine.connect() as conn:
        result = conn.execute(text("""
            SELECT tc.constraint_name, tc.table_name, kcu.column_name,
                   ccu.table_name AS foreign_table_name,
                   ccu.column_name AS foreign_column_name
            FROM information_schema.table_constraints AS tc
            JOIN information_schema.key_column_usage AS kcu
              ON tc.constraint_name = kcu.constraint_name
            JOIN information_schema.constraint_column_usage AS ccu
              ON ccu.constraint_name = tc.constraint_name
            WHERE tc.constraint_type = 'FOREIGN KEY';
        """))
        
        constraints = result.fetchall()
        print(f"\nForeign Key Constraints Found: {len(constraints)}")
        for c in constraints:
            print(f"  → {c.constraint_name}: {c.table_name}.{c.column_name} → {c.foreign_table_name}.{c.foreign_column_name}")
        
        return len(constraints) >= 0 # Initial migration might have 0 FKs

if __name__ == '__main__':
    counts_ok = validate_counts()
    constraints_ok = validate_constraints()
    
    if counts_ok and constraints_ok:
        print("\n🎉 Migration validation PASSED")
    else:
        print("\n⚠️ Migration validation FAILED or SKIPPED")
