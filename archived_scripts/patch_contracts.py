import re

with open('api/contracts.py', 'r', encoding='utf-8') as f:
    content = f.read()

# We need to remove from "# Parties endpoints" down to "# Contract builder endpoints for wizard"
start_str = "# Parties endpoints"
end_str = "# Contract builder endpoints for wizard"

start_idx = content.find(start_str)
end_idx = content.find(end_str)

if start_idx != -1 and end_idx != -1:
    new_content = content[:start_idx] + content[end_idx:]
    with open('api/contracts.py', 'w', encoding='utf-8') as f:
        f.write(new_content)
    print("Redundant parties endpoints removed from api/contracts.py.")
else:
    print("Could not find blocks to remove.")
