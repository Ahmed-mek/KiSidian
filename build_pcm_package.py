"""
Build KiCad PCM package for kisidian.

Creates: dist/kisidian-{version}-pcm.zip
"""
import os
import shutil
import zipfile
import json
from pathlib import Path

def build():
    # Read version from metadata
    with open("metadata.json") as f:
        meta = json.load(f)
    version = meta["versions"][0]["version"]
    
    print(f"Building KiSidian PCM Package v{version}")
    
    dist = Path("dist")
    dist.mkdir(exist_ok=True)
    
    zip_name = dist / f"KiSidian-{version}-pcm.zip"
    
    with zipfile.ZipFile(zip_name, 'w', zipfile.ZIP_DEFLATED) as zf:
        # Add plugins/ content
        src = Path("plugins")
        for f in src.rglob("*"):
            if f.is_file() and "__pycache__" not in str(f):
                # Use relative path from plugins/
                arcname = f"plugins/{f.relative_to(src)}"
                zf.write(f, arcname)
                print(f"  + {arcname}")
        
        # Add root metadata.json
        if os.path.exists("metadata.json"):
            zf.write("metadata.json", "metadata.json")
            print("  + metadata.json (root)")
        
        # Add root LICENSE if it exists
        if os.path.exists("LICENSE"):
            zf.write("LICENSE", "LICENSE")
            print("  + LICENSE (root)")
        
        # Add icon to resources/icon.png (PCM requirement)
        icon = Path("plugins/icon.png")
        if icon.exists():
            zf.write(icon, "resources/icon.png")
            print("  + resources/icon.png")
    
    print(f"\n✅ Created: {zip_name}")
    if zip_name.exists():
        print(f"   Size: {zip_name.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    build()
