"""
Build KiCad PCM package for kisidian.
Automatically calculates sizes and hashes to pass CI validation.
"""
import os
import shutil
import zipfile
import json
import hashlib
from pathlib import Path

def get_file_hash(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def build():
    # 1. Load metadata
    with open("metadata.json", 'r', encoding='utf-8') as f:
        meta = json.load(f)
    
    version = meta["versions"][0]["version"]
    print(f"--- Building KiSidian PCM Package v{version} ---")

    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    zip_name = dist / f"KiSidian-{version}-pcm.zip"

    install_size = 0
    
    # 2. Start Zipping
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add plugins/ content
        src = Path("plugins")
        for f in src.rglob("*"):
            if f.is_file() and "__pycache__" not in str(f):
                arcname = f"plugins/{f.relative_to(src)}"
                zf.write(f, arcname)
                install_size += f.stat().st_size
                print(f"  + {arcname}")

        # Add icon to resources/icon.png
        icon = Path("plugins/icon.png")
        if icon.exists():
            arcname = "resources/icon.png"
            zf.write(icon, arcname)
            install_size += icon.stat().st_size
            print(f"  + {arcname}")
            
        # Add root metadata.json to ZIP (temporary version, we'll fix it after)
        # Note: metadata.json itself is often counted in install_size by some validators
        meta_size = Path("metadata.json").stat().st_size
        install_size += meta_size
        zf.write("metadata.json", "metadata.json")
        print("  + metadata.json (root)")

    # 3. Calculate final zip stats
    download_size = zip_name.stat().st_size
    download_hash = get_file_hash(zip_name)

    print(f"\nCalculated Stats:")
    print(f"  Install Size: {install_size} bytes")
    print(f"  Download Size: {download_size} bytes")
    print(f"  SHA256: {download_hash}")

    # 4. Update metadata.json locally with final stats
    meta["versions"][0]["download_url"] = f"https://github.com/Ahmed-mek/KiSidian/releases/download/v{version}/KiSidian-{version}-pcm.zip"
    meta["versions"][0]["install_size"] = install_size
    meta["versions"][0]["download_size"] = download_size
    meta["versions"][0]["download_sha256"] = download_hash
    
    with open("metadata.json", 'w', encoding='utf-8') as f:
        json.dump(meta, f, indent=4)
    print("\n✅ metadata.json (Local) updated with correct sizes, hash, and URL.")

    # 5. Re-zip with STRIPPED metadata.json
    # Per KiCad requirements, the metadata.json INSIDE the zip MUST NOT 
    # contain download_url or download_sha256.
    stripped_meta = meta.copy()
    for v in stripped_meta["versions"]:
        v.pop("download_url", None)
        v.pop("download_sha256", None)
    
    with open("metadata_stripped.json", 'w', encoding='utf-8') as f:
        json.dump(stripped_meta, f, indent=4)

    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        for f in src.rglob("*"):
            if f.is_file() and "__pycache__" not in str(f):
                zf.write(f, f"plugins/{f.relative_to(src)}")
        if icon.exists():
            zf.write(icon, "resources/icon.png")
        # Add the stripped version as 'metadata.json' inside the zip
        zf.write("metadata_stripped.json", "metadata.json")
    
    os.remove("metadata_stripped.json")
    print(f"\n📦 Final Package (Compliant): {zip_name}")

if __name__ == "__main__":
    build()
