import sqlite3
from shared.database import DB_NAME

def insert_samples():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Contracts
    cur.execute("DELETE FROM contracts")
    contracts = [
        ('IMZ-334', 2, '2024-01-01', '2025-01-01', 'Kira'),
        ('IMZ-1234', 3, '2023-06-15', '2028-06-15', 'Satış/Yönetim')
    ]
    cur.executemany("INSERT INTO contracts (property_id, user_id, start_date, end_date, type) VALUES (?, ?, ?, ?, ?)", contracts)

    # Taxes
    cur.execute("DELETE FROM taxes")
    taxes = [
        ('bogaz-villa', 2024, 4500.0, '2024-05-31'),
        ('bogaz-villa', 2024, 4500.0, '2024-11-30'),
        ('cam-oda-penthouse', 2024, 2500.0, '2024-03-05')
    ]
    cur.executemany("INSERT INTO taxes (property_id, year, amount, due_date) VALUES (?, ?, ?, ?)", taxes)

    # Maintenance
    cur.execute("DELETE FROM maintenance")
    maint = [
        ('bogaz-villa', 'Kombi su sızdırıyor, acil kontrol gerekiyor.', '2024-02-15', 'completed'),
        ('cam-oda-penthouse', 'Havuz motoru periyodik bakımı yapıldı.', '2024-01-10', 'completed'),
        ('ekolojik-ev', 'Güneş paneli temizliği', '2024-04-01', 'planned')
    ]
    cur.executemany("INSERT INTO maintenance (property_id, description, scheduled_date, status) VALUES (?, ?, ?, ?)", maint)

    # Appointments
    cur.execute("DELETE FROM appointments")
    apps = [
        (2, 'bogaz-villa', '2024-03-10 14:00', 'Gösterim', 'confirmed'),
        (3, 'cam-oda-penthouse', '2024-03-12 10:30', 'Sözleşme Görüşmesi', 'pending')
    ]
    cur.executemany("INSERT INTO appointments (user_id, property_id, datetime, purpose, status) VALUES (?, ?, ?, ?, ?)", apps)

    conn.commit()
    conn.close()
    print("Sample data populated for modules")

if __name__ == '__main__':
    insert_samples()
