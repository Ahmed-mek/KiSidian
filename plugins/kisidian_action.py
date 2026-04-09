import pcbnew
import os
import sys
import html
import re
import wx
import wx.stc as stc

# Add local lib directory to sys.path for vendored dependencies
PLUG_DIR = os.path.abspath(os.path.dirname(__file__))
LIB_DIR = os.path.join(PLUG_DIR, 'lib')
if LIB_DIR not in sys.path:
    sys.path.insert(0, LIB_DIR)

try:
    import wx.html2 as _html2
except Exception:
    _html2 = None
    import wx.html as _html

try:
    import markdown as _markdown
except Exception:
    _markdown = None


# Obsidian-inspired dark palette
APP_BG = "#16181D"
EDITOR_BG = "#1E1F22"
EDITOR_FG = "#D4D4D4"
PREVIEW_BG = "#1E1F22"
GUTTER_BG = "#181A1F"
GUTTER_FG = "#5C6370"
DIVIDER = "#2A2D34"
CARET = "#7AA2F7"
SELECTION = "#2F3340"
CURRENT_LINE = "#23262D"
LINK = "#8AB4F8"
TAG = "#7DCFFF"
PURPLE = "#C792EA"
GREEN = "#98C379"
ORANGE = "#D19A66"
YELLOW = "#E5C07B"
RED = "#E06C75"
COMMENT = "#6B7280"
CODE_BG = "#191B20"
INLINE_CODE_BG = "#2A2D34"
BLOCKQUOTE_BAR = "#4C566A"
HR_COLOR = "#31343C"

PREVIEW_CSS = f"""
body {{
    font-family: "Inter", "Segoe UI", "Ubuntu", "DejaVu Sans", sans-serif;
    background: {PREVIEW_BG};
    color: {EDITOR_FG};
    margin: 0;
    padding: 28px 34px;
    line-height: 1.72;
    font-size: 15px;
}}

* {{ box-sizing: border-box; }}

h1, h2, h3, h4, h5, h6 {{
    color: #E5E9F0;
    font-weight: 700;
    margin-top: 1.4em;
    margin-bottom: 0.55em;
    line-height: 1.25;
}}

h1 {{
    font-size: 2.15rem;
    border-bottom: 1px solid {DIVIDER};
    padding-bottom: 0.38em;
}}

h2 {{
    font-size: 1.6rem;
    border-bottom: 1px solid #23262D;
    padding-bottom: 0.28em;
}}

h3 {{ font-size: 1.28rem; }}
h4 {{ font-size: 1.08rem; }}

p {{ margin: 0.75em 0; }}

a {{
    color: {LINK};
    text-decoration: none;
}}

a:hover {{ text-decoration: underline; }}

hr {{
    border: none;
    border-top: 1px solid {HR_COLOR};
    margin: 1.5em 0;
}}

blockquote {{
    margin: 1em 0;
    padding: 0.2em 0 0.2em 1em;
    border-left: 4px solid {BLOCKQUOTE_BAR};
    color: #C8CDD7;
    background: rgba(255,255,255,0.02);
}}

code {{
    font-family: "JetBrains Mono", "Ubuntu Mono", "DejaVu Sans Mono", monospace;
    background: {INLINE_CODE_BG};
    color: {YELLOW};
    padding: 0.18em 0.4em;
    border-radius: 6px;
    font-size: 0.95em;
}}

pre {{
    background: {CODE_BG};
    color: {EDITOR_FG};
    padding: 14px 16px;
    border-radius: 10px;
    overflow-x: auto;
    border: 1px solid {DIVIDER};
    box-shadow: inset 0 1px 0 rgba(255,255,255,0.02);
}}

pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    border-radius: 0;
}}

ul, ol {{
    margin: 0.5em 0 1em 1.45em;
    padding: 0;
}}

li {{ margin: 0.35em 0; }}

img {{
    max-width: 100%;
    border-radius: 10px;
}}

table {{
    width: 100%;
    border-collapse: collapse;
    margin: 1em 0;
    overflow: hidden;
    border-radius: 10px;
    border: 1px solid {DIVIDER};
}}

th, td {{
    text-align: left;
    padding: 10px 12px;
    border-bottom: 1px solid {DIVIDER};
}}

th {{
    background: #23262D;
    color: #E5E9F0;
}}

tr:nth-child(even) td {{
    background: rgba(255,255,255,0.015);
}}

.tag {{
    color: {TAG};
    font-weight: 600;
}}

.wikilink {{
    color: {PURPLE};
    font-weight: 600;
}}

.callout {{
    border: 1px solid {DIVIDER};
    border-left: 4px solid {LINK};
    background: rgba(122,162,247,0.08);
    border-radius: 10px;
    padding: 12px 14px;
    margin: 1em 0;
}}

.callout-title {{
    font-weight: 700;
    margin-bottom: 6px;
    color: #E5E9F0;
}}

.callout-note {{ border-left-color: {LINK}; }}
.callout-warning {{ border-left-color: {ORANGE}; background: rgba(209,154,102,0.08); }}
.callout-tip {{ border-left-color: {GREEN}; background: rgba(152,195,121,0.08); }}
.callout-danger {{ border-left-color: {RED}; background: rgba(224,108,117,0.08); }}
"""


