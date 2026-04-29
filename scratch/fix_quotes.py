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
    init_path = os.path.join(d, '__init__.py')
    if os.path.exists(init_path):
        with open(init_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Replace the backslash-quote with just quote
        content = content.replace("\\'", "'")
        
        with open(init_path, 'w', encoding='utf-8') as f:
            f.write(content)

print('Syntax errors fixed')
