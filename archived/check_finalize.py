import sys

with open('portal.html', 'r', encoding='utf-8') as f:
    content = f.read()

# Let's inspect finalizeContract
import re

finalize_str = re.search(r'async function finalizeContract\(\) \{.*?(?=async function|function|\Z)', content, re.DOTALL)
if finalize_str:
    print(finalize_str.group(0))
else:
    print("Could not find finalizeContract")
