import subprocess
import wx

class GitViewer(wx.Frame):
    def __init__(self):
        super().__init__(parent=None, title='Git Viewer')
        
        # Initialize variables
        self.commit_hashes = []
        self.filename = ''
        self.index = 0
        
        # Create UI elements
        panel = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)
        
        # Filename label and text input
        filename_label = wx.StaticText(panel, label='Enter filename:')
        vbox.Add(filename_label, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=10)
        self.filename_text = wx.TextCtrl(panel)
        vbox.Add(self.filename_text, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        
        # Button to load commit hashes and display file contents
        load_button = wx.Button(panel, label='Load')
        load_button.Bind(wx.EVT_BUTTON, self.on_load)
        vbox.Add(load_button, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        
        # Text display to show current commit hash
        self.commit_hash_text = wx.StaticText(panel, label='Commit hash:')
        vbox.Add(self.commit_hash_text, flag=wx.LEFT|wx.TOP|wx.BOTTOM, border=10)
        
        # Text display to show file contents
        self.file_text = wx.TextCtrl(panel, style=wx.TE_MULTILINE|wx.TE_READONLY)
        vbox.Add(self.file_text, proportion=1, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        
        # Button to show file contents at previous commit hash
        previous_button = wx.Button(panel, label='Previous')
        previous_button.Bind(wx.EVT_BUTTON, self.on_previous)
        vbox.Add(previous_button, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        
        # Button to show file contents at next commit hash
        next_button = wx.Button(panel, label='Next')
        next_button.Bind(wx.EVT_BUTTON, self.on_next)
        vbox.Add(next_button, flag=wx.EXPAND|wx.LEFT|wx.RIGHT|wx.BOTTOM, border=10)
        
        # Add the main sizer to the panel
        panel.SetSizer(vbox)
        
        # Set the window size and center it on the screen
        self.SetSize(500, 500)
        self.Center()
    
    def on_load(self, event):
        # Get the filename from the text input
        self.filename = self.filename_text.GetValue()
        
        # Get the list of commit hashes
        self.commit_hashes = subprocess.check_output(['git', 'log', '--format=%H']).splitlines()
        
        # Display the contents of the file at the most recent commit hash
        self.index = 0
        self.display_commit()
    
    def on_previous(self, event):
        # Decrement index to move to the previous commit hash
        self.index -= 1
        if self.index < 0:
            # If at the beginning of the list, loop back to end
            self.index = len(self.commit_hashes) - 1
        
        # Display the contents of the file at the current commit hash
        self.display_commit()
    
    def on_next(self, event):
        # Increment index to move to the next commit hash
        self.index += 1
        if self.index == len(self.commit_hashes):
            # If at the end of the list, loop back to beginning
            self.index = 0
        
        # Display the contents of the file at the current commit hash
        self.display_commit()
    
    def display_commit(self):
        # Get the current commit hash
        current_hash = self.commit_hashes[self.index].decode()
        
        # Set the commit hash text display
        self.commit_hash_text.SetLabel(f'Commit hash: {current_hash}')
        
        # Save the current scroll position
        scroll_pos = self.file_text.GetScrollPos(wx.VERTICAL)
        
        # Get the file contents at the current commit hash
        file_contents = subprocess.check_output(['git', 'show', f'{current_hash}:{self.filename}']).decode()
        
        # Set the file text display without changing the scroll value
        self.file_text.Freeze()
        self.file_text.SetValue(file_contents)
        self.file_text.ScrollLines(scroll_pos)
        self.file_text.Thaw()



if __name__ == '__main__':
    app = wx.App()
    frame = GitViewer()
    frame.Show()
    app.MainLoop()


       
