"""Data Governance course - setup self-test.

Run from the shopfast-kit folder, with your virtual environment activated:
    python check_setup.py

It prints one line per check and ends with READY (green) or NOT READY (red).
Take a screenshot of the final message and bring it to the CM 2 lab on 24 Nov.
"""
import importlib, os, platform, shutil, subprocess, sys, urllib.request

GREEN, RED, YELLOW, RESET = "\033[92m", "\033[91m", "\033[93m", "\033[0m"
if platform.system() == "Windows":
    os.system("")  # enables colours in the Windows terminal

results = []

def check(name, ok, hint="", optional=False):
    tag = f"{GREEN}OK  {RESET}" if ok else (f"{YELLOW}WARN{RESET}" if optional else f"{RED}FAIL{RESET}")
    print(f"[{tag}] {name}" + ("" if ok else f"\n        -> {hint}"))
    if not optional:
        results.append(ok)

print("\n=== Data Governance course - setup check ===\n")
print(f"System: {platform.system()} {platform.release()} | Python {platform.python_version()}\n")

# 1. Python version
v = sys.version_info
check("Python 3.11 or 3.12", (v.major, v.minor) in [(3, 11), (3, 12)],
      "Install Python 3.12 from python.org and recreate your virtual environment (see checklist step 2).")

# 2. RAM / disk (information)
try:
    import psutil
    ram = psutil.virtual_memory().total / 1024**3
    check(f"RAM: {ram:.1f} GB (8 GB is enough)", ram >= 7.0, "Less than 8 GB: close other apps during the labs.", optional=True)
except ImportError:
    check("psutil installed", False, "pip install -r requirements.txt")
free = shutil.disk_usage(".").free / 1024**3
check(f"Free disk: {free:.1f} GB (need 10 GB)", free >= 10, "Free some disk space (Docker images + Python packages need ~10 GB).", optional=True)

# 3. Python packages
for mod, label in [("pandas", "pandas"), ("duckdb", "DuckDB"), ("great_expectations", "Great Expectations"),
                   ("presidio_analyzer", "Presidio analyzer"), ("presidio_anonymizer", "Presidio anonymizer"),
                   ("psycopg2", "psycopg2 (Postgres driver)")]:
    try:
        importlib.import_module(mod)
        check(f"Python package: {label}", True)
    except Exception as e:
        check(f"Python package: {label}", False, f"pip install -r requirements.txt   ({type(e).__name__}: {e})")

# 4. spaCy language model for Presidio
try:
    import spacy
    spacy.load("en_core_web_sm")
    check("spaCy model en_core_web_sm", True)
except Exception:
    check("spaCy model en_core_web_sm", False, "python -m spacy download en_core_web_sm")

# 5. Command-line tools
def cmd_ok(cmd):
    try:
        out = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        return out.returncode == 0, (out.stdout or out.stderr).strip().splitlines()[:1]
    except Exception as e:
        return False, [str(e)]

ok, _ = cmd_ok(["dbt", "--version"]); check("dbt CLI (dbt --version)", ok, "Activate your venv, then pip install -r requirements.txt")
ok, _ = cmd_ok(["datacontract", "--version"]); check("datacontract CLI", ok, "Activate your venv, then pip install -r requirements.txt")
ok, _ = cmd_ok(["git", "--version"]); check("Git", ok, "Install Git from git-scm.com")
ok, _ = cmd_ok(["docker", "info"]); check("Docker is running", ok, "Start Docker Desktop (Windows/macOS) or the docker service (Linux).")

# 6. ShopFast database
try:
    import psycopg2
    con = psycopg2.connect(host="localhost", port=int(os.environ.get("SHOPFAST_PG_PORT", "5432")), dbname="shopfast", user="shopfast_admin",
                           password="shopfast_admin", connect_timeout=5)
    cur = con.cursor(); cur.execute("select count(*) from raw.customers"); n = cur.fetchone()[0]; con.close()
    check(f"ShopFast database loaded ({n} customers)", n == 1241, "Run: docker compose down -v  then  docker compose up -d")
except Exception as e:
    check("ShopFast database reachable on localhost:5432", False,
          f"In the shopfast-kit folder run: docker compose up -d   (error: {str(e).splitlines()[0][:90]})")

# 7. OpenRefine (optional - must be started by hand)
try:
    urllib.request.urlopen("http://127.0.0.1:3333", timeout=3)
    check("OpenRefine is running on http://127.0.0.1:3333", True)
except Exception:
    check("OpenRefine running (start it, then re-run this check)", False,
          "Start OpenRefine (see checklist step 5). It should open http://127.0.0.1:3333 in your browser.", optional=True)

print()
if all(results):
    print(f"{GREEN}==============================\n   READY for the 24 Nov lab  :-)\n=============================={RESET}")
else:
    print(f"{RED}==============================\n   NOT READY - fix the FAIL lines above\n=============================={RESET}")
