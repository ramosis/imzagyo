import json
import re

with open('detay.md', 'r', encoding='utf-8') as f:
    lines = f.readlines()

data = {
    "Grup_1": {"title": "Konut", "categories": []},
    "Grup_2": {"title": "Ticari/Endüstriyel", "categories": []},
    "Grup_3": {"title": "Arsa/Arazi", "categories": []}
}

current_group = None
current_category = None

for line in lines:
    line = line.strip()
    if not line:
        continue
    
    if "(Grup 1)" in line:
        current_group = "Grup_1"
    elif "(Grup 2)" in line:
        current_group = "Grup_2"
    elif "(Grup 3)" in line:
        current_group = "Grup_3"
    
    # Category matches "1. HUKUKİ VE İDARİ KONTROLLER"
    if re.match(r"^\d+\.\s+[A-ZÇĞİÖŞÜ ]+", line):
        current_category = {
            "name": line,
            "questions": []
        }
        if current_group:
            data[current_group]["categories"].append(current_category)
    
    # Question matches "[ ] Soru metni [1-2-3-0]"
    elif line.startswith("[ ]") and "[1-2-3-0]" in line:
        # Extract text between "[ ]" and "[1-2-3-0]"
        q_text = line.replace("[ ]", "").replace("[1-2-3-0]", "").strip()
        if current_category:
            current_category["questions"].append(q_text)

js_content = f"const inspectionData = {json.dumps(data, ensure_ascii=False, indent=4)};"

with open('js/inspection-data.js', 'w', encoding='utf-8') as f:
    f.write(js_content)

print("inspection-data.js generated successfully!")
