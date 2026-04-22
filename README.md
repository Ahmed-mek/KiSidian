# KiSidian (v1.3.0)

**KiSidian** is a KiCad Action Plugin designed to bring a professional, Obsidian-inspired note-taking experience directly into your PCB design workflow. It provides a powerful Markdown editor with a pixel-perfect dark mode preview.

![KiSidian UI](plugins/icon.png)

## 🌟 What's New in v1.3.0
- **Intelligent Checklist Support**: Support for `- [ ]` and `- [x]` with real-time color coding (Status-aware).
- **Premium Dark Mode Preview**: A completely redesigned live preview with smooth typography, custom scrollbars, and high-end CSS aesthetics.
- **Hidden Archive Storage**: Automatically manages a hidden `.kisidian/` directory to keep your project root clean.
- **Explicit Save Control**: Added a dedicated "Save Notes" button for peace of mind.

## ✨ Features
- **Split-Pane Editor**: Write Markdown on the left, see the rendered HTML on the right in real-time.
- **Obsidian-Inspired Theme**: A beautiful, eye-friendly dark mode palette.
- **Syntax Highlighting**: Real-time highlighting for headers, bold, italics, code blocks, and tags.
- **Project-Relative Persistence**: Notes are saved directly within your project folder, ensuring they travel with your design.
- **Zero Dependencies**: Bundled with the `markdown` library—no external setup required.

## 📖 Our Story: The Power of Good Notes
Every hardware project starts with excitement—that rush when a new board idea clicks into place. But somewhere between the first schematic and the final layout, things get messy. You're routing traces at 2 AM, chasing DRC errors, and fixing the same footprint issue for the third time.

We noticed a pattern: the projects that succeed aren't always the most clever designs—they’re the ones with clear notes. **KiSidian** was born from a simple realization: a note written today saves hours tomorrow, and a design decision documented now prevents the same argument six months later.

Originally started as a scratch pad to track design decisions, we built **KiSidian** to ensure your notes live exactly where they belong—embedded within your KiCad project. It’s built for engineers who've learned that memory is unreliable, but good notes aren't.

**KiSidian** is open source because good tools should be shared. If it helps you ship better boards, then we've achieved our goal.

## 📦 Installation
### 1. Via KiCad Official Repository (Recommended)
1. Open the **Plugin & Content Manager** from the KiCad main dashboard.
2. Search for **KiSidian**.
3. Click **Install**, then click **Apply Pending Changes**.

### 2. Manual Installation (Release ZIP)
1. Download the latest `KiSidian-1.3.0-pcm.zip` from the [Releases](https://github.com/Ahmed-mek/KiSidian/releases) page.
2. In KiCad, open the **Plugin & Content Manager**.
3. Click **Install from File...** and select the ZIP.

## 🚀 Usage
1. Open your PCB project.
2. Click the **KiSidian icon** in the top toolbar.
3. Start documenting! Your notes are safe in the `kisidian/` folder.

## License
Apache License 2.0
