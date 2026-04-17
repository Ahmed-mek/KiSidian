# KiSidian

**KiSidian** is a KiCad Action Plugin designed to bring a professional note-taking experience directly into your PCB design workflow. Inspired by Obsidian, it provides a powerful Markdown editor with a live preview side-by-side.

![KiSidian UI](plugins/icon.png)

## Features

-   **Split-Pane Editor**: Write Markdown on the left, see the rendered HTML on the right in real-time.
-   **Obsidian-Inspired Theme**: A beautiful, eye-friendly dark mode palette.
-   **Syntax Highlighting**: Real-time highlighting for headers, bold, italics, code blocks, and tags.
-   **Persistence**: Notes are automatically saved to a `notes.md` file in your KiCad project directory.
-   **Zero Dependencies**: Comes bundled with the `markdown` library for immediate use.
-   **Cross-Platform**: Supports Windows, macOS, and Linux (via KiCad PCM).

## 📦 Installation

### 1. Via KiCad Official Repository (Recommended)
Once the review process is complete, you can install KiSidian directly from KiCad:
1. Open the **Plugin & Content Manager** from the KiCad main dashboard.
2. Search for **KiSidian**.
3. Click **Install**, then click **Apply Pending Changes**.

### 2. Manual Installation (Release ZIP)
1. Download the latest `KiSidian-X.X.X-pcm.zip` from the [Releases](https://github.com/Ahmed-mek/KiSidian/releases) page.
2. In KiCad, open the **Plugin & Content Manager**.
3. Click **Install from File...** at the bottom.
4. Select the downloaded ZIP and click **Install**.

### 3. Developer & Local Testing
To test the plugin locally or contribute to development:
1. Clone this repository.
2. Run the build script to generate the PCM package:
   ```bash
   python3 build_pcm_package.py
   ```
3. The package will be created in the `dist/` folder.
4. You can add the local package to KiCad using the "Install from File" method mentioned above.

## 🚀 Usage
1. Open your PCB project in KiCad.
2. Click the **KiSidian icon** (Obsidian logo) in the top toolbar.
3. Start typing your engineering notes. 
4. **Auto-Save**: Closing the window automatically saves your notes to a `kisidian/` directory in your project folder.

## License
Apache License 2.0
