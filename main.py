import json
import os
import re
import sys
import wx
import subprocess
import wx.lib.newevent
import wx.html # old, doesn't support css and javascript
import wx.html2 # modern supports css and javascript
from wx.lib.splitter import MultiSplitterWindow
from pubsub import pub  # pip install pypubsub
from difflib import HtmlDiff

class Commit:
    def __init__(self, sha, date, author, comment):
        self.sha = sha
        self.date = date
        self.author = author
        self.comment = comment

current_repo_path = os.getcwd()
current_branch = 'main'
current_commit = 'HEAD'
previous_commit = 'HEAD'
scroll_pos = 0

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

        # bind the selection event to a method
        self.Bind(wx.EVT_LISTBOX, self.on_branch_selected, self.branches_list)
        
        # subscribe to 'repo-changed' message
        pub.subscribe(self.rebuild_branches, 'repo-changed')

        self.rebuild_branches()
        
        # set the panel sizer
        self.SetSizer(sizer)
    
    def rebuild_branches(self):
        # get the list of branches using the git command
        git_command = ['git', 'branch']
        branches = subprocess.check_output(git_command, universal_newlines=True).splitlines()
        self.branches_list.Set(branches)
    
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

        # set the selected item to the item with the current commit
        found = False
        for index in range(self.list_ctrl.GetItemCount()):
            if self.list_ctrl.GetItemText(index) == current_commit:
                self.list_ctrl.Select(index)
                self.list_ctrl.Focus(index)
                found = True
                break
        if not found:
            # set the selected item to the first
            self.list_ctrl.Select(0)
            self.list_ctrl.Focus(0)

    def on_commit_selected(self, event):
        # Update the global variable current_commit with the SHA of the selected commit
        selected_item = self.list_ctrl.GetFirstSelected()
        if selected_item != -1:
            global current_commit, previous_commit
            previous_commit = current_commit
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

        self.rebuild_tree()

    def rebuild_tree(self):
        # remember the selected item, if any
        item = self.tree.GetSelection() # Could be None
        item_text = ''
        if item:
            item_text = self.tree.GetItemText(item)

        # remember the expanded items
        expanded_items = []
        def get_expanded_items(item):
            if self.tree.IsExpanded(item):
                expanded_items.append(self.tree.GetItemText(item))
                child, cookie = self.tree.GetFirstChild(item)
                while child:
                    get_expanded_items(child)
                    child, cookie = self.tree.GetNextChild(item, cookie)
        if self.tree.GetCount():
            get_expanded_items(self.tree.GetRootItem())        

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

        # Expand the items that were expanded before
        def expand_items(item):
            if item != self.tree.GetRootItem() and self.tree.GetItemText(item) in expanded_items:
                self.tree.Expand(item)
            child, cookie = self.tree.GetFirstChild(item)
            while child:
                expand_items(child)
                child, cookie = self.tree.GetNextChild(item, cookie)

        if expanded_items:
            expand_items(self.tree.GetRootItem())
        else:
            # self.tree.ExpandAll()
            self.tree.CollapseAll()



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
        pub.sendMessage('file_selected', path=path, contents=contents)

    def get_file_contents(self, commit, file_path):
        # get the git command to get the contents of the file at the given commit
        command = ['git', 'show', f'{commit}:{file_path}']
        # run the command and return the output
        return subprocess.check_output(command).decode()

class FileContentsPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)

        pub.subscribe(self.on_file_selected, 'file_selected')

        # Create an html window to display the file contents
        self.html = wx.html2.WebView.New(self)

        # set background color to dark gray
        dark_grey = wx.Colour(47, 47, 47)
        self.html.SetBackgroundColour(dark_grey)

        # Use a box sizer to layout the html window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.html, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()
        
        self.html.Bind(wx.html2.EVT_WEBVIEW_NAVIGATED, self.on_page_navigated)
        self.html.Bind(wx.html2.EVT_WEBVIEW_LOADED, self.on_page_loaded)
        self.html.Bind(wx.html2.EVT_WEBVIEW_ERROR, self.on_page_error) # only seems to work for loadURL pages

        # Install message handler with the name wx_msg, this just listens for messages from the page
        # Bind an event handler to receive those messages
        self.html.AddScriptMessageHandler('wx_msg')
        self.html.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self.on_script_message_received)

    def on_file_selected(self, path, contents):
        # Set the HTML content and restore the scroll position
        html_str = self.generate_html(path, contents)
        self.html.SetPage(html_str, "")

    def on_page_navigated(self, event):
        # print("Page navigated")
        event.Skip()

    def on_page_loaded(self, event):
        # print("Page loaded")

        # This works but causes the page to jump from the top to the specified scroll position - yuk
        # so now we embed the scroll position in the html via the 9999 placeholder
        # self.html.RunScript(f"window.scrollTo(0, {scroll_pos})")
        pass

    def on_page_error(self, event):
        print("Page error")
        print(event.GetString())

    def on_script_message_received(self, event):
        global scroll_pos
        # print("Script message received", event.GetString())

        # if first char of message is '{' then it is JSON containing our scroll position
        if event.GetString()[0] == '{':
            scroll_pos_data = json.loads(event.GetString())
            # print("Scroll pos extracted as", scroll_pos_data['scrollPos'])
            scroll_pos = scroll_pos_data['scrollPos']

    def generate_html(self, path, source_file_contents):
        _, file_ext = os.path.splitext(path)
        lang_map = {
            '.html': 'html',
            '.css': 'css',
            '.js': 'javascript',
            '.py': 'python',
            '.java': 'java',
            '.md': 'markdown',
            # Add more mappings for other file types as needed
        }
        lang = lang_map.get(file_ext, 'auto') # Use "auto" if extension is not recognized

        template_path = os.path.join(os.path.dirname(__file__), 'template.html')
        with open(template_path, 'r') as f:
            template = f.read()

        js_file_contents = os.path.join(os.path.dirname(__file__), 'template.js')
        with open(js_file_contents, 'r') as f:
            js_file_contents = f.read()
        js_file_contents = js_file_contents.replace('9999', str(scroll_pos)) # wish there was a nicer way to do this

        # use the template as a f string and substitue the values
        html_str = template.format(lang=lang, source_file_contents=source_file_contents, js_file_contents=js_file_contents)

        # write html to file junk.html
        # with open('junk.html', 'w') as f:
        #     f.write(html_str)

        return html_str


class DiffPanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent, style=wx.SIMPLE_BORDER)

        # Create an html window to display the diff
        self.html = wx.html2.WebView.New(self)

        # Use a box sizer to layout the html window
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.html, proportion=1, flag=wx.EXPAND)
        self.SetSizer(sizer)
        self.Layout()

        pub.subscribe(self.on_show_diff, 'commit_changed')

        self.html.SetPage("diffs go here", "")

    def on_show_diff(self):
        diff = f"{previous_commit} -> {current_commit}"
        # call git to get the diff between the two commits
        diff = self.get_diff(previous_commit, current_commit)
        # wrap in a pre and html
        diff = f"""<html>
        <head>
        <style>
        pre {{
            background-color: #2f2f2f;
            color: #ffffff;
            font-family: monospace;
            white-space: pre-wrap;
            word-wrap: break-word;
        }}
        </style>
        </head>
        <body>
        <pre>{diff}</pre>
        </body>
        </html>
        """


        # Set the HTML content
        self.html.SetPage(diff, "")

    def get_diff(self, previous_commit, current_commit):
        # construct the git command to get the diff between the two commits
        git_command = ['git', 'diff', previous_commit, current_commit]
        
        # call git to get the diff between the two commits
        git_output = subprocess.check_output(git_command)
        
        # decode the output from bytes to a string and return it
        return git_output.decode('utf-8')
        

    # def get_diff(self, previous_commit, current_commit):
    #     # construct the git command to get the diff between the two commits
    #     git_command = ['git', 'diff', previous_commit, current_commit]
        
    #     # call git to get the diff between the two commits
    #     git_output = subprocess.check_output(git_command)
        
    #     # decode the output from bytes to a string
    #     git_output_str = git_output.decode('utf-8')
        
    #     # split the output into lines and process each line individually
    #     lines = git_output_str.split('\n')
    #     diff_lines = []
    #     file_path = ''
    #     for i, line in enumerate(lines):
    #         if line.startswith('diff --git'):
    #             # if the line is the start of a new diff section, extract the filename from it
    #             parts = line.split(' ')
    #             file_path = parts[2][2:]
    #             diff_lines.append(f"--- a/{file_path}\n+++ b/{file_path}\n")
    #         elif line.startswith('-'):
    #             # if the line is a removal, add the filename and line number to the beginning of the line
    #             diff_lines.append(f"-{file_path}:{i}:{line[1:]}\n")
    #         elif line.startswith('+'):
    #             # if the line is an addition, add the filename and line number to the beginning of the line
    #             diff_lines.append(f"+{file_path}:{i}:{line[1:]}\n")
    #         else:
    #             # otherwise, just add the filename and line number to the beginning of the line
    #             diff_lines.append(f" {file_path}:{i}:{line}\n")
        
    #     # join the lines back together and return the result
    #     return ''.join(diff_lines)
        

    # def get_diff(self, previous_commit, current_commit):
    #     # construct the git command to get the diff between the two commits
    #     git_command = ['git', 'diff', previous_commit, current_commit]
        
    #     # call git to get the diff between the two commits
    #     git_output = subprocess.check_output(git_command)
        
    #     # decode the output from bytes to a string
    #     git_output_str = git_output.decode('utf-8')
        
    #     # split the output into lines and process each line individually
    #     lines = git_output_str.split('\n')
    #     diff_lines = []
    #     file_path = ''
    #     for i, line in enumerate(lines):
    #         if line.startswith('diff --git'):
    #             # if the line is the start of a new diff section, extract the filename from it
    #             parts = line.split(' ')
    #             file_path = parts[2][2:]
    #             diff_lines.append(f"--- a/{file_path}\n+++ b/{file_path}\n")
    #         elif line.startswith('-'):
    #             # if the line is a removal, add the filename and line number to the beginning of the line,
    #             # and wrap it in HTML with a red color
    #             diff_lines.append(f'<span style="color:red">-{file_path}:{i}:{line[1:]}</span><br>\n')
    #         elif line.startswith('+'):
    #             # if the line is an addition, add the filename and line number to the beginning of the line,
    #             # and wrap it in HTML with a green color
    #             diff_lines.append(f'<span style="color:green">+{file_path}:{i}:{line[1:]}</span><br>\n')
    #         else:
    #             # otherwise, just add the filename and line number to the beginning of the line,
    #             # and wrap it in HTML
    #             diff_lines.append(f" {file_path}:{i}:{line}<br>\n")
        
    #     # join the lines back together and generate the HTML diff with red and green colors
    #     diff_str = ''.join(diff_lines)
    #     html_diff = HtmlDiff().make_file(git_output_str.splitlines(), diff_str.splitlines(), fromdesc='', todesc='', context=True, numlines=5)
        
    #     # return the HTML diff
    #     return html_diff


    # def get_diff(self, previous_commit, current_commit):
    #     # construct the git command to get the diff between the two commits
    #     git_command = ['git', 'diff', previous_commit, current_commit]
        
    #     # call git to get the diff between the two commits
    #     git_output = subprocess.check_output(git_command)
        
    #     # generate the HTML diff with red and green colors
    #     html_diff = HtmlDiff().make_file(git_output.decode('utf-8').splitlines(), [], fromdesc='', todesc='', context=True, numlines=5)
        
    #     # return the HTML diff
    #     return html_diff


    # def get_diff(self, previous_commit, current_commit):
    #     # Get the diff information using git diff command
    #     diff = subprocess.check_output(['git', 'diff', previous_commit, current_commit])
    #     # Convert the diff bytes to string
    #     diff = diff.decode('utf-8')

    #     # # Create an instance of HtmlDiff
    #     # html_diff = HtmlDiff()
    #     # # Generate the HTML diff information
    #     # # diff_html = html_diff.make_file(fromlines=diff.split('\n'), tolines=[], fromdesc='Previous Commit', todesc='Current Commit', context=True)
    #     # diff_html = html_diff.make_file(fromlines=[], tolines=diff.split('\n'), fromdesc='Previous Commit', todesc='Current Commit', context=True)

    #     # Split the diff information into added and removed lines
    #     added_lines = []
    #     removed_lines = []
    #     for line in diff.split('\n'):
    #         if line.startswith('+'):
    #             added_lines.append(line[1:])
    #         elif line.startswith('-'):
    #             removed_lines.append(line[1:])
    #     # Create an instance of HtmlDiff
    #     html_diff = HtmlDiff()
    #     # Generate the HTML diff information
    #     diff_html = html_diff.make_file(fromlines=removed_lines, tolines=added_lines, fromdesc='Previous Commit', todesc='Current Commit', context=True)

    #     # write to junk.html
    #     with open('junk.html', 'w') as f:
    #         f.write(diff_html)

    #     # Return the HTML diff information
    #     return diff_html


    # def get_diff(self, previous_commit, current_commit, path='main.py'):
    #     import diff_match_patch as dmp_module

    #     # construct the git command to get the file content at the previous commit
    #     git_command = ['git', 'show', '{}:{}'.format(previous_commit, path)]
        
    #     # call git to get the file content at the previous commit
    #     previous_content = subprocess.check_output(git_command).decode('utf-8')
        
    #     # construct the git command to get the file content at the current commit
    #     git_command = ['git', 'show', '{}:{}'.format(current_commit, path)]
        
    #     # call git to get the file content at the current commit
    #     current_content = subprocess.check_output(git_command).decode('utf-8')

    #     dmp = dmp_module.diff_match_patch()
    #     diff = dmp.diff_main(previous_content, current_content)
    #     dmp.diff_cleanupSemantic(diff)
    #     html_diff_span = dmp.diff_prettyHtml(diff)

    #     # wrap span with html
    #     html_diff = f'<html><body>{html_diff_span}</body></html>'



    #     # write html_diff to junk.html
    #     with open('junk.html', 'w') as f:
    #         f.write(html_diff)

    #     return html_diff

        # # generate the HTML diff with red and green colors
        # html_diff = HtmlDiff().make_file(previous_content.splitlines(), current_content.splitlines(), fromdesc='previous', todesc='current', context=True, numlines=5)
        
        # # add CSS to make the diff table responsive
        # html_output = '<!DOCTYPE html>\n<html>\n<head>\n<style>\n.diff { width: 100%; overflow-x: auto; overflow-y: hidden; }\n</style>\n</head>\n<body>\n'
        
        # # add the HTML diff to the output
        # html_output += html_diff
        
        # # close the HTML document
        # html_output += '</body>\n</html>'
        
        # # return the HTML diff with responsive CSS
        # return html_output


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
        super().__init__(parent, title=self.title)
        
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
        file_menu.Append(wx.ID_OPEN, 'Open Git Repo\tCtrl+O', 'Open a git repo')
        self.Bind(wx.EVT_MENU, self.on_open, id=wx.ID_OPEN)


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
        left_area.AppendWindow(DiffPanel(left_area))

        right_area = FileContentsPanel(outer_area)

        # right_area = wx.SplitterWindow(outer_area, -1, style=wx.SP_LIVE_UPDATE|wx.SP_3DSASH)
        # # add FileContentsPanel and DiffPanel vertically in splitter
        # self.file_contents_area = FileContentsPanel(right_area)
        # self.diff_area = DiffPanel(right_area)
        # right_area.SplitVertically(self.file_contents_area, self.diff_area)
        # right_area.SetSashGravity(0.5)
        # right_area.SetSashPosition(300)
        # # right_sizer = wx.BoxSizer(wx.VERTICAL)
        # # right_sizer.Add(right_area, 1, wx.EXPAND)

        outer_area.SplitVertically(left_area, right_area)
        outer_area.SetSashGravity(0.5)

        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(outer_area, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def OnSashChanging(self, event):
        event.Skip()

    def on_quit(self, event):
        self.Close()

    def on_open(self, event):
        global current_repo_path
        path = wx.DirSelector('Select a git repo')
        if path:
            current_repo_path = path
            os.chdir(path)
            self.SetTitle(self.title)
            pub.sendMessage('repo-changed')

    @property
    def title(self):
        return f"Git Repo Time Machine - {current_repo_path}"

if __name__ == '__main__':
    app = wx.App()
    frame = MyFrame(None)
    app.MainLoop()
