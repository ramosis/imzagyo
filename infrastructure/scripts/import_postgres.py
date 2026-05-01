#!/usr/bin/env python3
"""
Import JSON export into PostgreSQL.
Run this AFTER creating PostgreSQL tables with Alembic.
"""

import json
import os
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker

def main():
    json_path = 'data/export.json'
    db_url = os.getenv('DATABASE_URL')
    
    if not db_url:
        print("❌ DATABASE_URL not set")
        return
    
    if not os.path.exists(json_path):
        print(f"❌ Export file not found at {json_path}")
        return

    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    
    with open(json_path, 'r', encoding='utf-8') as f:
        export_data = json.load(f)
    
    print(f"Importing from {export_data['source']}")
    print(f"Exported at: {export_data['exported_at']}\n")
    
    for table_data in export_data['tables']:
        table_name = table_data['table']
        rows = table_data['rows']
        
        if not rows:
            print(f"⏭️  Skipping {table_name} (empty)")
            continue
        
        print(f"Importing {table_name}: {len(rows)} rows...")
        
        # Get columns
        columns = list(rows[0].keys())
        col_names = ', '.join(f'"{c}"' for c in columns)
        placeholders = ', '.join(f':{c}' for c in columns)
        
        # Insert query
        query = text(f'INSERT INTO "{table_name}" ({col_names}) VALUES ({placeholders})')
        
        # Batch insert
        batch_size = 1000
        for i in range(0, len(rows), batch_size):
            batch = rows[i:i + batch_size]
            try:
                session.execute(query, batch)
                session.commit()
                print(f"  → Inserted {min(i + batch_size, len(rows))}/{len(rows)}")
            except Exception as e:
                session.rollback()
                print(f"  ❌ Error inserting into {table_name}: {e}")
                break
        
        print(f"  ✅ {table_name} complete\n")
    
    session.close()
    print("🎉 All data imported successfully!")

if __name__ == '__main__':
    main()
