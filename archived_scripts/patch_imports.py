import re
import os

files_to_fix = [
    os.path.join('api', 'leads.py'),
    os.path.join('api', 'expenses.py'),
    os.path.join('api', 'integrations.py'),
    os.path.join('api', 'hero.py')
]

for file_path in files_to_fix:
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Remove the global import
        content = content.replace("from api.auth import get_current_user\n", "")
        content = content.replace("from api.auth import get_current_user, require_inner_circle\n", "")
        
        # We will inject the import inside the functions that use get_current_user()
        # This is the safest way to break circular imports in Flask blueprints.
        content = re.sub(r'(def [a-zA-Z_]+\(.*\):)\n\s+user = get_current_user\(\)', r'\1\n    from api.auth import get_current_user\n    user = get_current_user()', content)
        
        # Write back
        with open(file_path, 'w', encoding='utf-8') as f:
            f.write(content)
        
print("Circular import patches applied.")
