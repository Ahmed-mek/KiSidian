import html
import re

import wx
import wx.stc as stc

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


SAMPLE_TEXT = """# Obsidian-like Markdown Editor

A cleaner editor with **live preview**, `inline code`, and a darker interface.

## Features
- Split editor / preview layout
- Obsidian-like dark palette
- Better typography
- Markdown tables
- Code fences
- #tags and [[wikilinks]] styling in preview

> [!note]
> This is a callout block.
> It supports multiple lines.

### Code Example
```python
def greet(name: str) -> str:
    return f"Hello, {name}!"
```

### Table
| Item | Status | Note |
|------|--------|------|
| Editor | Done | STC based |
| Preview | Done | HTML live |
| File tree | Later | optional |

Visit [OpenAI](https://openai.com)
"""


class StyledMarkdownCtrl(stc.StyledTextCtrl):
    """Markdown editor with Obsidian-like dark styling."""

    def __init__(self, parent):
        super().__init__(parent, style=wx.BORDER_NONE)
        self._setup_editor()

    def _setup_editor(self):
        self.SetLexer(stc.STC_LEX_MARKDOWN)
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

        # Margin 1: fold markers
        self.SetProperty("fold", "1")
        self.SetMarginType(1, stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(1, stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(1, True)
        self.SetMarginWidth(1, 18)

        self._apply_theme()
        self._setup_markers()
        self.Bind(stc.EVT_STC_MARGINCLICK, self._on_margin_click)

    def _apply_theme(self):
        default_spec = f"face:JetBrains Mono,Ubuntu Mono,DejaVu Sans Mono,size:11,fore:{EDITOR_FG},back:{EDITOR_BG}"
        self.StyleSetSpec(stc.STC_STYLE_DEFAULT, default_spec)
        self.StyleClearAll()

        self.SetWhitespaceForeground(True, "#3A3F4B")
        self.SetWhitespaceBackground(True, EDITOR_BG)

        self.StyleSetSpec(stc.STC_STYLE_LINENUMBER, f"face:JetBrains Mono,Ubuntu Mono,size:10,fore:{GUTTER_FG},back:{GUTTER_BG}")
        self.StyleSetSpec(stc.STC_STYLE_BRACELIGHT, f"fore:#FFFFFF,back:{LINK},bold")
        self.StyleSetSpec(stc.STC_STYLE_BRACEBAD, f"fore:#FFFFFF,back:{RED},bold")
        self.StyleSetSpec(stc.STC_STYLE_INDENTGUIDE, f"fore:#2C313C,back:{EDITOR_BG}")

        # Markdown styles
        self.StyleSetSpec(stc.STC_MARKDOWN_DEFAULT, f"fore:{EDITOR_FG},back:{EDITOR_BG}")
        self.StyleSetSpec(stc.STC_MARKDOWN_LINE_BEGIN, f"fore:{COMMENT}")
        self.StyleSetSpec(stc.STC_MARKDOWN_STRONG1, f"fore:{YELLOW},bold")
        self.StyleSetSpec(stc.STC_MARKDOWN_STRONG2, f"fore:{YELLOW},bold")
        self.StyleSetSpec(stc.STC_MARKDOWN_EM1, f"fore:{PURPLE},italic")
        self.StyleSetSpec(stc.STC_MARKDOWN_EM2, f"fore:{PURPLE},italic")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER1, f"fore:{PURPLE},bold,size:15")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER2, f"fore:{PURPLE},bold,size:14")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER3, f"fore:{PURPLE},bold,size:13")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER4, f"fore:{PURPLE},bold,size:12")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER5, f"fore:{PURPLE},bold")
        self.StyleSetSpec(stc.STC_MARKDOWN_HEADER6, f"fore:{PURPLE},bold")
        self.StyleSetSpec(stc.STC_MARKDOWN_BLOCKQUOTE, f"fore:{COMMENT},italic")
        self.StyleSetSpec(stc.STC_MARKDOWN_STRIKEOUT, f"fore:{COMMENT}")
        self.StyleSetSpec(stc.STC_MARKDOWN_HRULE, f"fore:{HR_COLOR}")
        self.StyleSetSpec(stc.STC_MARKDOWN_LINK, f"fore:{LINK},underline")
        self.StyleSetSpec(stc.STC_MARKDOWN_CODE, f"fore:{GREEN},back:{INLINE_CODE_BG}")
        self.StyleSetSpec(stc.STC_MARKDOWN_CODE2, f"fore:{GREEN},back:{INLINE_CODE_BG}")
        self.StyleSetSpec(stc.STC_MARKDOWN_CODEBK, f"fore:{GREEN},back:{CODE_BG}")
        self.StyleSetSpec(stc.STC_MARKDOWN_ULIST_ITEM, f"fore:{ORANGE},bold")
        self.StyleSetSpec(stc.STC_MARKDOWN_OLIST_ITEM, f"fore:{ORANGE},bold")

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
        super().__init__(None, title="Obsidian-like Markdown Preview", size=(1280, 760))
        self._preview_timer = None
        self._build_ui()
        self.editor.SetText(SAMPLE_TEXT)
        self._update_preview()
        self.Centre()

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


def main():
    app = wx.App(False)
    frame = LivePreviewFrame()
    frame.Show()
    app.MainLoop()


if __name__ == "__main__":
    main()
