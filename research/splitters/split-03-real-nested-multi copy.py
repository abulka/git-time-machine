import wx
from wx.lib.splitter import MultiSplitterWindow
    
########################################################################
class RandomPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, color):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(color)
    
########################################################################
class MainPanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        
        topSplitter = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        vSplitter = wx.SplitterWindow(topSplitter, -1, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        
        panelOne = RandomPanel(vSplitter, "blue")
        panelTwo = RandomPanel(vSplitter, "red")
        vSplitter.SplitHorizontally(panelOne, panelTwo)
        vSplitter.SetSashGravity(0.5)
        
        # panelThree = RandomPanel(topSplitter, "green")
        panelThree = MultiSplitterWindow(topSplitter, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        panelThree.SetOrientation(wx.VERTICAL)
        colours = ["pink", "yellow", "sky blue", "Lime Green"]
        for colour in colours:
            panel = RandomPanel(panelThree, colour)
            panelThree.AppendWindow(panel)
        

        topSplitter.SplitVertically(panelThree, vSplitter)
        topSplitter.SetSashGravity(0.5)
        
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(topSplitter, 1, wx.EXPAND)
        self.SetSizer(sizer)
        
########################################################################
class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="Nested and Multi Splitters",
                          size=(800,600))
        panel = MainPanel(self)
        self.Show()
        
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    app.MainLoop()