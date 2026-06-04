import os, sys, platform, subprocess, importlib.util, time
from datetime import datetime, timedelta, timezone


BASE_PACKAGES = [
    ("requests", "requests"),
    ("rich", "rich"),
    ("httpx", "httpx"),
    ("python-cfonts", "python_cfonts"),
]

FLASK_PACKAGES = BASE_PACKAGES + [
    ("flask", "flask"),
]

FASTAPI_PACKAGES = BASE_PACKAGES + [
    ("fastapi", "fastapi"),
    ("uvicorn", "uvicorn"),
]


def _ensure_packages():
    packages = FLASK_PACKAGES if (is_termux or is_pydroid) else FASTAPI_PACKAGES
    missing = []
    for pip_name, import_name in packages:
        if importlib.util.find_spec(import_name) is None:
            missing.append(pip_name)
    if not missing:
        return
    print(f"[setup] installing: {', '.join(missing)}")
    cmd = [sys.executable, "-m", "pip", "install", *missing]
    subprocess.check_call(cmd)


ver = f"{sys.version_info.major}.{sys.version_info.minor}"
base_dir = os.path.dirname(os.path.abspath(__file__))
files_dir = os.path.join(base_dir, "files")
lastupdate_file = os.path.join(files_dir, "lastupdate.txt")

is_termux = "com.termux" in os.environ.get("PREFIX", "")
is_pydroid = os.environ.get("PYDROID_PYTHON") is not None or "pydroid" in os.environ.get("HOME", "").lower()

if is_termux or is_pydroid:
    remote_base = "https://raw.githubusercontent.com/stein-exe/instagram-mass-reporter/main/flask"
    local_name = f"{ver}_android.py"
else:
    remote_base = "https://raw.githubusercontent.com/stein-exe/instagram-mass-reporter/main/fastapi"
    local_name = f"{ver}_fastapi.py"

local_file = os.path.join(files_dir, local_name)
remote_url = f"{remote_base}/{ver}.py"

os.makedirs(files_dir, exist_ok=True)


def _is_usable_cache(path):
    if not os.path.isfile(path):
        return False
    try:
        return os.path.getsize(path) > 0
    except OSError:
        return False


def _read_cache_age():
    if not _is_usable_cache(lastupdate_file):
        return None
    try:
        with open(lastupdate_file, encoding="utf-8") as f:
            raw = f.read().strip()
        saved = datetime.fromisoformat(raw)
    except (OSError, ValueError):
        return None
    if saved.tzinfo is None:
        saved = saved.replace(tzinfo=timezone.utc)
    return datetime.now(timezone.utc).astimezone() - saved


need_download = True
if _is_usable_cache(local_file):
    age = _read_cache_age()
    if age is not None and age < timedelta(hours=12):
        need_download = False

if need_download:
    _ensure_packages()
    import requests
    print("wait 10 seconds til file loads......")
    resp = requests.get(remote_url, timeout=30)
    resp.raise_for_status()
    payload = resp.text
    if not payload.strip():
        raise RuntimeError(f"empty payload from {remote_url}")
    tmp_file = f"{local_file}.tmp"
    with open(tmp_file, "w", encoding="utf-8") as f:
        f.write(payload)
    os.replace(tmp_file, local_file)
    with open(lastupdate_file, "w", encoding="utf-8") as f:
        f.write(datetime.now(timezone.utc).astimezone().isoformat())

with open(local_file, encoding="utf-8") as f:
    code = f.read()

exec(code, {"__name__": "__main__", "__file__": local_file})
