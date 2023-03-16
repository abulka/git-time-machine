import wx

class MyApp(wx.App):
    def OnInit(self):
        # Create a frame
        self.frame = MyFrame(None, title='Shortcut Test')
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Create a menu bar
        menu_bar = wx.MenuBar()

        # Create a file menu
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit the application')
        self.Bind(wx.EVT_MENU, self.on_quit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_quit, id=wx.ID_CLOSE)
        menu_bar.Append(file_menu, 'File')

        # Set the menu bar
        self.SetMenuBar(menu_bar)

        # Register the keyboard shortcut
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CTRL, ord('Q'), wx.ID_EXIT)])
        self.SetAcceleratorTable(accel_tbl)

        # Create a panel
        panel = wx.Panel(self)

        # Create a label
        label = wx.StaticText(panel, label='Press Cmd+Q to quit')

        # Add the label to the panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(label, 0, wx.ALL, 10)
        panel.SetSizer(sizer)

    def on_quit(self, event):
        self.Close()

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
