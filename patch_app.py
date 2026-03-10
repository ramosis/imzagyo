import sys

with open('app.py', 'r', encoding='utf-8') as f:
    content = f.read()

s1 = 'app.register_blueprint(contract_templates_bp)'
s2 = 'app.register_blueprint(contract_templates_bp)\napp.register_blueprint(parties_bp)'

if s1 in content:
    content = content.replace(s1, s2)
    with open('app.py', 'w', encoding='utf-8') as f:
        f.write(content)
    print("Patched app.py successfully")
else:
    print("Could not find string in app.py")
