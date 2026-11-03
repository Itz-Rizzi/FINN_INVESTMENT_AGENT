import os

root_dir = r"C:\Users\yenni\.gemini\antigravity\scratch\finn"

items = [
    ("Root README.md", os.path.join(root_dir, "README.md")),
    ("Root .gitignore", os.path.join(root_dir, ".gitignore")),
    ("Backend requirements.txt", os.path.join(root_dir, "backend", "requirements.txt")),
    ("Backend .env.example", os.path.join(root_dir, "backend", ".env.example")),
    ("Backend main.py", os.path.join(root_dir, "backend", "app", "main.py")),
    ("Backend Database Schema (schema.sql)", os.path.join(root_dir, "backend", "app", "db", "schema.sql")),
    ("Backend SQLite Database (finn.db)", os.path.join(root_dir, "backend", "app", "data", "finn.db")),
    ("Backend Test Suite", os.path.join(root_dir, "backend", "tests")),
    ("Frontend package.json", os.path.join(root_dir, "frontend", "package.json")),
    ("Frontend .env.example", os.path.join(root_dir, "frontend", ".env.example")),
    ("Frontend page.tsx", os.path.join(root_dir, "frontend", "src", "app", "page.tsx")),
    ("Frontend layout.tsx", os.path.join(root_dir, "frontend", "src", "app", "layout.tsx")),
    ("Frontend components", os.path.join(root_dir, "frontend", "src", "components")),
]

print("==========================================")
print("SECTION 8: SUBMISSION CHECKLIST AUDIT")
print("==========================================")

all_exist = True
for label, p in items:
    exists = os.path.exists(p)
    if exists:
        size = os.path.getsize(p) if os.path.isfile(p) else len(os.listdir(p))
        unit = "bytes" if os.path.isfile(p) else "items"
        print(f"  [OK] {label:<38} -> Exists ({size} {unit})")
    else:
        print(f"  [FAIL] {label:<38} -> MISSING!")
        all_exist = False

print("="*60)
print(f"SUBMISSION CHECKLIST STATUS: {'100% COMPLETE' if all_exist else 'INCOMPLETE'}")
print("="*60)
