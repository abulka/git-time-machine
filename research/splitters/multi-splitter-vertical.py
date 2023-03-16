import wx
from wx.lib.splitter import MultiSplitterWindow

########################################################################
class SamplePanel(wx.Panel):
    """"""

    #----------------------------------------------------------------------
    def __init__(self, parent, colour):
        """Constructor"""
        wx.Panel.__init__(self, parent)
        self.SetBackgroundColour(colour)
    
########################################################################
class MainFrame(wx.Frame):
    """"""

    #----------------------------------------------------------------------
    def __init__(self):
        """Constructor"""
        wx.Frame.__init__(self, None, title="MultiSplitterWindow Tutorial")
        
        splitter = MultiSplitterWindow(self, style=wx.SP_3DSASH | wx.SP_LIVE_UPDATE)
        splitter.SetOrientation(wx.VERTICAL)
        
        colours = ["pink", "yellow", "sky blue", "Lime Green"]
        for colour in colours:
            panel = SamplePanel(splitter, colour)
            splitter.AppendWindow(panel)
        
        self.Show()
    
#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)
    frame = MainFrame()
    frame.SetSize((500,600))
    app.MainLoop()