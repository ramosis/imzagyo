"""
Fix portal.html by moving PMS module JS (contracts, taxes, maintenance, appointments)
from outside the main script block INTO the main script block (before its closing </script>).
This ensures API_BASE and currentWizStep are in scope.
"""

with open('inject_modules_js.py', 'r', encoding='utf-8') as f:
    injector_text = f.read()

import re

m_js = re.search(r'new_js = """(.*?)"""', injector_text, re.DOTALL)
m_logic = re.search(r'new_show_logic = """(.*?)"""', injector_text, re.DOTALL)

if not m_js or not m_logic:
    print("ERROR: Could not parse inject_modules_js.py")
    exit(1)

payload = m_js.group(1) + m_logic.group(1)

with open('portal.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Check if payload is still appended after inspection-data.js (outside main block)
if payload in html:
    # Remove all occurrences from the inspection-data block (outside main JS)
    # The payload currently is after </script> line 1906, inside a different script block
    # Remove it from last </script>
    html = html.replace(payload + '\n</script>', '</script>')
    print("Removed injected payload from inspection block")
else:
    print("WARNING: payload not found in html, may already be cleaned up")

# Now find the MAIN script block's closing tag
# The main script opens around line 1012 and closes around line 1906
# We need to inject the payload INSIDE the main script block, before its first </script>
# Strategy: find the </script> that comes AFTER 'let currentWizStep = 1' 

wiz_idx = html.find('let currentWizStep = 1;')
if wiz_idx == -1:
    print("ERROR: Cannot find 'let currentWizStep = 1'")
    exit(1)

# Find the next </script> after currentWizStep
close_script_idx = html.find('</script>', wiz_idx)
if close_script_idx == -1:
    print("ERROR: Cannot find </script> after wizard step")
    exit(1)

# Inject payload before this </script>
html = html[:close_script_idx] + payload + '\n' + html[close_script_idx:]
print(f"Injected payload into main script block at position {close_script_idx}")

with open('portal.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("Done! portal.html fixed.")
