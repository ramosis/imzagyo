import sqlite3
import os

DB_NAME = "imza_database.db"

def populate_templates():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Templates
    templates = [
        ("Konut Kira Sözleşmesi", "Standart konut kiralama işlemleri için."),
        ("Konut Satış Sözleşmesi", "Konut satış ve devir işlemleri için."),
        ("Düzenleme Şeklinde Taşınmaz Satış Vaadi", "Noter onaylı satış vaadi işlemleri için ön hazırlık."),
        ("Ticari Kira Sözleşmesi", "Ofis, dükkan ve depo kiralama işlemleri için.")
    ]

    for name, desc in templates:
        cur.execute('INSERT OR IGNORE INTO contract_templates (name, description) VALUES (?, ?)', (name, desc))
    
    conn.commit()

    # Get template IDs
    cur.execute('SELECT id, name FROM contract_templates')
    template_map = {name: id for id, name in cur.fetchall()}

    # Clauses
    clauses = [
        # Kira Sözleşmesi Maddeleri
        (template_map["Konut Kira Sözleşmesi"], "Kiralanan taşınmaz sadece konut amacıyla kullanılabilir.", True, 1),
        (template_map["Konut Kira Sözleşmesi"], "Kira bedeli her ayın en geç 5. günü banka hesabına ödenir.", True, 2),
        (template_map["Konut Kira Sözleşmesi"], "Depozito bedeli 2 aylık kira tutarı olarak kararlaştırılmıştır.", False, 3),
        (template_map["Konut Kira Sözleşmesi"], "Evcil hayvan beslenmesi ev sahibinin yazılı onayına tabidir.", False, 4),
        (template_map["Konut Kira Sözleşmesi"], "Boyave badana işlemleri tahliye sırasında eksiksiz teslim edilir.", False, 5),

        # Satış Sözleşmesi Maddeleri
        (template_map["Konut Satış Sözleşmesi"], "Satış bedeli tapu devri sırasında nakden veya hesaben ödenir.", True, 1),
        (template_map["Konut Satış Sözleşmesi"], "Tüm emlak vergisi ve masraflar alıcı tarafından karşılanır.", False, 2),
        (template_map["Konut Satış Sözleşmesi"], "Gayrimenkul üzerindeki tüm takyidatların temizlenmesi satıcıya aittir.", True, 3),

        # Satış Vaadi Maddeleri
        (template_map["Düzenleme Şeklinde Taşınmaz Satış Vaadi"], "Taraflar en geç 6 ay içinde kesin satışı gerçekleştirmeyi taahhüt eder.", True, 1),
        (template_map["Düzenleme Şeklinde Taşınmaz Satış Vaadi"], "Cayma tazminatı olarak satış bedelinin %10'u kararlaştırılmıştır.", True, 2)
    ]

    for tid, text, mandatory, order in clauses:
        cur.execute('''
            INSERT OR IGNORE INTO contract_clauses (template_id, clause_text, is_mandatory, sort_order)
            VALUES (?, ?, ?, ?)
        ''', (tid, text, mandatory, order))

    conn.commit()
    conn.close()
    print("Sözleşme şablonları ve maddeleri başarıyla eklendi.")

if __name__ == "__main__":
    populate_templates()
