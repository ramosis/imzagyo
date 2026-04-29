import os
import subprocess

moves = [
    # Investment
    ('frontend/pages/anasayfa.html', 'frontend/investment/pages/index.html'),
    ('frontend/pages/detay.html', 'frontend/investment/pages/property.html'),
    ('frontend/pages/arama.html', 'frontend/investment/pages/search.html'),
    ('frontend/pages/koleksiyon.html', 'frontend/investment/pages/collection.html'),
    ('frontend/pages/ekip.html', 'frontend/investment/pages/team.html'),
    ('frontend/pages/araclar.html', 'frontend/investment/pages/tools.html'),
    ('frontend/pages/ai_firsat_rotasi.html', 'frontend/investment/pages/ai-opportunity.html'),
    ('frontend/pages/kurumsal.html', 'frontend/investment/pages/corporate.html'),
    # Neighborhood
    ('frontend/pages/mahalle.html', 'frontend/neighborhood/pages/index.html'),
    ('frontend/pages/compass-dashboard.html', 'frontend/neighborhood/pages/dashboard.html'),
    # Portal
    ('frontend/pages/portal.html', 'frontend/portal/pages/index.html'),
    ('frontend/pages/pipeline.html', 'frontend/portal/pages/pipeline.html'),
    ('frontend/pages/admin-analytics.html', 'frontend/portal/pages/analytics.html')
]

for src, dst in moves:
    os.makedirs(os.path.dirname(dst), exist_ok=True)
    if os.path.exists(src):
        print(f"Moving {src} to {dst}")
        subprocess.run(['git', 'mv', src, dst])
    else:
        print(f"Skipped {src} - not found")

print("Moves completed")
