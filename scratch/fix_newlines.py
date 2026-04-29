import os

blueprints = [
    'backend/core/sales/finance',
    'backend/core/sales/crm',
    'backend/core/properties/portfolio',
    'backend/core/neighborhood',
    'backend/core/identity/auth',
    'backend/addons/mobile',
    'backend/addons/legal',
    'backend/addons/ai'
]

for d in blueprints:
    routes_path = os.path.join(d, 'routes.py')
    if os.path.exists(routes_path):
        with open(routes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the literal \n with an actual newline
        content = content.replace("\\nfrom flask import", "\nfrom flask import")
        content = content.replace("\\nfrom", "\nfrom")
        content = content.replace("\\nimport", "\nimport")
        
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(content)

print('Newlines fixed')
