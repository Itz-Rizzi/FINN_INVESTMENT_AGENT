import os
import sys
import re

if sys.stdout.encoding.lower() != 'utf-8':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
        sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        pass

root_dir = r"C:\Users\yenni\.gemini\antigravity\scratch\finn"
secret_patterns = [
    ("Google API Key", re.compile(r"AIza[0-9A-Za-z-_]{35}")),
    ("Generic Secret", re.compile(r"""(?:api[_-]?key|secret|password)\s*[:=]\s*["']([^"'\s]{8,})["']""", re.I))
]

print("==========================================")
print("SECTION 7: DEPLOYMENT READINESS & SECRETS SCAN")
print("==========================================")

found_secrets = []
for dirpath, dirnames, filenames in os.walk(root_dir):
    if any(skip in dirpath for skip in ["node_modules", ".next", ".git", "chrome-temp", "__pycache__"]):
        continue
    for fname in filenames:
        if fname.endswith((".png", ".pdf", ".db", ".index", ".ico", ".svg", ".lock")):
            continue
        fpath = os.path.join(dirpath, fname)
        rel_path = os.path.relpath(fpath, root_dir)
        try:
            with open(fpath, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read()
                for label, p in secret_patterns:
                    matches = p.findall(content)
                    for m in matches:
                        m_str = str(m)
                        if any(safe in m_str.lower() for safe in ["your_", "placeholder", "example", "gemini_api_key", "default_"]):
                            continue
                        found_secrets.append((rel_path, label, m_str))
        except Exception:
            pass

print(f"Total Hardcoded Secrets Detected: {len(found_secrets)}")
if found_secrets:
    for path, label, val in found_secrets:
        print(f"  [ALERT] {label} in {path}: {val[:6]}...")
else:
    print("  ✓ ZERO hardcoded API keys, passwords, or secrets found across repository.")

# Review .env.example files
print("\n=== ENVIRONMENT VARIABLES AUDIT ===")
backend_env_ex = os.path.join(root_dir, "backend", ".env.example")
frontend_env_ex = os.path.join(root_dir, "frontend", ".env.example")

print(f"Backend .env.example ({os.path.exists(backend_env_ex)}):")
if os.path.exists(backend_env_ex):
    with open(backend_env_ex, "r", encoding="utf-8") as f:
        print(f.read().strip())

print(f"\nFrontend .env.example ({os.path.exists(frontend_env_ex)}):")
if os.path.exists(frontend_env_ex):
    with open(frontend_env_ex, "r", encoding="utf-8") as f:
        print(f.read().strip())

# Check root and frontend .gitignore
print("\n=== .gitignore AUDIT ===")
for gipath in [os.path.join(root_dir, ".gitignore"), os.path.join(root_dir, "backend", ".gitignore"), os.path.join(root_dir, "frontend", ".gitignore")]:
    if os.path.exists(gipath):
        print(f"File: {os.path.relpath(gipath, root_dir)}")
        with open(gipath, "r", encoding="utf-8") as f:
            lines = [l.strip() for l in f.readlines() if l.strip() and not l.startswith("#")]
            env_rules = [l for l in lines if ".env" in l or "node_modules" in l or "*.db" in l]
            print(f"  Protected patterns: {env_rules}")
    else:
        print(f"File MISSING: {os.path.relpath(gipath, root_dir)}")

print("\nSECTION 7 AUDIT COMPLETED.")
