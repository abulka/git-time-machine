import sys
import wx
import subprocess

class Commit:
    def __init__(self, sha, date, author, comment):
        self.sha = sha
        self.date = date
        self.author = author
        self.comment = comment

# wx.EVT_COMMAND_COMMIT_SELECTED = wx.NewEventType()
# wx.EVT_COMMIT_SELECTED = wx.PyEventBinder(wx.EVT_COMMAND_COMMIT_SELECTED.typeId, 1)

# class CommitSelectionEvent(wx.PyCommandEvent):
#     """Custom event to signal when a commit has been selected."""
#     def __init__(self, commit):
#         super().__init__(wx.EVT_COMMAND_COMMIT_SELECTED.typeId)
#         self.commit = commit



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
        super().__init__(parent)

        # Set panel background color
        self.SetBackgroundColour(wx.Colour(200, 255, 255))

        # Create a box sizer to contain the list control
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Create a list control to display the commits
        self.list_ctrl = wx.ListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.InsertColumn(0, "SHA")
        self.list_ctrl.InsertColumn(1, "Date")
        self.list_ctrl.InsertColumn(2, "Author")
        self.list_ctrl.InsertColumn(3, "Comment", width=300)

        # Add the list control to the sizer
        sizer.Add(self.list_ctrl, 1, wx.EXPAND)

        # Fetch the commits for the current branch
        commits = get_commits_for_branch("main")  # Replace "master" with current branch name

        # Add the commits to the list control
        for commit in commits:
            index = self.list_ctrl.InsertItem(sys.maxsize, commit.sha)
            self.list_ctrl.SetItem(index, 1, commit.date)
            self.list_ctrl.SetItem(index, 2, commit.author)
            self.list_ctrl.SetItem(index, 3, commit.comment)

        # Set the sizer for the panel
        self.SetSizer(sizer)


class FileTreePanel(wx.Panel):
    def __init__(self, parent, commit):
        super().__init__(parent)

        # Set panel background color
        self.SetBackgroundColour(wx.Colour(255, 255, 200))

        # Create a tree control to display the file tree
        self.tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)

        # Fetch the file tree for the specified commit
        command = ['git', 'ls-tree', '-r', '--name-only', commit]
        output = subprocess.check_output(command).decode().strip()

        # Add each file in the tree to the tree control
        for line in output.splitlines():
            path_parts = line.split('/')
            parent = self.tree.GetRootItem()
            for part in path_parts[:-1]:
                item, cookie = self.tree.GetFirstChild(parent)
                while item:
                    if self.tree.GetItemText(item) == part:
                        parent = item
                        break
                    item, cookie = self.tree.GetNextChild(parent, cookie)

                else:
                    parent = self.tree.AppendItem(parent, part)

            self.tree.AppendItem(parent, path_parts[-1])

        # Expand the tree to show all items
        self.tree.ExpandAll()

        # Use a box sizer to layout the controls
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sizer)



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
        file_tree_panel = FileTreePanel(self, "main")
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