SAMPLE_TEXT = """# KiSidian: Obsidian-style Notes for KiCad

A powerful, distraction-free **Markdown editor** with **live preview** integrated directly into your KiCad workflow.

## Key Features
- **Project-Aware Storage**: Automatically saves `notes.md` inside your KiCad project folder.
- **Obsidian Styling**: Minimalist dark interface inspired by Obsidian.
- **Advanced Markdown**: Supports tables, task lists, and code highlighting.
- **Rich Callouts**: Built-in support for notes, warnings, and tips using `[!kind]` syntax.
- **Tagging & Links**: Support for #tags and [[wikilinks]] for better organization.
- **Zero Setup**: Bundled with the `markdown` library for immediate use.

> [!tip]
> Your notes are saved automatically when you close this window. You can find them in the same directory as your `.kicad_pcb` file!

### Integrated Engineering Notes
```python
# Use the editor to document your design decisions:
PCB_REVISION = "1.0.4"
BOM_STATUS = "Verified"
```

### Development Roadmap
| Feature | Status | Priority |
|:---|:---|:---|
| Markdown Rendering | ✅ Done | High |
| Auto-save Implementation | ✅ Done | High |
| Attachment Support | ⏳ Planned | Medium |
| Remote Sync | 🗺️ Roadmap | Low |

---
*Developed for KiCad as a Productivity tool.*
"""



