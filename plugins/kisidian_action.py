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
html {{
    background-color: {PREVIEW_BG};
    color-scheme: dark;
}}

body {{
    font-family: "Inter", "Segoe UI", "SF Pro Display", "Roboto", sans-serif;
    background-color: {PREVIEW_BG};
    color: {EDITOR_FG};
    margin: 0;
    padding: 30px 40px;
    line-height: 1.8;
    font-size: 16px;
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
    text-rendering: optimizeLegibility;
}}

* {{ box-sizing: border-box; }}

::selection {{
    background: rgba(122, 162, 247, 0.3);
    color: inherit;
}}

/* Minimalist Scrollbar */
::-webkit-scrollbar {{
    width: 8px;
    height: 8px;
}}
::-webkit-scrollbar-track {{
    background: transparent;
}}
::-webkit-scrollbar-thumb {{
    background: {DIVIDER};
    border-radius: 10px;
}}
::-webkit-scrollbar-thumb:hover {{
    background: {COMMENT};
}}

h1, h2, h3, h4, h5, h6 {{
    color: #F8F9FB;
    font-weight: 700;
    margin-top: 1.6em;
    margin-bottom: 0.6em;
    line-height: 1.3;
}}

h1 {{
    font-size: 2.4rem;
    border-bottom: 1px solid {DIVIDER};
    padding-bottom: 0.4em;
    letter-spacing: -0.02em;
}}

h2 {{
    font-size: 1.8rem;
    border-bottom: 1px solid rgba(255,255,255, 0.05);
    padding-bottom: 0.3em;
    letter-spacing: -0.01em;
}}

h3 {{ font-size: 1.4rem; }}
h4 {{ font-size: 1.15rem; }}

p {{ margin: 1em 0; }}

a {{
    color: {LINK};
    text-decoration: none;
    transition: color 0.2s ease;
    border-bottom: 1px solid transparent;
}}

a:hover {{
    color: #A0C3FF;
    border-bottom-color: {LINK};
}}

hr {{
    border: none;
    border-top: 1px solid {HR_COLOR};
    margin: 2em 0;
    opacity: 0.6;
}}

blockquote {{
    margin: 1.5em 0;
    padding: 0.5em 1.2em;
    border-left: 4px solid {BLOCKQUOTE_BAR};
    color: #ABB2BF;
    background: rgba(255,255,255,0.02);
    border-radius: 0 8px 8px 0;
}}

code {{
    font-family: "JetBrains Mono", "SF Mono", "Menlo", monospace;
    background: {INLINE_CODE_BG};
    color: {YELLOW};
    padding: 0.2em 0.45em;
    border-radius: 6px;
    font-size: 0.9em;
}}

pre {{
    background: {CODE_BG};
    color: {EDITOR_FG};
    padding: 20px;
    border-radius: 12px;
    overflow-x: auto;
    border: 1px solid {DIVIDER};
    box-shadow: 0 4px 12px rgba(0,0,0,0.2);
    margin: 1.5em 0;
}}

pre code {{
    background: transparent;
    color: inherit;
    padding: 0;
    border-radius: 0;
    line-height: 1.5;
}}

ul, ol {{
    margin: 1em 0 1.5em 1.6em;
    padding: 0;
}}

li {{ margin: 0.5em 0; }}

img {{
    max-width: 100%;
    border-radius: 12px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.3);
    margin: 1.5em 0;
}}

table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    margin: 1.5em 0;
    overflow: hidden;
    border-radius: 10px;
    border: 1px solid {DIVIDER};
}}

th, td {{
    text-align: left;
    padding: 12px 16px;
    border-bottom: 1px solid {DIVIDER};
}}

th {{
    background: #23262D;
    color: #F8F9FB;
    font-weight: 600;
    text-transform: uppercase;
    font-size: 0.85em;
    letter-spacing: 0.05em;
}}

tr:last-child td {{
    border-bottom: none;
}}

tr:nth-child(even) td {{
    background: rgba(255,255,255,0.015);
}}

