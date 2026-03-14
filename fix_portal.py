
import sys

with open('portal.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

# Line numbers are 1-indexed. We want to delete 2683 to 6057.
# Python indexes are 0-indexed. 
# Keep lines 0 to 2681 (which are 1 to 2682)
# Keep lines 6057 onwards (which are 6058 onwards)

new_lines = lines[0:2682] + lines[6057:]

with open('portal.html', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)

print(f"Removed {6057 - 2682} lines. New total: {len(new_lines)}")