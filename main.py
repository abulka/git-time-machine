import sys
import wx
import subprocess
import wx.lib.newevent
# from wx.lib.pubsub import pub # deprecated
from pubsub import pub  # pip install pypubsub

# ------------ create a listener ------------------

def listener1(arg1, arg2=None):
    print('Function listener1 received:')
    print('  arg1 =', arg1)
    print('  arg2 =', arg2)

# ------------ register listener ------------------

pub.subscribe(listener1, 'rootTopic')

# ---------------- send a message ------------------

print('Publish something via pubsub')
anObj = dict(a=456, b='abc')
pub.sendMessage('rootTopic', arg1=123, arg2=anObj)


class Commit:
    def __init__(self, sha, date, author, comment):
        self.sha = sha
        self.date = date
        self.author = author
        self.comment = comment

current_commit = 'HEAD'

class FileSelectedEvent(wx.PyCommandEvent):
    def __init__(self, evtType, id, filecontents):
        wx.PyCommandEvent.__init__(self, evtType, id)
        self.filecontents = filecontents

EVT_FILE_SELECTED = wx.NewEventType()
EVT_FILE_SELECTED_CHANGED = wx.PyEventBinder(EVT_FILE_SELECTED, 1)

# RefreshPlantUmlEvent, EVT_REFRESH_PLANTUML_EVENT = wx.lib.newevent.NewEvent()

# SomeNewEvent, EVT_SOME_NEW_EVENT = wx.lib.newevent.NewEvent()
# SomeNewCommandEvent, EVT_SOME_NEW_COMMAND_EVENT = wx.lib.newevent.NewCommandEvent()

def get_files_in_repo(commit):
    command = ['git', 'ls-tree', '-r', '--name-only', commit]
    output = subprocess.check_output(command).decode().strip()
    return output.splitlines()

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

        # Bind the list control selection event to on_commit_selected
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.on_commit_selected)

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

    def on_commit_selected(self, event):
        # Update the global variable current_commit with the SHA of the selected commit
        selected_item = self.list_ctrl.GetFirstSelected()
        if selected_item != -1:
            global current_commit
            current_commit = self.list_ctrl.GetItemText(selected_item)

class FileTreePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Set panel background color
        self.SetBackgroundColour(wx.Colour(255, 255, 200))

        # Create a tree control to display the file tree
        self.tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)

        # Bind the tree control to the EVT_TREE_SEL_CHANGED event
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_sel_changed)
       
        # Bind the custom event to the EVT_FILE_SELECTED_CHANGED event

        # self.Bind(EVT_REFRESH_PLANTUML_EVENT, self.refresh_plantuml_view)
        # self.Bind(EVT_SOME_NEW_EVENT, self.handler)

        # Fetch the file tree for the current commit
        files = get_files_in_repo(current_commit)

        root = self.tree.AddRoot("My Root Item")

        # Add each file in the tree to the tree control
        for file_path in files:
            path_parts = file_path.split('/')
            parent = self.tree.GetRootItem()
            print('parent', parent, self.tree.GetItemText(parent))
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

    def on_tree_sel_changed(self, event):
        # Get the selected file path
        item = event.GetItem()

        item = event.GetItem()
        if item:
            # Get the full path of the selected file
            path = self.tree.GetItemText(item)
            parent = self.tree.GetItemParent(item)
            while parent:
                print(self.tree.GetItemText(parent))
                path = self.tree.GetItemText(parent) + '/' + path
                parent = self.tree.GetItemParent(parent)

            # Remove the root item from the path
            path = path.replace('My Root Item/', '')

            # Do something with the path, e.g. display the file contents
            print(path)
        event.Skip()

        # Get the contents of the selected file at the current commit
        contents = self.get_file_contents(current_commit, path)
        # print(contents)
        pub.sendMessage('EVT_FILE_SELECTED_CHANGED', contents=contents)
        
        # anObj = dict(a=456, b='abc')
        # pub.sendMessage('rootTopic', arg1=123, arg2=anObj)


        # evt = FileSelectedEvent(EVT_FILE_SELECTED, self.GetId(), contents)
        # wx.PostEvent(self, evt)

        # # Display the contents in the file contents panel
        # # Send a custom event to the parent window with the selected file path
        # evt = FileSelectedEvent(EVT_FILE_SELECTED, self.GetId(), contents)
        # print('post event', evt)
        # target = self.GetParent()
        # print('target', target)
        # target_parent = target.GetParent()
        # print('target_parent', target_parent)
        # target_parent_parent = target_parent.GetParent()
        # print('target_parent_parent', target_parent_parent)
        # # ensure target_parent_parent is type wx.Frame
        # if isinstance(target_parent_parent, wx.Frame):
        #     print('is wx.Frame, OK')
        # else:
        #     print('not wx.Frame, ERROR')

        # # wx.PostEvent(target_parent_parent, evt)
        # wx.PostEvent(self, evt)
        # wx.PostEvent(target_parent_parent, RefreshPlantUmlEvent())
        # # Create the event
        # evt = SomeNewEvent(attr1="hello", attr2=654)
        # # Post the event
        # wx.PostEvent(target_parent_parent, evt)
        # wx.PostEvent(self, evt)

        # handler = self.GetParent().GetEventHandler()
        # # if wx.EvtHandler.GetEventHandler().HasEventHandlerFor(EVT_FILE_SELECTED):
        # if target_parent_parent.GetEventHandler().HasEventHandlerFor(EVT_FILE_SELECTED):
        # # if target_parent_parent.HasEventHandlers(EVT_FILE_SELECTED):
        #     print("Handler is registered")
        # else:
        #     print("Handler is not registered")

    def get_file_contents(self, commit, file_path):
        # get the git command to get the contents of the file at the given commit
        command = ['git', 'show', f'{commit}:{file_path}']
        # run the command and return the output
        return subprocess.check_output(command).decode()

    def on_file_selected(self, event):
        print('on_file_selected: got event', event)
        file_contents = event.filecontents

        # Display the contents of the selected file in the FileContentsPanel
        # (assuming the parent window has a reference to the FileContentsPanel)
        print('self.GetParent().file_contents_panel', self.GetParent().file_contents_panel)
        self.GetParent().file_contents_panel.display_file_contents(file_contents)

    # def refresh_plantuml_view(self, event):
    #     print('refresh_plantuml_view: got event', event)

    # def handler(self, evt):
    #     # Given the above constructed event, the following is true
    #     print(evt.attr1 == "hello")
    #     print(evt.attr2 == 654)

class FileContentsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)

        self.Bind(EVT_FILE_SELECTED_CHANGED, self.on_file_selected)
        pub.subscribe(self.on_file_selected, 'EVT_FILE_SELECTED_CHANGED')

        # Set the background color to red
        self.SetBackgroundColour(wx.RED)

        # Create a text control to display the file contents
        self.text_ctrl = wx.TextCtrl(self, style=wx.TE_MULTILINE | wx.TE_READONLY)

        # Use a box sizer to layout the text control
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.text_ctrl, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

    def on_file_selected(self, contents):
        print('on_file_selected: got event')
        file_contents = contents

        # Set the file text display without changing the scroll value
        self.text_ctrl.Freeze()
        self.text_ctrl.SetValue(file_contents)
        self.text_ctrl.Thaw()


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
        
        # Set the size of the frame
        self.SetSize(wx.Size(1000, 600))

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
