import wx

class MyFrame(wx.Frame):
    def __init__(self, parent, title):
        super().__init__(parent, title=title)

        # Create the tree control
        self.tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE)

        """
        WXPYTHON BUG REPORT:
        https://github.com/wxWidgets/Phoenix/issues/2366 
        wx.TreeCtrl has a bug where the colour of the selected item when the control
        loses focus is white text on a light grey background. This is a problem for visibility.
        changing the background or foreground colours of the control does not help.
        """
        # self.tree.SetBackgroundColour(wx.LIGHT_GREY)
        # self.tree.SetBackgroundColour(wx.BLUE)
        # self.tree.SetForegroundColour(wx.BLACK)

        # Add some items to the tree
        root = self.tree.AddRoot("Root")
        item1 = self.tree.AppendItem(root, "Item 1")
        item2 = self.tree.AppendItem(root, "Item 2")
        self.tree.AppendItem(item1, "Subitem 1")
        self.tree.AppendItem(item1, "Subitem 2")

        # Create the text input control
        self.text = wx.TextCtrl(self)

        # Add the tree and text controls to a sizer
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.EXPAND|wx.ALL, 10)
        sizer.Add(self.text, 0, wx.EXPAND|wx.ALL, 10)

        # Set the sizer for the frame
        self.SetSizer(sizer)

        # Show the frame
        self.Show()

app = wx.App()
frame = MyFrame(None, title="My App")
app.MainLoop()
