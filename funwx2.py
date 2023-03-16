import os
import subprocess
import wx


# class GitViewer(wx.Frame):
#     def __init__(self):
#         super().__init__(None, title='Git Viewer', size=(800, 600))
        
#         # Initialize the commit index
#         self.index = 0
        
#         # Initialize the commit hash list
#         self.commit_hashes = []
        
#         # Create the UI
#         self.create_ui()
        
#         # Load the files in the repository
#         self.load_files()
        
#         # Display the initial commit
#         self.display_commit()
        
#     def create_ui(self):
#         # Create the main panel
#         panel = wx.Panel(self)
        
#         # Create the file tree on the left
#         self.file_tree = wx.TreeCtrl(panel, style=wx.TR_DEFAULT_STYLE|wx.TR_HIDE_ROOT)
#         self.file_tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_file_selected)
        
#         # Create the commit navigation buttons
#         prev_button = wx.Button(panel, label='Previous')
#         prev_button.Bind(wx.EVT_BUTTON, self.previous_commit)
#         next_button = wx.Button(panel, label='Next')
#         next_button.Bind(wx.EVT_BUTTON, self.next_commit)
        
#         # Create the commit hash display
#         self.commit_hash_text = wx.StaticText(panel)
        
#         # Create the file text display on the right
#         self.file_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
#         self.file_text.Bind(wx.EVT_MOUSEWHEEL, self.on_mouse_wheel)
        
#         # Create the sizer
#         sizer = wx.BoxSizer(wx.HORIZONTAL)
#         left_sizer = wx.BoxSizer(wx.VERTICAL)
#         left_sizer.Add(self.file_tree, 1, wx.EXPAND)
#         right_sizer = wx.BoxSizer(wx.VERTICAL)
#         right_sizer.Add(prev_button, 0, wx.ALL, 5)
#         right_sizer.Add(next_button, 0, wx.ALL, 5)
#         right_sizer.Add(self.commit_hash_text, 0, wx.ALL, 5)
#         right_sizer.Add(self.file_text, 1, wx.EXPAND)
#         sizer.Add(left_sizer, 1, wx.EXPAND)
#         sizer.Add(right_sizer, 2, wx.EXPAND)
        
#         # Set the panel sizer
#         panel.SetSizer(sizer)

