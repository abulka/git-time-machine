import wx
import subprocess

class Commit:
    def __init__(self, sha, date, author, comment):
        self.sha = sha
        self.date = date
        self.author = author
        self.comment = comment

def get_commits_for_branch(branch):
    try:
        # Fetch the commit hashes for the specified branch
        command = ['git', 'log', f'{branch}', '--format=%H']
        commit_hashes = subprocess.check_output(command).splitlines()

        # Fetch the commit information for each hash
        commits = []
        for commit_hash in commit_hashes:
            command = ['git', 'log', f'{commit_hash.decode()}', '-n', '1', '--pretty=format:%ci %cn %s']
            output = subprocess.check_output(command).decode().strip()
            date, author, comment = output.split(' ', 2)
            commits.append(Commit(commit_hash.decode(), date, author, comment))

        return commits

    except subprocess.CalledProcessError:
        # Handle Git errors by returning an empty list
        print(f"Error fetching commits for branch '{branch}'")
        return []


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
        
        # Create the UI elements for the Commits panel
        title = wx.StaticText(self, label="Commits")
        commit_list = wx.ListBox(self)
        
        # Fetch the list of commits for the current branch
        # (Assuming you have some function or library that can do this)
        commits = get_commits_for_branch("main")  # Replace "master" with current branch name
        
        # Add the commit information to the commit list
        for commit in commits:
            commit_str = f"{commit.sha} - {commit.date} - {commit.author} - {commit.comment}"
            commit_list.Append(commit_str)
        
        # Add the UI elements to the Commits panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(title, flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)
        sizer.Add(commit_list, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        self.SetSizer(sizer)



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
