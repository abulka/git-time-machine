import wx

class MyFrame(wx.Frame):
    def __init__(self, parent):
        wx.Frame.__init__(self, parent, -1, "Splitter Example")
        splitterWindow = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        leftP = wx.Panel(splitterWindow, -1)
        leftP.SetBackgroundColour(wx.BLUE)
        rightP = wx.Panel(splitterWindow, -1)
        rightP.SetBackgroundColour(wx.GREEN)
        splitterWindow.SplitVertically(leftP, rightP, 200)
        splitterWindow.SetSashPosition(200, True)
        splitterWindow.Bind(wx.EVT_SPLITTER_SASH_POS_CHANGING, self.OnSashChanging)

    def OnSashChanging(self, event):
        event.Skip()

app = wx.App()
frame = MyFrame(None)
frame.Show(True)
app.MainLoop()