/* Checkbox styling */
input[type="checkbox"] {{
    appearance: none;
    -webkit-appearance: none;
    width: 16px;
    height: 16px;
    border: 1.5px solid {GREEN};
    border-radius: 4px;
    background: rgba(152,195,121,0.1);
    cursor: default;
    vertical-align: middle;
    margin-right: 10px;
    position: relative;
    top: -1px;
}}
input[type="checkbox"]:checked {{
    background: {RED};
    border-color: {RED};
}}
input[type="checkbox"]:checked::after {{
    content: "L";
    position: absolute;
    left: 4px;
    top: -2px;
    width: 6px;
    height: 10px;
    border: solid white;
    border-width: 0 2px 2px 0;
    transform: rotate(45deg);
}}

.tag {{
    color: {TAG};
    font-weight: 600;
    background: rgba(125, 207, 255, 0.1);
    padding: 1px 6px;
    border-radius: 4px;
}}

.wikilink {{
    color: {PURPLE};
    font-weight: 600;
    border-bottom: 1px dashed {PURPLE};
}}

.callout {{
    border: 1px solid {DIVIDER};
    border-left: 4px solid {LINK};
    background: rgba(122,162,247,0.06);
    border-radius: 12px;
    padding: 16px 20px;
    margin: 1.5em 0;
    box-shadow: 0 4px 12px rgba(0,0,0,0.1);
}}

.callout-title {{
    font-weight: 750;
    margin-bottom: 8px;
    color: #F8F9FB;
    font-size: 1.05em;
    display: flex;
    align-items: center;
}}

.callout-note {{ border-left-color: {LINK}; }}
.callout-warning {{ border-left-color: {ORANGE}; background: rgba(209,154,102,0.06); }}
.callout-tip {{ border-left-color: {GREEN}; background: rgba(152,195,121,0.06); }}
.callout-danger {{ border-left-color: {RED}; background: rgba(224,108,117,0.06); }}
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


- [ ] مهمة غير مكتملة
- [x] مهمة مكتملة

