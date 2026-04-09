import html

import wx

try:
    import wx.html2 as _html2
except Exception:
    _html2 = None
    import wx.html as _html

try:
    import markdown as _markdown
except Exception:
    _markdown = None

PREVIEW_CSS = """
body {
    font-family: "Ubuntu", "DejaVu Sans", sans-serif;
    background: #0E1116;
    color: #D5D8DD;
    margin: 20px;
    line-height: 1.6;
}
a { color: #6B80CF; }
code, pre {
    font-family: "Ubuntu Mono", "DejaVu Sans Mono", monospace;
    background: #2D2D2D;
    color: #D5D8DD;
}
pre {
    padding: 10px 12px;
    border-radius: 6px;
    overflow-x: auto;
}
"""


class LivePreviewFrame(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Markdown Live Preview", size=(1000, 650))
        self._preview_timer = None
        self._build_ui()
        self._update_preview()
        self.Centre()

    def _build_ui(self):
        panel = wx.Panel(self)
        panel.SetBackgroundColour("#0C1014")

        splitter = wx.SplitterWindow(panel, style=wx.SP_LIVE_UPDATE)
        editor_panel = wx.Panel(splitter)
        preview_panel = wx.Panel(splitter)

        self.editor = wx.TextCtrl(
            editor_panel,
            style=wx.TE_MULTILINE | wx.TE_RICH2
        )
        self.editor.SetBackgroundColour("#0D1017")
        self.editor.SetForegroundColour("#D5D8DD")
        self.editor.Bind(wx.EVT_TEXT, self._on_text_change)

        self.preview = self._make_preview_ctrl(preview_panel)
        self.preview.SetBackgroundColour("#0E1116")

        editor_sizer = wx.BoxSizer(wx.VERTICAL)
        editor_sizer.Add(self.editor, 1, wx.EXPAND)
        editor_panel.SetSizer(editor_sizer)

        preview_sizer = wx.BoxSizer(wx.VERTICAL)
        preview_sizer.Add(self.preview, 1, wx.EXPAND)
        preview_panel.SetSizer(preview_sizer)

        splitter.SplitVertically(editor_panel, preview_panel, sashPosition=500)
        splitter.SetMinimumPaneSize(240)

        main_sizer = wx.BoxSizer(wx.VERTICAL)
        main_sizer.Add(splitter, 1, wx.EXPAND | wx.ALL, 8)
        panel.SetSizer(main_sizer)

    def _make_preview_ctrl(self, parent):
        if _html2 is not None:
            return _html2.WebView.New(parent)
        preview = _html.HtmlWindow(parent)
        preview.SetStandardFonts()
        return preview

    def _render_markdown(self, text):
        if _markdown is None:
            return "<pre>" + html.escape(text) + "</pre>"
        return _markdown.markdown(text, extensions=["fenced_code", "tables"])

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
            "</head>"
            "<body bgcolor='#0E1116' text='#D5D8DD'>"
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
