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
        # Add plugins/ content (files directly under plugins/, NOT plugins/kisidian/)
        # KiCad PCM extracts to: .../plugins/com_pcbtools_kisidian/
        # So our files go directly there, not in a kisidian/ subfolder
        src = Path("kisidian")
        for f in src.rglob("*"):
            if f.is_file() and "__pycache__" not in str(f):
                # Use relative path from kisidian/ directly under plugins/
                arcname = f"plugins/{f.relative_to(src)}"
                zf.write(f, arcname)
                print(f"  + {arcname}")
        
        # Add root metadata.json
        zf.write("metadata.json", "metadata.json")
        print("  + metadata.json (root)")
        
        # Add resources/icon.png (64x64 for PCM)
        icon = Path("resources/icons/icon.png")
        if icon.exists():
            zf.write(icon, "resources/icon.png")
            print("  + resources/icon.png")
    
    print(f"\n✅ Created: {zip_name}")
    print(f"   Size: {zip_name.stat().st_size / 1024:.1f} KB")

if __name__ == "__main__":
    build()
