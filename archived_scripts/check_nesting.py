lines = open('portal.html', 'r', encoding='utf-8').readlines()
indent = 0
for i in range(458, min(1700, len(lines))):
    line = lines[i].strip()
    opens = line.count('<div') + line.count('<section')
    closes = line.count('</div>') + line.count('</section>')
    if opens > 0 or closes > 0:
        if closes > opens:
            indent -= (closes - opens)
        print(f"L{i+1}: {'  '*max(0,indent)} [{'+' if opens > closes else '-' if closes > opens else '='}{abs(opens-closes) if opens != closes else opens}] {line[:120]}")
        if opens > closes:
            indent += (opens - closes)
