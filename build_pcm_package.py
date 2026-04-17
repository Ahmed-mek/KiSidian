"""
Build KiCad PCM package for kisidian.
Creates: dist/KiSidian-{version}-pcm.zip
"""
import os
import zipfile
import json
import hashlib
from pathlib import Path

def get_sha256(filename):
    sha256_hash = hashlib.sha256()
    with open(filename, "rb") as f:
        for byte_block in iter(lambda: f.read(4096), b""):
            sha256_hash.update(byte_block)
    return sha256_hash.hexdigest()

def clean_metadata(input_file):
    with open(input_file, 'r') as f:
        data = json.load(f)
    
    # Remove download-related fields for the internal metadata.json
    for version in data.get("versions", []):
        version.pop("download_url", None)
        version.pop("download_sha256", None)
        version.pop("download_size", None)
        version.pop("install_size", None)
    
    return json.dumps(data, indent=4)

def build():
    # Read version from metadata
    if not os.path.exists("metadata.json"):
        print("Error: metadata.json not found!")
        return
        
    with open("metadata.json") as f:
        meta = json.load(f)
    version = meta["versions"][0]["version"]
    
    print(f"Building KiSidian PCM Package v{version}")
    
    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    
    zip_path = dist / f"KiSidian-{version}-pcm.zip"
    
    with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zf:
        # 1. Add plugins/ content
        src = Path("plugins")
        if src.exists():
            for f in src.rglob("*"):
                if f.is_file() and "__pycache__" not in str(f):
                    arcname = f"plugins/{f.relative_to(src)}"
                    zf.write(f, arcname)
                    print(f"  + {arcname}")
        
        # 2. Add resources (icon and screenshots)
        icon = Path("plugins/icon.png")
        if icon.exists():
            zf.write(icon, "resources/icon.png")
            print("  + resources/icon.png")
        
        screenshots_dir = Path("screenshots")
        if screenshots_dir.exists():
            for f in screenshots_dir.glob("*.png"):
                arcname = f"resources/screenshots/{f.name}"
                zf.write(f, arcname)
                print(f"  + {arcname}")

        # 3. Add root LICENSE
        if os.path.exists("LICENSE"):
            zf.write("LICENSE", "LICENSE")
            print("  + LICENSE (root)")
            
        # 4. Add CLEAN metadata.json to root
        clean_meta_content = clean_metadata("metadata.json")
        zf.writestr("metadata.json", clean_meta_content)
        print("  + metadata.json (cleaned root)")
    
    print(f"\n✅ Created: {zip_path}")
    if zip_path.exists():
        size = zip_path.stat().st_size
        sha256 = get_sha256(zip_path)
        print(f"   Size: {size / 1024:.1f} KB")
        print(f"   SHA256: {sha256}")
        print("\n--- Use these values for your repository submission ---")
        print(f"\"download_sha256\": \"{sha256}\",")
        print(f"\"download_size\": {size},")
        print(f"\"install_size\": {size}  # (Approximate, usually larger after extract)")

if __name__ == "__main__":
    build()