class GitViewer(wx.Frame):
    def __init__(self):
        super().__init__(None, title="Git File Tree", size=(800, 600))
        self.repo_path = self.get_repo_path()
        self.current_commit = None
        self.commits = None
        self.files = None
        self.tree = None  # add this line
        self.create_widgets()
        self.load_commits()
        self.load_files()
    
    def create_widgets(self):
        panel = wx.Panel(self)
        hbox = wx.BoxSizer(wx.HORIZONTAL)
        
        # create the file tree on the left
        self.tree = wx.TreeCtrl(panel, wx.ID_ANY, style=wx.TR_DEFAULT_STYLE | wx.TR_FULL_ROW_HIGHLIGHT)
        hbox.Add(self.tree, 1, wx.EXPAND | wx.ALL, 10)
        
        # create the commit and file viewers on the right
        vbox = wx.BoxSizer(wx.VERTICAL)
        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        vbox2 = wx.BoxSizer(wx.VERTICAL)
        
        commit_label = wx.StaticText(panel, label="Commit: ")
        vbox2.Add(commit_label, flag=wx.TOP | wx.LEFT | wx.BOTTOM, border=5)
        
        self.commit_display = wx.StaticText(panel, label="")
        vbox2.Add(self.commit_display, flag=wx.LEFT | wx.BOTTOM, border=5)
        
        file_label = wx.StaticText(panel, label="File: ")
        vbox2.Add(file_label, flag=wx.LEFT | wx.BOTTOM, border=5)
        
        self.file_display = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        vbox2.Add(self.file_display, 1, wx.EXPAND | wx.LEFT | wx.BOTTOM | wx.RIGHT, 5)
        
        hbox2.Add(vbox2, 1, wx.EXPAND)
        vbox.Add(hbox2, 1, wx.EXPAND)
        
        # create the navigation buttons
        hbox3 = wx.BoxSizer(wx.HORIZONTAL)
        self.prev_button = wx.Button(panel, label="Prev")
        hbox3.Add(self.prev_button, flag=wx.LEFT | wx.RIGHT, border=5)
        
        self.next_button = wx.Button(panel, label="Next")
        hbox3.Add(self.next_button, flag=wx.LEFT | wx.RIGHT, border=5)
        
        vbox.Add(hbox3, flag=wx.ALIGN_RIGHT | wx.RIGHT, border=10)
        
        hbox.Add(vbox, 2, wx.EXPAND)
        panel.SetSizer(hbox)
        
        # bind events
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_select)
        self.prev_button.Bind(wx.EVT_BUTTON, self.on_prev_button)
        self.next_button.Bind(wx.EVT_BUTTON, self.on_next_button)
        
        self.Bind(wx.EVT_CLOSE, self.on_close)

    def on_tree_select(self, event):
        item = event.GetItem()
        path = self.tree.GetItemPyData(item)
        if os.path.isfile(path):
            self.current_file = path
            self.load_file(self.current_commit, self.current_file)

    def get_repo_path(self):
        # get the current working directory
        cwd = os.getcwd()

        # loop upwards in the directory tree until we find a .git folder
        while not os.path.exists(os.path.join(cwd, '.git')):
            # move up one level
            cwd = os.path.dirname(cwd)
            
            # if we reach the root directory and still haven't found a .git folder, return None
            if cwd == os.path.dirname(cwd):
                return None
        
        # return the path to the .git folder
        return cwd

    def load_files(self):
        self.tree.DeleteAllItems()
        root = self.tree.AddRoot(self.repo_path)
        for file in self.git_files():
            # split file path into its parts
            parts = file.decode().split('/')
            # start at the root
            current_item = root
            # traverse the tree, adding missing parts
            for part in parts:
                if not part:
                    continue
                child, cookie = self.tree.GetFirstChild(current_item)
                while child:
                    if self.tree.GetItemText(child) == part:
                        current_item = child
                        break
                    child, cookie = self.tree.GetNextChild(current_item, cookie)
                else:
                    current_item = self.tree.AppendItem(current_item, part)
            self.tree.SetPyData(current_item, file)
        self.tree.ExpandAll()

    def git_files(self):
        files = subprocess.check_output(['git', 'ls-tree', '--name-only', '-r', 'HEAD']).splitlines()
        for file in files:
            if file:
                yield file
            
    def on_file_selected(self, event):
        # Get the selected file path
        path = os.path.join(os.getcwd(), self.file_tree.GetItemText(event.GetItem()))
        
        # Display the selected file at the current commit
        self.display_file_at_commit(path, self.commit_hashes[self.index])
        
    def display_file_at_commit(self, commit_hash, path):
        # Get the contents of the file at the specified commit and path
        contents = subprocess.check_output(['git', 'show', '{}:{}'.format(commit_hash, path)]).decode('utf-8')
        # Set the file text display
        self.file_text.ChangeValue(contents)
        
    def display_commit(self):
        # Get the current commit hash
        commit_hash = self.commit_hashes[self.index]
        
        # Set the commit hash display
        self.commit_hash_text.SetLabelText('Commit Hash: {}'.format(commit_hash))
        
        # Refresh the file text display
        self.on_file_selected(wx.TreeEvent())
        
    def previous_commit(self, event):
        # Decrement the commit index
        self.index = max(self.index - 1, 0)
        
        # Display the previous commit
        self.display_commit()
        
    def next_commit(self, event):
        # Increment the commit index
        self.index = min(self.index + 1, len(self.commit_hashes) - 1)
        
        # Display the next commit
        self.display_commit()
        
    def on_mouse_wheel(self, event):
        # Save the current scroll position
        pos = self.file_text.GetScrollPos(wx.VERTICAL)
        
        # Skip the event to prevent changing the scroll position
        event.Skip()
        
        # Restore the saved scroll position
        self.file_text.ScrollLines(pos - self.file_text.GetScrollPos(wx.VERTICAL))
        

if __name__ == '__main__':
    app = wx.App()
    GitViewer().Show()
    app.MainLoop()