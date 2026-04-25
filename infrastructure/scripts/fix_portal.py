import re

with open('inject_modules_js.py', 'r', encoding='utf-8') as f:
    text = f.read()

m_js = re.search(r'new_js = \"\"\"(.*?)\"\"\"', text, re.DOTALL)
m_logic = re.search(r'new_show_logic = \"\"\"(.*?)\"\"\"', text, re.DOTALL)

if m_js and m_logic:
    payload = m_js.group(1) + m_logic.group(1)
    
    with open('portal.html', 'r', encoding='utf-8') as f:
        html = f.read()
        
    print('Found occurrences of payload:', html.count(payload))
    cleaned_html = html.replace(payload + '\n</script>', '</script>')
    
    print('After cleaning:', cleaned_html.count(payload))
    
    parts = cleaned_html.rsplit('</script>', 1)
    if len(parts) == 2:
        final_html = parts[0] + payload + '\n</script>' + parts[1]
        with open('portal.html', 'w', encoding='utf-8') as f:
            f.write(final_html)
        print('Fixed portal.html successfully!')
    else:
        print('Could not find </script>')
else:
    print('Could not extract payload.')
