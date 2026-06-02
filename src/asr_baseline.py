from pathlib import Path
import json
import shutil


def safe_json_write(obj, path):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False), encoding="utf-8")
    return path


def safe_copy(src, dst):
    src = Path(src)
    dst = Path(dst)
    if not src.exists():
        return None
    dst.parent.mkdir(parents=True, exist_ok=True)
    try:
        if src.resolve() == dst.resolve():
            return str(dst)
    except Exception:
        pass
    return shutil.copy2(src, dst)


def make_zip(src_dir, zip_base):
    return shutil.make_archive(str(zip_base), "zip", str(src_dir))