class StyledMarkdownCtrl(stc.StyledTextCtrl):
    """Markdown editor with Obsidian-like dark styling."""

    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._setup_editor()

    def _setup_editor(self):
        self.SetLexer(stc.STC_LEX_CONTAINER)
        self.SetWrapMode(stc.STC_WRAP_WORD)
        self.SetUseHorizontalScrollBar(False)
        self.SetScrollWidthTracking(True)
        self.SetTabWidth(4)
        self.SetIndent(4)
        self.SetUseTabs(False)
        self.SetEOLMode(stc.STC_EOL_LF)
        self.SetViewEOL(False)
        self.SetViewWhiteSpace(False)
        self.SetBufferedDraw(True)
        self.SetTechnology(stc.STC_TECHNOLOGY_DEFAULT)
        self.SetLayoutCache(stc.STC_CACHE_PAGE)
        self.SetExtraAscent(3)
        self.SetExtraDescent(3)
        self.SetCaretForeground(CARET)
        self.SetCaretLineVisible(True)
        self.SetCaretLineBackground(CURRENT_LINE)
        self.SetSelBackground(True, SELECTION)
        self.SetSelForeground(False, "#FFFFFF")

        # Margin 0: line numbers
        self.SetMarginType(0, stc.STC_MARGIN_NUMBER)
        self.SetMarginWidth(0, 52)
        self.SetMarginSensitive(0, False)

        # Margin 1: fold markers (note: manual styling requires manual fold handling too if desired)
        self.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        self.SetMarginWidth(1, 0) # Disable for now to simplify

        self._apply_theme()
        self._setup_markers()
        self.Bind(stc.EVT_STC_STYLENEEDED, self._on_style_needed)

    def _on_style_needed(self, event):
        pos = self.GetEndStyled()
        last = event.GetPosition()
        
        # Style the requested range line by line
        start_line = self.LineFromPosition(pos)
        end_line = self.LineFromPosition(last)
        
        for line_no in range(start_line, end_line + 1):
            line_start = self.PositionFromLine(line_no)
            line_end = self.GetLineEndPosition(line_no)
            line_text = self.GetLine(line_no)
            
            # Default style for the line
            self.StartStyling(line_start)
            self.SetStyling(len(line_text), 0)
            
            # 1. Headers Check (highest priority)
            # Headers MUST have a space after # (e.g., # Header)
            h_match = re.match(r'^(\s{0,3})(#+)\s+(.*)', line_text)
            if h_match:
                level = len(h_match.group(2))
                if 1 <= level <= 6:
                    self.StartStyling(line_start)
                    self.SetStyling(len(line_text), level) # Styles 1-6
                    continue 

            # 2. Inline Styles
            # Tags #tag (Hash followed by text, no space)
            # We look for #tag anywhere in the line
            for m in re.finditer(r'(^|\s)#([A-Za-z0-9_\-]+)', line_text):
                self.StartStyling(line_start + m.start())
                self.SetStyling(m.end() - m.start(), 12) # Style 12: Tag
                
            # Bold **text**
            for m in re.finditer(r'\*\*.*?\*\*', line_text):
                self.StartStyling(line_start + m.start())
                self.SetStyling(m.end() - m.start(), 7) # Style 7: Bold
                
            # Italic *text* (excluding bold matches usually)
            for m in re.finditer(r'(?<!\*)\*([^*]+)\*(?!\*)', line_text):
                self.StartStyling(line_start + m.start())
                self.SetStyling(m.end() - m.start(), 8) # Style 8: Italic

            # Inline Code `text`
            for m in re.finditer(r'`.*?`', line_text):
                self.StartStyling(line_start + m.start())
                self.SetStyling(m.end() - m.start(), 10) # Style 10: Code
                
            # Links [text](url)
            for m in re.finditer(r'\[.*?\]\(.*?\)', line_text):
                self.StartStyling(line_start + m.start())
                self.SetStyling(m.end() - m.start(), 9) # Style 9: Link

    def _apply_theme(self):
        default_spec = f"face:JetBrains Mono,Ubuntu Mono,DejaVu Sans Mono,size:11,fore:{EDITOR_FG},back:{EDITOR_BG}"
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, default_spec)
        self.StyleClearAll()

        # Custom Styles for Container Lexer
        # 0: Default
        # 1-6: Headers
        # 7: Bold
        # 8: Italic
        # 9: Link
        # 10: Code
        # 11: Blockquote

        h_base = f"fore:{PURPLE},bold,face:sans-serif"
        self.StyleSetSpec(1, f"{h_base},size:20")
        self.StyleSetSpec(2, f"{h_base},size:18")
        self.StyleSetSpec(3, f"{h_base},size:16")
        self.StyleSetSpec(4, f"{h_base},size:14")
        self.StyleSetSpec(5, f"{h_base},size:13")
        self.StyleSetSpec(6, f"{h_base},size:12")

        self.StyleSetSpec(7, f"fore:{YELLOW},bold")
        self.StyleSetSpec(8, f"fore:{PURPLE},italic")
        self.StyleSetSpec(9, f"fore:{LINK},underline")
        self.StyleSetSpec(10, f"fore:{GREEN},back:{INLINE_CODE_BG}")
        self.StyleSetSpec(11, f"fore:{COMMENT},italic")
        self.StyleSetSpec(12, f"fore:{TAG},bold") # Style 12: Tag

        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, f"face:JetBrains Mono,Ubuntu Mono,size:10,fore:{GUTTER_FG},back:{GUTTER_BG}")

        self.SetFoldMarginColour(True, GUTTER_BG)
        self.SetFoldMarginHiColour(True, GUTTER_BG)
        self.SetBackgroundColour(EDITOR_BG)
        self.SetForegroundColour(EDITOR_FG)

    def _setup_markers(self):
        fg = "#ABB2BF"
        bg = GUTTER_BG
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPEN, stc.STC_MARK_BOXMINUS, fg, bg)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDER, stc.STC_MARK_BOXPLUS, fg, bg)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERSUB, stc.STC_MARK_VLINE, fg, bg)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERTAIL, stc.STC_MARK_LCORNER, fg, bg)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEREND, stc.STC_MARK_BOXPLUSCONNECTED, fg, bg)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDEROPENMID, stc.STC_MARK_BOXMINUSCONNECTED, fg, bg)
        self.MarkerDefine(stc.STC_MARKNUM_FOLDERMIDTAIL, stc.STC_MARK_TCORNER, fg, bg)

    def _on_margin_click(self, event):
        if event.GetMargin() == 1:
            line = self.LineFromPosition(event.GetPosition())
            if self.GetFoldLevel(line) & stc.STC_FOLDLEVELHEADERFLAG:
                self.ToggleFold(line)


class LivePreviewFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="KiSidian", size=(1280, 760))
        self.notes_file = None
        self._preview_timer = None
        self._build_ui()
        self.Bind(wx.EVT_CLOSE, self._on_close)
    def _update_preview(self):
        # We'll call this after setting text or on change
        pass

    def load_content(self, text):
        self.editor.SetText(text)
        self._update_preview()

    def get_content(self):
        return self.editor.GetValue()

    def _build_ui(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour(APP_BG)

        root = wx.BoxSizer(wx.VERTICAL)

        header = self._build_header(panel)
        root.Add(header, 0, wx.EXPAND | wx.LEFT | wx.RIGHT | wx.TOP, 10)

        splitter = wx.SplitterWindow(panel, style=wx.SP_LIVE_UPDATE | wx.BORDER_NONE)
        splitter.SetSashGravity(0.5)
        splitter.SetMinimumPaneSize(260)
        splitter.SetBackgroundColour(DIVIDER)

        editor_panel = wx.Panel(splitter)
        preview_panel = wx.Panel(splitter)
        editor_panel.SetBackgroundColour(EDITOR_BG)
        preview_panel.SetBackgroundColour(PREVIEW_BG)

        self.editor = StyledMarkdownCtrl(editor_panel)
        # Internal patching is handled by StyledMarkdownCtrl itself.
        # We also need to trigger the preview update here.
        self.editor.Bind(stc.EVT_STC_CHANGE, self._on_text_change)

        self.preview = self._make_preview_ctrl(preview_panel)
        try:
            self.preview.SetBackgroundColour(PREVIEW_BG)
        except Exception:
            pass

        editor_box = wx.BoxSizer(wx.VERTICAL)
        editor_box.Add(self.editor, 1, wx.EXPAND | wx.ALL, 12)
        editor_panel.SetSizer(editor_box)

        preview_box = wx.BoxSizer(wx.VERTICAL)
        preview_box.Add(self.preview, 1, wx.EXPAND | wx.ALL, 12)
        preview_panel.SetSizer(preview_box)

        splitter.SplitVertically(editor_panel, preview_panel, sashPosition=640)
        root.Add(splitter, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizer(root)
        self.SetBackgroundColour(APP_BG)

    def _build_header(self, parent):
        header = wx.Panel(parent)
        header.SetBackgroundColour("#1B1D23")

        sizer = wx.BoxSizer(wx.HORIZONTAL)

        title = wx.StaticText(header, label="Advanced Markdown Editor")
        title_font = wx.Font(12, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        title.SetFont(title_font)
        title.SetForegroundColour("#E5E9F0")

        subtitle = wx.StaticText(header, label="Obsidian-like dark editor + live preview")
        subtitle.SetForegroundColour("#8B949E")

        left = wx.BoxSizer(wx.VERTICAL)
        left.Add(title, 0, wx.BOTTOM, 2)
        left.Add(subtitle, 0)

        sizer.Add(left, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 12)
        sizer.AddStretchSpacer()

        badge = wx.StaticText(header, label="Markdown")
        badge.SetForegroundColour("#DCE3EA")
        badge.SetBackgroundColour("#2A2D34")
        badge.SetWindowStyleFlag(wx.BORDER_NONE)
        sizer.Add(badge, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 12)

        header.SetSizer(sizer)
        return header

    def _make_preview_ctrl(self, parent):
        if _html2 is not None:
            return _html2.WebView.New(parent)
        preview = _html.HtmlWindow(parent)
        preview.SetStandardFonts()
        return preview

    def _preprocess_markdown(self, text):
        # basic Obsidian-like callouts
        lines = text.splitlines()
        out = []
        i = 0
        in_code = False
        while i < len(lines):
            line = lines[i]
            if line.strip().startswith("```"):
                in_code = not in_code
                out.append(line)
                i += 1
                continue

            if not in_code:
                callout = re.match(r'^\s*>\s*\[!(\w+)\]\s*(.*)$', line)
                if callout:
                    kind = callout.group(1).lower()
                    title = callout.group(1).capitalize()
                    content = [callout.group(2)]
                    i += 1
                    while i < len(lines) and lines[i].lstrip().startswith('>'):
                        content.append(lines[i].lstrip()[1:].lstrip())
                        i += 1
                    out.append(
                        f'<div class="callout callout-{kind}">'
                        f'<div class="callout-title">{html.escape(title)}</div>'
                        f'<div>{html.escape(chr(10).join(content))}</div>'
                        f'</div>'
                    )
                    continue

            out.append(line)
            i += 1

        processed = "\n".join(out)
        processed = re.sub(r'(^|[\s\(])(#([A-Za-z0-9_\-]+))', r'\1<span class="tag">#\3</span>', processed)
        processed = re.sub(r'\[\[([^\]|]+)\|([^\]]+)\]\]', r'<span class="wikilink">\2</span>', processed)
        processed = re.sub(r'\[\[([^\]]+)\]\]', r'<span class="wikilink">\1</span>', processed)
        return processed

    def _render_markdown(self, text):
        processed = self._preprocess_markdown(text)
        if _markdown is None:
            return "<pre>" + html.escape(text) + "</pre>"
        return _markdown.markdown(
            processed,
            extensions=["fenced_code", "tables", "sane_lists", "nl2br"],
        )

    def _set_preview_html(self, html_doc):
        if _html2 is not None:
            self.preview.SetPage(html_doc, "")
        else:
            self.preview.SetPage(html_doc)

    def _update_preview(self):
        rendered = self._render_markdown(self.editor.GetValue())
        html_doc = (
            "<!doctype html><html><head>"
            "<meta charset='utf-8'>"
            f"<style>{PREVIEW_CSS}</style>"
            "</head><body>"
            f"{rendered}"
            "</body></html>"
        )
        self._set_preview_html(html_doc)

    def _on_text_change(self, event):
        if self._preview_timer is not None:
            self._preview_timer.Stop()
        self._preview_timer = wx.CallLater(120, self._update_preview)
        event.Skip()

    def _on_close(self, event):
        if self.notes_file:
            try:
                # Ensure directory exists
                project_dir = os.path.dirname(self.notes_file)
                if not os.path.exists(project_dir):
                    os.makedirs(project_dir)
                
                with open(self.notes_file, 'w', encoding='utf-8') as f:
                    f.write(self.editor.GetValue())
            except Exception as e:
                wx.MessageBox(f"Error saving notes: {str(e)}", "KiSidian Error", wx.OK | wx.ICON_ERROR)
        
        self.Destroy()


class KiSidianPlugin(pcbnew.ActionPlugin):
    def __init__(self):
        super().__init__()
        self.frame = None

    def defaults(self):
        self.name = "KiSidian"
        self.category = "Productivity"
        self.description = "Obsidian-style notes inside KiCad"
        self.show_toolbar_button = True
        self.shortcut = "Ctrl+Alt+K"
        # Load icon dynamically
        self.icon_file_name = os.path.join(PLUG_DIR, "icon.png")

    def Run(self):
        # Prevent multiple instances
        if self.frame:
            try:
                self.frame.Raise()
                return
            except Exception:
                self.frame = None

        # Try to find the project directory
        try:
            board = pcbnew.GetBoard()
            pcb_path = board.GetFileName()
            if pcb_path:
                project_dir = os.path.dirname(pcb_path)
                notes_file = os.path.join(project_dir, "notes.md")
            else:
                notes_file = None
        except Exception:
            notes_file = None

        self.frame = LivePreviewFrame()
        
        # Load existing notes if any
        content = SAMPLE_TEXT
        if notes_file and os.path.exists(notes_file):
            try:
                with open(notes_file, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                wx.MessageBox(f"Error loading notes: {str(e)}", "KiSidian Error", wx.OK | wx.ICON_ERROR)

        self.frame.editor.SetText(content)
        self.frame.notes_file = notes_file # Store it in frame to save later
        
        self.frame.Show()