---
*Developed for KiCad as a Productivity tool.*
"""

class TabButton(wx.Panel):
    """Custom tab button with hover and active states."""
    def __init__(self, parent, filename, label, is_active, callback, right_callback=None):
        super().__init__(parent)
        self.filename = filename
        self.label = label
        self.is_active = is_active
        self.callback = callback
        self.right_callback = right_callback
        self.hover = False
        
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        self.SetBackgroundStyle(wx.BG_STYLE_PAINT)
        
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_ENTER_WINDOW, self.OnEnter)
        self.Bind(wx.EVT_LEAVE_WINDOW, self.OnLeave)
        self.Bind(wx.EVT_LEFT_DOWN, self.OnClick)
        self.Bind(wx.EVT_RIGHT_DOWN, self.OnRightClick)
        
        # Calculate size based on label
        font = wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD)
        # We need a DC to measure text
        temp_dc = wx.ScreenDC()
        temp_dc.SetFont(font)
        w, h = temp_dc.GetTextExtent(label)
        self.SetMinSize((w + 32, 40)) 

    def OnEnter(self, event):
        self.hover = True
        self.Refresh()

    def OnLeave(self, event):
        self.hover = False
        self.Refresh()

    def OnClick(self, event):
        self.callback(self.filename)

    def OnRightClick(self, event):
        if self.right_callback:
            self.right_callback(self.filename, event)

    def OnPaint(self, event):
        dc = wx.AutoBufferedPaintDC(self)
        
        # Background
        bg_color = wx.Colour("#2D3139") if self.hover and not self.is_active else wx.Colour("#1B1D23")
        if self.is_active: 
            bg_color = wx.Colour("#16181D")
        
        dc.SetBackground(wx.Brush(bg_color))
        dc.Clear()
        
        # Text
        text_color = wx.Colour("#FFFFFF") if self.is_active else (wx.Colour("#DCE3EA") if self.hover else wx.Colour(COMMENT))
        dc.SetTextForeground(text_color)
        dc.SetFont(wx.Font(9, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_BOLD))
        
        w, h = self.GetSize()
        tw, th = dc.GetTextExtent(self.label)
        dc.DrawText(self.label, (w - tw) // 2, (h - th) // 2)
        
        # Active Indicator (Bottom line)
        if self.is_active:
            dc.SetPen(wx.Pen(wx.Colour(PURPLE), 3))
            dc.DrawLine(0, h-1, w, h-1)



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

            # Checkboxes [ ] and [x]
            for m in re.finditer(r'\[\s\]', line_text):
                self.StartStyling(line_start + m.start())
                self.SetStyling(m.end() - m.start(), 13) # Style 13: Unchecked
            for m in re.finditer(r'\[x\]', line_text):
                self.StartStyling(line_start + m.start())
                self.SetStyling(m.end() - m.start(), 14) # Style 14: Checked
                
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
        self.StyleSetSpec(13, f"fore:{GREEN},bold") # Style 13: Unchecked (Now Green)
        self.StyleSetSpec(14, f"fore:{RED},bold") # Style 14: Checked (Now Red)

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
    def __init__(self, project_dir=None):
        super().__init__(None, title="KiSidian", size=(1280, 800))
        self.project_dir = project_dir
        self.kisidian_dir = os.path.join(project_dir, "kisidian") if project_dir else None
        self.active_file = None
        self._preview_timer = None
        self.show_preview = True
        
        self.core_files = {
            "design_notes.md": "Design Notes",
            "component_note.md": "Component Note",
            "checklist.md": "Checklist"
        }

        self._ensure_kisidian_setup()
        self._build_ui()
        self.Bind(wx.EVT_CLOSE, self._on_close)
        
        # Load first file by default
        if self.kisidian_dir:
            self._refresh_file_list()
            self._on_file_selected("design_notes.md")

    def _ensure_kisidian_setup(self):
        if not self.kisidian_dir:
            return
            
        if not os.path.exists(self.kisidian_dir):
            os.makedirs(self.kisidian_dir)
            
        # Create core files if missing
        for filename, title in self.core_files.items():
            path = os.path.join(self.kisidian_dir, filename)
            if not os.path.exists(path):
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(f"# {title}\n\nStart writing your notes here...")

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
        root.Add(header, 0, wx.EXPAND)

        # Tabs Area
        self.tabs_container = wx.Panel(panel)
        self.tabs_container.SetBackgroundColour("#1B1D23")
        self.tab_sizer = wx.BoxSizer(wx.HORIZONTAL)
        self.tabs_container.SetSizer(self.tab_sizer)
        
        root.Add(self.tabs_container, 0, wx.EXPAND)
        
        # Thin divider below tabs
        divider = wx.Panel(panel, size=(-1, 1))
        divider.SetBackgroundColour(DIVIDER)
        root.Add(divider, 0, wx.EXPAND)

        # Content Splitter
        self.splitter = wx.SplitterWindow(panel, style=wx.SP_LIVE_UPDATE | wx.BORDER_NONE)
        self.splitter.SetSashGravity(0.5)
        self.splitter.SetMinimumPaneSize(300)
        self.splitter.SetBackgroundColour(DIVIDER)

        self.editor_panel = wx.Panel(self.splitter)
        self.preview_panel = wx.Panel(self.splitter)
        self.editor_panel.SetBackgroundColour(EDITOR_BG)
        self.preview_panel.SetBackgroundColour(PREVIEW_BG)

        self.editor = StyledMarkdownCtrl(self.editor_panel)
        self.editor.Bind(stc.EVT_STC_CHANGE, self._on_text_change)

        self.preview = self._make_preview_ctrl(self.preview_panel)
        try:
            self.preview.SetBackgroundColour(PREVIEW_BG)
        except Exception:
            pass

        editor_box = wx.BoxSizer(wx.VERTICAL)
        editor_box.Add(self.editor, 1, wx.EXPAND | wx.ALL, 12)
        self.editor_panel.SetSizer(editor_box)

        preview_box = wx.BoxSizer(wx.VERTICAL)
        preview_box.Add(self.preview, 1, wx.EXPAND | wx.ALL, 12)
        self.preview_panel.SetSizer(preview_box)

        self.splitter.SplitVertically(self.editor_panel, self.preview_panel, sashPosition=500)
        root.Add(self.splitter, 1, wx.EXPAND)

        panel.SetSizer(root)
        self.SetBackgroundColour(APP_BG)

    def _refresh_file_list(self):
        if not self.kisidian_dir or not os.path.exists(self.kisidian_dir):
            return
            
        files = [f for f in os.listdir(self.kisidian_dir) if f.endswith(".md")]
        core_ordered = [f for f in self.core_files.keys() if f in files]
        others = sorted([f for f in files if f not in self.core_files.keys()])
        all_files = core_ordered + others
        
        self.file_items = all_files
        self._update_tab_buttons()

    def _update_tab_buttons(self):
        # Clear existing tabs
        self.tab_sizer.Clear(True)
        self.tab_buttons = {}

        for filename in self.file_items:
            display_name = self.core_files.get(filename, filename.replace(".md", "").replace("_", " ").title())
            is_active = (filename == self.active_file)
            
            tab = TabButton(self.tabs_container, filename, display_name, is_active, self._on_tab_click, self._on_tab_right_click)
            self.tab_sizer.Add(tab, 0, wx.EXPAND)
            self.tab_buttons[filename] = tab

        self.tabs_container.Layout()

    def _on_toggle_preview(self, event):
        if self.show_preview:
            self.splitter.Unsplit(self.preview_panel)
            self.toggle_preview_btn.SetLabel("Show Preview")
        else:
            self.splitter.SplitVertically(self.editor_panel, self.preview_panel, 500)
            self.toggle_preview_btn.SetLabel("Hide Preview")
        
        self.show_preview = not self.show_preview
        self.Layout()

    def _on_tab_click(self, filename):
        self._on_file_selected(filename)

    def _on_tab_right_click(self, filename, event):
        menu = wx.Menu()
        
        item_add = menu.Append(wx.ID_ANY, "Add New Note")
        item_refresh = menu.Append(wx.ID_ANY, "Refresh List")
        menu.AppendSeparator()
        
        item_rename = menu.Append(wx.ID_ANY, f"Rename '{filename}'")
        item_delete = menu.Append(wx.ID_ANY, f"Delete '{filename}'")
        
        # Disable rename/delete for core files
        if filename in self.core_files:
            item_rename.Enable(False)
            item_delete.Enable(False)
            
        self.Bind(wx.EVT_MENU, self._on_add_file, item_add)
        self.Bind(wx.EVT_MENU, lambda e: self._refresh_file_list(), item_refresh)
        self.Bind(wx.EVT_MENU, lambda e: self._on_rename_file(filename), item_rename)
        self.Bind(wx.EVT_MENU, lambda e: self._on_delete_file(filename), item_delete)
        
        self.PopupMenu(menu)
        menu.Destroy()

    def _on_add_file(self, event):
        dlg = wx.TextEntryDialog(self, "Enter new note name (e.g. my_ideas):", "Add New Note")
        if dlg.ShowModal() == wx.ID_OK:
            name = dlg.GetValue().strip()
            if not name: return
            if not name.endswith(".md"): name += ".md"
            
            path = os.path.join(self.kisidian_dir, name)
            if os.path.exists(path):
                wx.MessageBox("A file with this name already exists.", "Error", wx.OK | wx.ICON_ERROR)
                return
                
            try:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(f"# {name.replace('.md', '').replace('_', ' ').title()}\n\n")
                self._refresh_file_list()
                self._on_file_selected(name)
            except Exception as e:
                wx.MessageBox(f"Could not create file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def _on_rename_file(self, filename):
        old_path = os.path.join(self.kisidian_dir, filename)
        dlg = wx.TextEntryDialog(self, f"Rename '{filename}' to:", "Rename Note", filename)
        if dlg.ShowModal() == wx.ID_OK:
            new_name = dlg.GetValue().strip()
            if not new_name or new_name == filename: return
            if not new_name.endswith(".md"): new_name += ".md"
            
            new_path = os.path.join(self.kisidian_dir, new_name)
            if os.path.exists(new_path):
                wx.MessageBox("A file with this name already exists.", "Error", wx.OK | wx.ICON_ERROR)
                return
                
            try:
                os.rename(old_path, new_path)
                if self.active_file == filename:
                    self.active_file = new_name
                self._refresh_file_list()
            except Exception as e:
                wx.MessageBox(f"Could not rename file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)
        dlg.Destroy()

    def _on_delete_file(self, filename):
        path = os.path.join(self.kisidian_dir, filename)
        msg = f"Are you sure you want to delete '{filename}'?\nThis action cannot be undone."
        if wx.MessageBox(msg, "Confirm Deletion", wx.YES_NO | wx.ICON_WARNING) == wx.YES:
            try:
                os.remove(path)
                if self.active_file == filename:
                    self.active_file = "design_notes.md"
                self._refresh_file_list()
                if self.active_file == "design_notes.md":
                    # Force reload design notes if we were on the deleted file
                    self._on_file_selected("design_notes.md")
            except Exception as e:
                wx.MessageBox(f"Could not delete file: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

    def _on_file_selected(self, filename):
        if self.active_file == filename:
            return
            
        if self.active_file:
            self._save_to_file()
            
        self.active_file = filename
        path = os.path.join(self.kisidian_dir, filename)
        
        if os.path.exists(path):
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
                self.editor.SetText(content)
                self._update_preview()
                self._update_tab_buttons() # Redraw tabs to update highlight
            except Exception as e:
                wx.MessageBox(f"Error loading {filename}: {str(e)}", "Error", wx.OK | wx.ICON_ERROR)

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
        
        self.toggle_preview_btn = wx.Button(header, label="Hide Preview", size=(120, 30))
        self.toggle_preview_btn.SetBackgroundColour("#2D3139")
        self.toggle_preview_btn.SetForegroundColour("#E5E9F0")
        self.toggle_preview_btn.Bind(wx.EVT_BUTTON, self._on_toggle_preview)

        save_btn = wx.Button(header, label="Save Notes", size=(100, 30))
        save_btn.SetBackgroundColour("#2D3139")
        save_btn.SetForegroundColour("#E5E9F0")
        save_btn.Bind(wx.EVT_BUTTON, self._on_save_clicked)

        sizer.Add(self.toggle_preview_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 12)
        sizer.Add(save_btn, 0, wx.ALL | wx.ALIGN_CENTER_VERTICAL, 12)
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
        # Checkboxes
        processed = re.sub(r'-\s+\[\s\]\s+(.*)', r'<p><input type="checkbox" disabled /> \1</p>', processed)
        processed = re.sub(r'-\s+\[x\]\s+(.*)', r'<p><input type="checkbox" disabled checked /> \1</p>', processed)
        
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
            "<meta name='color-scheme' content='dark'>"
            f"<style>{PREVIEW_CSS}</style>"
            f"</head><body bgcolor='{PREVIEW_BG}' text='{EDITOR_FG}'>"
            f"{rendered}"
            "</body></html>"
        )
        self._set_preview_html(html_doc)

    def _on_text_change(self, event):
        if self._preview_timer is not None:
            self._preview_timer.Stop()
        self._preview_timer = wx.CallLater(120, self._update_preview)
        event.Skip()

    def _on_save_clicked(self, event):
        self._save_to_file()
        wx.MessageBox(f"'{self.active_file}' saved successfully to kisidian/", "KiSidian", wx.OK | wx.ICON_INFORMATION)

    def _save_to_file(self):
        if self.kisidian_dir and self.active_file:
            try:
                if not os.path.exists(self.kisidian_dir):
                    os.makedirs(self.kisidian_dir)
                
                path = os.path.join(self.kisidian_dir, self.active_file)
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(self.editor.GetValue())
            except Exception as e:
                wx.MessageBox(f"Error saving notes: {str(e)}", "KiSidian Error", wx.OK | wx.ICON_ERROR)

    def _on_close(self, event):
        self._save_to_file()
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
        project_dir = None
        try:
            board = pcbnew.GetBoard()
            pcb_path = board.GetFileName()
            if pcb_path:
                project_dir = os.path.dirname(pcb_path)
            else:
                # Try project manager context
                try:
                    project_dir = os.path.dirname(pcbnew.GetProjectPath())
                except:
                    pass
        except Exception:
            pass

        # If we have no project_dir, we might not be able to save
        if not project_dir:
            wx.MessageBox("Could not determine project directory. Notes might not be saved.", "KiSidian Warning", wx.OK | wx.ICON_WARNING)
            # Fallback to current directory or temp
            project_dir = os.getcwd()

        # Migration from hidden .kisidian
        old_kisidian = os.path.join(project_dir, ".kisidian")
        new_kisidian = os.path.join(project_dir, "kisidian")
        if os.path.exists(old_kisidian) and not os.path.exists(new_kisidian):
            try:
                os.rename(old_kisidian, new_kisidian)
            except:
                pass

        self.frame = LivePreviewFrame(project_dir=project_dir)
        self.frame.Show()

