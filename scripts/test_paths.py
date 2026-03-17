import os

def test_paths():
    files_to_check = [
        'pages/anasayfa.html',
        'pages/portal.html',
        'app.py',
        'api/auth.py'
    ]
    
    print(f"Current Working Directory: {os.getcwd()}")
    for f in files_to_check:
        exists = os.path.exists(f)
        print(f"File: {f} - Exists: {exists}")
        if exists:
            print(f"  Absolute path: {os.path.abspath(f)}")

if __name__ == "__main__":
    test_paths()
