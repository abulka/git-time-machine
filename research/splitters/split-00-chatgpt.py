import wx

class MyPanelBase(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)
        self.splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        self.red_panel = wx.Panel(self.splitter)
        self.red_panel.SetBackgroundColour(wx.RED)
        self.blue_panel = wx.Panel(self.splitter)
        self.blue_panel.SetBackgroundColour(wx.BLUE)

        self.splitter.SplitVertically(self.red_panel, self.blue_panel)

        # set the initial splitter position to be halfway
        # self.splitter.SetSashPosition(int(self.GetSize().GetWidth() / 2))
        print(int(self.GetSize().GetWidth() / 2), self.GetSize().GetWidth()) # too small!
        self.splitter.SetSashPosition(200)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.splitter, 1, wx.EXPAND)
        self.SetSizer(sizer)

class MyApp(wx.App):
    def OnInit(self):
        frame = wx.Frame(None, title="MyApp")
        panel = MyPanelBase(frame)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(panel, 1, wx.EXPAND)
        frame.SetSizer(sizer)
        frame.Show(True)
        return True

if __name__ == "__main__":
    app = MyApp(False)
    app.MainLoop()
