import wx
import wx.lib.agw.fourwaysplitter as fws

########################################################################
class MyFrame(wx.Frame):

    #----------------------------------------------------------------------
    def __init__(self):

        wx.Frame.__init__(self, None, title="FourWaySplitter Example")

        splitter = fws.FourWaySplitter(self, agwStyle=wx.SP_LIVE_UPDATE)

        # Put in some coloured panels...
        for colour in [wx.RED, wx.WHITE, wx.BLUE, wx.GREEN]:

            panel = wx.Panel(splitter)
            panel.SetBackgroundColour(colour)

            splitter.AppendWindow(panel)

#----------------------------------------------------------------------
if __name__ == "__main__":
    app = wx.App(False)

    frame = MyFrame()
    app.SetTopWindow(frame)
    frame.Show()

    app.MainLoop()
    