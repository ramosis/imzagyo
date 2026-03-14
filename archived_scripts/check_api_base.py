import sys
import re

with open('portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Fix fetch calls for appointments and contracts to include /api/
# In portal.html, API_BASE is probably '/api' but let's check
import re

api_base_match = re.search(r'const API_BASE\s*=\s*[\'"]([^\'"]*)[\'"]', content)
if api_base_match:
    print(f"API_BASE is set to: {api_base_match.group(1)}")
    # If API_BASE is '/api', then fetch(`${API_BASE}/contracts`) would be '/api/contracts', which is correct.
    # Why is it failing then? Let's check the terminal output for errors.
else:
    print("Could not find API_BASE")

# Wait, maybe the problem is the API URL itself. Let's make sure the JS calls /api/contracts correctly.

content = content.replace('`${API_BASE}/contracts`', '`${API_BASE}/contracts`')
content = content.replace('`${API_BASE}/appointments`', '`${API_BASE}/appointments`')

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(content)
