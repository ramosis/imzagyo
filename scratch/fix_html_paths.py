import os

frontend_dir = 'frontend'

for root, _, files in os.walk(frontend_dir):
    for f in files:
        if f.endswith('.html'):
            filepath = os.path.join(root, f)
            with open(filepath, 'r', encoding='utf-8') as file:
                content = file.read()
                
            original_content = content
            content = content.replace('href="../static/', 'href="/static/')
            content = content.replace('src="../static/', 'src="/static/')
            content = content.replace("href='../static/", "href='/static/")
            content = content.replace("src='../static/", "src='/static/")
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as file:
                    file.write(content)
                print(f"Updated paths in {filepath}")

print("Path updates complete")
