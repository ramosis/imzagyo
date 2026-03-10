import re

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Fix leads
html = html.replace("${l.score || '0'}", "${l.ai_score || '0'}")
html = html.replace("${l.property_interest || '-'}", "${l.property_title || '-'}")
html = html.replace('title="${l.property_interest}"', 'title="${l.property_title}"')

# Fix expenses
html = html.replace("${e.title}", "${e.description || '-'}")
html = html.replace("${e.expense_type}", "${e.category || '-'}")
html = html.replace("${e.created_at ? e.created_at.substring(0,10) : '-'}", "${e.date ? e.date.substring(0,10) : '-'}")

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)
print("Patch 2 successful.")
