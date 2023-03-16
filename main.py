import re
import sys
import wx
import subprocess
import wx.lib.newevent
import wx.html
from wx.lib.splitter import MultiSplitterWindow
from pubsub import pub  # pip install pypubsub

class Commit:
    def __init__(self, sha, date, author, comment):
        self.sha = sha
        self.date = date
        self.author = author
        self.comment = comment

current_branch = 'main'
current_commit = 'HEAD'

def get_files_in_repo(commit):
    command = ['git', 'ls-tree', '-r', '--name-only', commit]
    output = subprocess.check_output(command).decode().strip()
    return output.splitlines()

def get_commits_for_branch(branch):
    try:
        # Fetch the commit hashes for the specified branch
        command = ['git', 'log', f'{branch}', '--format=%H///%cd///%an///%s']
        commit_info = subprocess.check_output(command).splitlines()

        commits = []
        for info in commit_info:
            # split on '///' and get the sha, date, author, and comment
            sha, date, author, comment = info.decode('utf-8').split('///')
            commits.append(Commit(sha, date, author, comment))
        return commits

    except subprocess.CalledProcessError:
        # Handle Git errors by returning an empty list
        print(f"Error fetching commits for branch '{branch}'")
        return []

def extract_fields(commit_info):
    print('commit_info', commit_info)
    match = re.match(r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \+\d{4}) (?P<author>.*) (?P<comment>.*)', commit_info)

    if match:
        # sha = match.group('sha')
        date = match.group('date')
        author = match.group('author')
        comment = match.group('comment')
        print(f'date: {date}, author: {author}, comment: {comment}')
    else:
        # old dogy technique
        date, author, comment = commit_info.split(' ', 2)

    return date,author,comment

class BranchesPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)
        
        # Set the background color to blue
        # self.SetBackgroundColour(wx.BLUE)
        
        # create a box sizer for the panel
        sizer = wx.BoxSizer(wx.VERTICAL)
        
        # create a listbox to display the branches
        self.branches_list = wx.ListBox(self, wx.ID_ANY, style=wx.LB_SINGLE)
        sizer.Add(self.branches_list, proportion=1, flag=wx.EXPAND|wx.ALL, border=10)
        
        # get the list of branches using the git command
        git_command = ['git', 'branch']
        branches = subprocess.check_output(git_command, universal_newlines=True).splitlines()
        self.branches_list.Set(branches)
        
        # bind the selection event to a method
        self.Bind(wx.EVT_LISTBOX, self.on_branch_selected, self.branches_list)
        
        # set the panel sizer
        self.SetSizer(sizer)
    
    def on_branch_selected(self, event):
        global current_branch
        current_branch = self.branches_list.GetStringSelection().strip('* ')

        # Publish a message to notify the CommitsPanel that the branch has changed
        pub.sendMessage('branch_changed')

class CommitsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Set panel background color
        # self.SetBackgroundColour(wx.Colour(200, 255, 255))

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

        # Bind the list control selection event to on_commit_selected
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_commit_selected)

        pub.subscribe(self.rebuild_commits, 'branch_changed')

        self.rebuild_commits()

        # Set the sizer for the panel
        self.SetSizer(sizer)

    def rebuild_commits(self):
        # Fetch the commits for the current branch
        commits = get_commits_for_branch(current_branch)

        # Clear the list control
        self.list_ctrl.DeleteAllItems()

        # Add the commits to the list control
        for commit in commits:
            index = self.list_ctrl.InsertItem(sys.maxsize, commit.sha)
            self.list_ctrl.SetItem(index, 1, commit.date)
            self.list_ctrl.SetItem(index, 2, commit.author)
            self.list_ctrl.SetItem(index, 3, commit.comment)

    def on_commit_selected(self, event):
        # Update the global variable current_commit with the SHA of the selected commit
        selected_item = self.list_ctrl.GetFirstSelected()
        if selected_item != -1:
            global current_commit
            current_commit = self.list_ctrl.GetItemText(selected_item)

            # Publish a message to notify the FileTreePanel that the commit has changed
            pub.sendMessage('commit_changed')

class FileTreePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Set panel background color
        # self.SetBackgroundColour(wx.Colour(255, 255, 200))

        # Create a tree control to display the file tree
        self.tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)

        # Bind the tree control to the EVT_TREE_SEL_CHANGED event
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_sel_changed)
       
        pub.subscribe(self.rebuild_tree, 'commit_changed')

        # Use a box sizer to layout the controls
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sizer)

        # self.tree.SetBackgroundColour(wx.Colour(0, 0, 0))
        # set to wx red
        # self.tree.SetForegroundColour(wx.RED)
        # Set the color of the focus item when the tree widget loses focus to grey
        # self.tree.SetItemTextColour(self.tree.GetSelection(), wx.Colour(128, 128, 128))
        # Set the HideSelection property of the treeview to False
        # self.tree.HideSelection = False

        self.rebuild_tree()

    def rebuild_tree(self):
        # remember the selected item, if any
        item = self.tree.GetSelection() # Could be None
        item_text = ''
        if item:
            item_text = self.tree.GetItemText(item)
            
        # Clear the treeview
        self.tree.DeleteAllItems()

        # Fetch the file tree for the current commit
        files = get_files_in_repo(current_commit)

        root = self.tree.AddRoot("My Root Item")

        # Add each file in the tree to the tree control
        for file_path in files:
            path_parts = file_path.split('/')
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

        # Restore the selection, if possible, using self.get_item_by_label
        if item_text:
            item = self.get_item_by_label(self.tree, item_text, root)
            if item.IsOk():
                self.tree.SelectItem(item)

        # Expand the tree to show all items
        self.tree.ExpandAll()

    def get_item_by_label(self, tree, search_text, root_item):
        item, cookie = tree.GetFirstChild (root_item)
        while item.IsOk ():
            text = tree.GetItemText (item)
            if text.lower () == search_text.lower ():
                return item
            if tree.ItemHasChildren (item):
                match = self.get_item_by_label (tree, search_text, item)
                if match.IsOk ():
                    return match
            item, cookie = tree.GetNextChild (root_item, cookie)
        return wx.TreeItemId ()

    def on_tree_sel_changed(self, event):
        # Get the selected file path
        item = event.GetItem()
        if item:
            # Get the full path of the selected file
            path = self.tree.GetItemText(item)
            parent = self.tree.GetItemParent(item)
            while parent:
                path = self.tree.GetItemText(parent) + '/' + path
                parent = self.tree.GetItemParent(parent)

            # Remove the root item from the path
            path = path.replace('My Root Item/', '')

            # self.tree.SetItemBackgroundColour(item, wx.Colour(255, 0, 0)) # set the background color to red

        event.Skip()

        # Get the contents of the selected file at the current commit
        contents = self.get_file_contents(current_commit, path)
        pub.sendMessage('EVT_FILE_SELECTED_CHANGED', contents=contents)

    def get_file_contents(self, commit, file_path):
        # get the git command to get the contents of the file at the given commit
        command = ['git', 'show', f'{commit}:{file_path}']
        # run the command and return the output
        return subprocess.check_output(command).decode()

class FileContentsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)

        pub.subscribe(self.on_file_selected, 'EVT_FILE_SELECTED_CHANGED')

        # Set the background color to red
        # self.SetBackgroundColour(wx.RED)

        # Create an html window to display the file contents
        self.html = wx.html.HtmlWindow(self, style=wx.SIMPLE_BORDER)
        # set background color to dark gray
        dark_grey = wx.Colour(47, 47, 47)
        self.html.SetBackgroundColour(dark_grey)

        # Use a box sizer to layout the html window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.html, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def on_file_selected(self, contents):
        file_contents = contents

        # Get the current scroll position
        scroll_pos = self.html.GetViewStart()[1]

        # add line numbers
        lines = file_contents.split('\n')
        file_contents = ''
        for i, line in enumerate(lines):
            file_contents += f'<font color="silver">{i+1:4}</font> <font color="white" size="4">{line}</font>\n'

        html_str = f"""<html><body bgcolor='dark gray'><pre>{file_contents}</p></pre></html>"""
        self.html.SetPage(html_str)
        print(html_str)

        # Set the scroll position to the same value
        self.html.Scroll(0, scroll_pos)

class LeftPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)

        # Create the CommitsPanel and FileTreePanel sub-panels vertically
        commits_panel = CommitsPanel(self)
        file_tree_panel = FileTreePanel(self)

        # Split the left panel vertically to show the two sub-panels
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(commits_panel, proportion=1, flag=wx.EXPAND)
        sizer.Add(file_tree_panel, proportion=2, flag=wx.EXPAND)
        self.SetSizer(sizer)

class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title="Git Repo Time Machine")
        
        # Set the size of the frame
        self.SetSize(wx.Size(1000, 600))

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
        accel_tbl = wx.AcceleratorTable([(wx.ACCEL_CMD, ord('Q'), wx.ID_EXIT)])
        self.SetAcceleratorTable(accel_tbl)

        self.layout_ui()

        self.Show()

    def layout_ui(self):
        outer_area = wx.SplitterWindow(self, -1, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)

        left_area = MultiSplitterWindow(outer_area, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        left_area.SetOrientation(wx.VERTICAL)
        left_area.AppendWindow(BranchesPanel(left_area))
        left_area.AppendWindow(CommitsPanel(left_area))
        left_area.AppendWindow(FileTreePanel(left_area))

        right_area = FileContentsPanel(outer_area)

        outer_area.SplitVertically(left_area, right_area)
        outer_area.SetSashGravity(0.5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(outer_area, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def OnSashChanging(self, event):
        event.Skip()

    def on_quit(self, event):
        self.Close()

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    app.MainLoop()
