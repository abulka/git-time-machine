import wx

class BranchesPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        
        # Set the background color to blue
        self.SetBackgroundColour(wx.BLUE)
        
        # TODO: Add code to create the Branches panel UI


class CommitsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        
        # Set the background color to green
        self.SetBackgroundColour(wx.GREEN)
        
        # TODO: Add code to create the Commits panel UI


class FileTreePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        
        # Set the background color to yellow
        self.SetBackgroundColour(wx.YELLOW)
        
        # TODO: Add code to create the FileTree panel UI


class FileContentsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        
        # Set the background color to red
        self.SetBackgroundColour(wx.RED)
        
        # TODO: Add code to create the FileContents panel UI


class LowerPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        
        # Create the FileTreePanel and FileContentsPanel sub-panels
        file_tree_panel = FileTreePanel(self)
        file_contents_panel = FileContentsPanel(self)
        
        # Split the lower panel horizontally to show the two sub-panels
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(file_tree_panel, proportion=1, flag=wx.EXPAND)
        sizer.Add(file_contents_panel, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)

class MainPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        
        # Create the CommitsPanel and LowerPanel sub-panels
        commits_panel = CommitsPanel(self)
        lower_panel = LowerPanel(self)
        
        # Add the sub-panels to the MainPanel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(commits_panel, proportion=1, flag=wx.EXPAND)
        sizer.Add(lower_panel, proportion=2, flag=wx.EXPAND)
        self.SetSizer(sizer)


class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="My App")
        
        # Create the BranchesPanel and MainPanel sub-panels
        branches_panel = BranchesPanel(self)
        main_panel = MainPanel(self)
        
        # Add the sub-panels to the main frame
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(branches_panel, proportion=1, flag=wx.EXPAND)
        sizer.Add(main_panel, proportion=3, flag=wx.EXPAND)
        self.SetSizer(sizer)

        self.Show()


if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    app.MainLoop()
