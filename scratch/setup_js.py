import os

dirs = [
    'frontend/shared/js/core',
    'frontend/portal/static/js/core',
    'frontend/portal/static/js/modules',
    'frontend/portal/static/js/pages'
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

files = [
    'frontend/shared/js/core/api.js',
    'frontend/shared/js/core/auth.js',
    'frontend/shared/js/core/utils.js',
    'frontend/portal/static/js/modules/portfolio.js',
    'frontend/portal/static/js/modules/crm.js',
    'frontend/portal/static/js/modules/finance.js',
    'frontend/portal/static/js/pages/portal.js',
    'frontend/portal/static/js/pages/pipeline.js'
]

for f in files:
    if not os.path.exists(f):
        with open(f, 'w', encoding='utf-8') as file:
            file.write('// Auto-generated module stub\\n')

print("JS architecture created")
