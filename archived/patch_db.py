import sys

with open('database.py', 'r', encoding='utf-8') as f:
    content = f.read()

old_contracts = """    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            start_date TEXT,
            end_date TEXT,
            type TEXT,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(user_id) REFERENCES users(id)
        )
    ''')"""

new_contracts = """    cursor.execute('''
        CREATE TABLE IF NOT EXISTS contracts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            property_id TEXT NOT NULL,
            user_id INTEGER NOT NULL,
            seller_id INTEGER,
            buyer_id INTEGER,
            contract_type TEXT,
            special_conditions TEXT,
            status TEXT DEFAULT 'draft',
            start_date TEXT,
            end_date TEXT,
            type TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY(property_id) REFERENCES portfoyler(id),
            FOREIGN KEY(user_id) REFERENCES users(id),
            FOREIGN KEY(seller_id) REFERENCES parties(id),
            FOREIGN KEY(buyer_id) REFERENCES parties(id)
        )
    ''')"""

if old_contracts in content:
    content = content.replace(old_contracts, new_contracts)
    with open('database.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched database.py successfully")
else:
    print("Could not find the old contracts table schema in database.py")
