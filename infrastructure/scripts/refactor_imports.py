import os

def fix_imports(directory):
    for root, dirs, files in os.walk(directory):
        if ".git" in root or "__pycache__" in root or ".gemini" in root:
            continue
        for file in files:
            if file.endswith(".py"):
                path = os.path.join(root, file)
                try:
                    with open(path, "r", encoding="utf-8") as f:
                        content = f.read()
                    
                    # Core replacements
                    new_content = content.replace("from shared.extensions import", "from shared.extensions import")
                    new_content = new_content.replace("from shared.database import", "from shared.database import")
                    new_content = new_content.replace("from shared.models import", "from shared.models import")
                    
                    # Decorator replacements
                    new_content = new_content.replace("from modules.auth.decorators import login_required, circle_required", "from modules.auth.decorators import login_required, circle_required")
                    new_content = new_content.replace("from modules.auth.decorators import require_permission", "from modules.auth.decorators import require_permission")
                    new_content = new_content.replace("from modules.auth.decorators import login_required", "from modules.auth.decorators import login_required")
                    new_content = new_content.replace("from modules.auth.decorators import circle_required", "from modules.auth.decorators import circle_required")
                    
                    if new_content != content:
                        with open(path, "w", encoding="utf-8") as f:
                            f.write(new_content)
                        print(f"Fixed: {path}")
                except Exception as e:
                    print(f"Error processing {path}: {e}")

if __name__ == "__main__":
    # Scan root and subdirectories
    fix_imports(".")
