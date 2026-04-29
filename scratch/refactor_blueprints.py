import os
import re

blueprints = {
    'backend/core/sales/finance': ('finance_bp', 'finance'),
    'backend/core/sales/crm': ('crm_bp', 'crm'),
    'backend/core/properties/portfolio': ('portfolio_bp', 'portfolio'),
    'backend/core/neighborhood': ('neighborhood_bp', 'neighborhood'),
    'backend/core/identity/auth': ('auth_bp', 'auth'),
    'backend/addons/mobile': ('mobile_bp', 'mobile_api'),
    'backend/addons/legal': ('legal_bp', 'legal'),
    'backend/addons/ai': ('ai_bp', 'ai')
}

for d, (bp_name, bp_str) in blueprints.items():
    if not os.path.exists(d):
        continue
        
    init_path = os.path.join(d, '__init__.py')
    with open(init_path, 'w', encoding='utf-8') as f:
        f.write(f'''from flask import Blueprint

{bp_name} = Blueprint(
    \\'{bp_str}\\',
    __name__,
    template_folder=\\'templates\\',
    static_folder=\\'static\\',
    static_url_path=\\'/static/{bp_str}\\'
)

from . import routes
''')

    routes_path = os.path.join(d, 'routes.py')
    if os.path.exists(routes_path):
        with open(routes_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove Blueprint creation
        content = re.sub(rf'{bp_name}\\s*=\\s*Blueprint\\([^)]+\\)\\n?', '', content)
        
        # Add import
        if 'from flask import' in content:
            content = content.replace('from flask import', f'from . import {bp_name}\\nfrom flask import', 1)
        else:
            content = f'from . import {bp_name}\\n' + content
            
        with open(routes_path, 'w', encoding='utf-8') as f:
            f.write(content)

print('Blueprints updated successfully')
