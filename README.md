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

## Installation

### Via KiCad Plugin & Content Manager (Recommended)
1. Open KiCad.
2. Open the **Plugin & Content Manager** from the main dashboard.
3. Search for **KiSidian**.
4. Click **Install**.

### Manual Installation
1. Download the latest release ZIP.
2. Extract the contents into your KiCad 3rd party plugins folder:
    - **Linux**: `~/.local/share/kicad/8.0/3rdparty/plugins/`
    - **Windows**: `%APPDATA%\kicad\8.0\3rdparty\plugins\`
    - **macOS**: `~/Library/Application Support/kicad/8.0/3rdparty/plugins/`

## Usage
1. Open your PCB project in KiCad.
2. Click the KiSidian icon in the top toolbar or press `Ctrl + Alt + K`.
3. Start typing your notes. They will be saved to `notes.md` in your project folder when you close the window.

## License
Apache License 2.0
