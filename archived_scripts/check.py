import sys
import traceback

def main():
    try:
        import app
        print("Success!")
    except Exception as e:
        with open("full_traceback.txt", "w", encoding="utf-8") as f:
            traceback.print_exc(file=f)
        print("Error written to full_traceback.txt")

if __name__ == '__main__':
    main()
