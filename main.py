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
from util import add_filename_to_link, get_file_contents
from jinja2 import Environment, FileSystemLoader

class Commit:
    def __init__(self, sha, date, author, comment):
        self.sha = sha
        self.date = date
        self.author = author
        self.comment = comment

app_version = '0.1.0'
current_repo_path = os.getcwd()
current_branch = 'main'
current_commit = 'HEAD'
scroll_pos = 0  # window scroll position
scroll_posX = 0  # pre scroll position containg the source code being previewed by prism
scroll_is_for_path = ''  # path of the file being previewed by prism and whose scroll position is being saved
event_debug = False
html_debug = False
show_git_fails_in_msgbox = False

main_path = os.path.dirname(os.path.abspath(__file__))
templates_path = os.path.join(main_path, 'templates')
environment = Environment(loader=FileSystemLoader(templates_path)) # jinja templating

LIGHT_GREEN = "#90EE90"

def get_files_in_repo(commit):
    command = ['git', 'ls-tree', '-r', '--name-only', commit]
    try:
        output = subprocess.check_output(command).decode().strip()
    except subprocess.CalledProcessError as e:
        if show_git_fails_in_msgbox:
            wx.MessageBox(str(e), f'Error calling git', wx.OK | wx.ICON_INFORMATION)
        return []
    return output.splitlines()

def get_commits_for_branch(branch):
    try:
        # Fetch the commit hashes for the specified branch
        command = ['git', 'log', f'{branch}', '--format=%H///%cd///%an///%s']
        try:
            commit_info = subprocess.check_output(command).splitlines()
        except subprocess.CalledProcessError as e:
            if show_git_fails_in_msgbox:
                wx.MessageBox(str(e), f'Error calling git', wx.OK | wx.ICON_INFORMATION)
            return []

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
    # print('commit_info', commit_info)
    match = re.match(r'(?P<date>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2} \+\d{4}) (?P<author>.*) (?P<comment>.*)', commit_info)

    if match:
        # sha = match.group('sha')
        date = match.group('date')
        author = match.group('author')
        comment = match.group('comment')
        # print(f'date: {date}, author: {author}, comment: {comment}')
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

        # set the panel sizer
        self.SetSizer(sizer)
    
    def rebuild_branches(self):
        if event_debug:
            print('   repo-changed ->', 'rebuild_branches')
        
        # get the list of branches using the git command
        git_command = ['git', 'branch']
        try:
            branches = subprocess.check_output(git_command, universal_newlines=True).splitlines()
        except subprocess.CalledProcessError as e:
            if show_git_fails_in_msgbox:
                wx.MessageBox(str(e), f'Error calling git', wx.OK | wx.ICON_INFORMATION)
            return

        self.branches_list.Set(branches)

        if event_debug:
            print('\n⚡️branch_changed (BranchesPanel, rebuild_branches)')
        pub.sendMessage('branch_changed') ## NEW
    
    def on_branch_selected(self, event):
        global current_branch
        current_branch = self.branches_list.GetStringSelection().strip('* ')

        # Publish a message to notify the CommitsPanel that the branch has changed
        if event_debug:
            print('\n⚡️branch_changed (BranchesPanel)')
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

        # Set the sizer for the panel
        self.SetSizer(sizer)

    def rebuild_commits(self):
        if event_debug:
            print('   branch_changed ->', 'rebuild_commits')

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
        # this will trigger the on_commit_selected event
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
            global current_commit
            current_commit = self.list_ctrl.GetItemText(selected_item)

            # Publish a message to notify the FileTreePanel that the commit has changed
            if event_debug:
                print('\n⚡️commit_changed (CommitsPanel, on_commit_selected)')
            pub.sendMessage('commit_changed')

class FileTreePanel(wx.Panel):
    def __init__(self, parent):
        super().__init__(parent)

        # Set panel background color
        # self.SetBackgroundColour(wx.Colour(255, 255, 200))

        # Create a tree control to display the file tree
        self.tree = wx.TreeCtrl(self, style=wx.TR_DEFAULT_STYLE | wx.TR_HIDE_ROOT)

        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_sel_changed)
       
        pub.subscribe(self.rebuild_tree, 'commit_changed')
        pub.subscribe(self.select_treeview_item, 'select_treeview_item')

        # Use a box sizer to layout the controls
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.tree, 1, wx.EXPAND)
        self.SetSizer(sizer)

    def select_treeview_item(self, path):
        if event_debug:
            print('   select_treeview_item ->', 'select_treeview_item')

        # Select the item in the treeview that corresponds to the given path
        # Correctly matches the full path e.g. 'src/main/java/com/example/HelloWorld.java'
        item = self.tree.GetRootItem()
        for part in path.split('/'):
            child, cookie = self.tree.GetFirstChild(item)
            while child:
                if self.tree.GetItemText(child) == part:
                    item = child
                    break
                child, cookie = self.tree.GetNextChild(item, cookie)

        # Avoid raising the event twice by selecting the item without triggering the event
        # Disconnect the event handler
        self.tree.Unbind(wx.EVT_TREE_SEL_CHANGED)
        # Set the item without triggering the event
        self.tree.SelectItem(item)
        # Reconnect the event handler
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_tree_sel_changed)

    def rebuild_tree(self):
        if event_debug:
            print('   commit_changed ->', 'rebuild_tree')
        
        # remember the selected item, if any
        item = self.tree.GetSelection() # Could be None
        item_text = ''
        item_path = ''
        if item and self.tree.GetItemText(item) != 'My Root Item':
            item_text = self.tree.GetItemText(item)
            item_path = [item_text]
            parent = self.tree.GetItemParent(item)
            while parent.IsOk():
                parent_text = self.tree.GetItemText(parent)
                if parent_text != 'My Root Item':
                    item_path.insert(0, parent_text)
                parent = self.tree.GetItemParent(parent)
            item_path = '/'.join(item_path)
            # print('remembering selected item', item_path)
        else:
            # print('no item selected')
            pass 

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

        # restore the selected item, if any
        if item_path:
            item = self.get_item_by_path(item_path)
            if item.IsOk() and self.tree.GetItemText(item) != 'My Root Item':
                self.tree.SelectItem(item)
                # print('restored selection to', item_path)
            else:
                # print('could not restore selection to', item_path)
                pub.sendMessage('file_selected', path=None, contents=None, scroll_to=0) # NEW
        else:
            # print('not restoring anything')
            pub.sendMessage('file_selected', path=None, contents=None, scroll_to=0) # NEW


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

    def get_item_by_path(self, item_path):
        root_item = self.tree.GetRootItem()
        item_parts = item_path.split('/')
        item = root_item
        for part in item_parts:
            child, cookie = self.tree.GetFirstChild(item)
            while child:
                if self.tree.GetItemText(child) == part:
                    item = child
                    break
                child, cookie = self.tree.GetNextChild(item, cookie)
            else:
                return wx.TreeItemId()
        return item

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
            # print('on_tree_sel_changed', path)

            # self.tree.SetItemBackgroundColour(item, wx.Colour(255, 0, 0)) # set the background color to red

        event.Skip()

        # Get the contents of the selected file at the current commit
        contents = get_file_contents(current_commit, path)

        # If file path has changed, scroll_pos will be wrong and needs to be reset to 0
        global scroll_is_for_path, scroll_pos, scroll_posX
        if scroll_is_for_path != path:
            scroll_pos = 0
            scroll_posX = 0
        scroll_is_for_path = path

        if event_debug:
            print('\n⚡️file_selected (FileTreePanel, on_tree_sel_changed)')
        pub.sendMessage('file_selected', path=path, contents=contents, scroll_to=scroll_pos)

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
        self.html.Bind(wx.html2.EVT_WEBVIEW_ERROR, self.on_page_error) # only seems to work for loadURL pages

        # Install message handler with the name wx_msg, this just listens for messages from the page
        # Bind an event handler to receive those messages
        self.html.AddScriptMessageHandler('wx_msg')
        self.html.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self.on_script_message_received)
        
        empty_page = environment.get_template("empty.html")
        html_str = empty_page.render()
        self.html.SetPage(html_str, "")

    def on_file_selected(self, path, contents, scroll_to=None, line_to=None):
        if event_debug:
            print('   file_selected ->', 'on_file_selected')

        # Set the HTML content and restore the scroll position
        if (not path):
            empty_page = environment.get_template("empty.html")
            html_str = empty_page.render()
        else:
            html_str = self.generate_html(path, contents, scroll_to, line_to)
        self.html.SetPage(html_str, "")

    def on_page_navigated(self, event):
        # print("Page navigated")
        event.Skip()

    def on_page_error(self, event):
        print("Page error")
        print(event.GetString())

    def on_script_message_received(self, event):
        global scroll_pos, scroll_posX
        # print("Script message received", event.GetString())

        # if first char of message is '{' then it is JSON containing our scroll position
        if event.GetString()[0] == '{':
            scroll_pos_data = json.loads(event.GetString())
            scroll_pos = scroll_pos_data.get('scrollPos', scroll_pos) # if key not found, use previous value
            scroll_posX = scroll_pos_data.get('scrollPosX', scroll_posX) # if key not found, use previous value

    def generate_html(self, path, source_file_contents, scroll_to=None, line_to=None):
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

        js_file_template = environment.get_template("template.jinja-js")
        js_file_contents = js_file_template.render(scroll_to=scroll_to, scroll_to_x=scroll_posX, line_to=line_to)

        template = environment.get_template("template.html")
        html_str = template.render(lang=lang, source_file_contents=source_file_contents, js_file_contents=js_file_contents)

        if html_debug:
            with open('junk-content.html', 'w') as f:
                f.write(html_str)

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

        self.html.AddScriptMessageHandler('wx_msg')
        self.html.Bind(wx.html2.EVT_WEBVIEW_SCRIPT_MESSAGE_RECEIVED, self.on_script_message_received)

        pub.subscribe(self.generate_html_diff, 'commit_changed')

        self.html.SetPage("diffs go here", "")

    def on_script_message_received(self, event):
        # print("Script message received (Diff Panel)", event.GetString())
        if event.GetString()[0] == '{':
            command_obj = json.loads(event.GetString())
            if command_obj['command'] == 'jump_to_file':
                filePath = command_obj['filePath']
                lineNum = command_obj['lineNum']
                # print("Jump to file command received", filePath, lineNum)

                # Load the file contents into the content view and jump to the specified line
                contents = get_file_contents(current_commit, filePath)

                if event_debug:
                    print('\n⚡️file_selected (DiffPanel, jump_to_file)')
                pub.sendMessage('file_selected', path=filePath, contents=contents, line_to=lineNum)

                # Tell the treeview to select the item
                if event_debug:
                    print('\n⚡️select_treeview_item (DiffPanel, jump_to_file)')
                pub.sendMessage('select_treeview_item', path=filePath)


    def get_previous_commit(self, current_commit):
        # construct the git command to get the previous commit in history
        git_command = ['git', 'rev-list', current_commit]

        # call git to get the list of commits
        try:
            git_output = subprocess.check_output(git_command)
        except subprocess.CalledProcessError as e:
            if show_git_fails_in_msgbox:
                wx.MessageBox(str(e), f'Error calling git', wx.OK | wx.ICON_INFORMATION)
            return None

        # decode the output from bytes to a string and split it into a list of commits
        commits = git_output.decode('utf-8').splitlines()

        # return the previous commit in the list (i.e., the commit before current_commit)
        if len(commits) > 1:
            return commits[1]
        elif len(commits) == 1:
            return None
        else:
            raise Exception("No commits found in repository")
    
    def generate_html_diff(self):
        if event_debug:
            print('   commit_changed ->', 'on_show_diff')
        # call git to find the sha of the previous commit to current_commit sha
        previous_commit = self.get_previous_commit(current_commit)

        # call git to get the diff between the two commits
        diff_body = self.get_diff(previous_commit, current_commit)

        hyperlinks = self.extract_hyperlinks(diff_body)
        diff_body = self.inject_hyperlinks(diff_body, hyperlinks)

        toc_template = environment.get_template("links-diff.html")
        toc_links = toc_template.render(hyperlinks=hyperlinks, add_filename_to_link=add_filename_to_link)

        js_file_contents = environment.get_template("template-diff.js").render()
        
        html_template = environment.get_template("template-diff.html")
        html_str = html_template.render(toc_links=toc_links, diff_body=diff_body, js=js_file_contents)

        if html_debug:
            with open('junk-diff.html', 'w') as f:
                f.write(html_str)

        # Set the HTML content
        self.html.SetPage(html_str, "")

    def extract_hyperlinks(self, diff_output):
        # Initialize variables to hold filename and line numbers
        filename = None
        start_line = None
        end_line = None
        hyperinks = []

        # Define regular expressions to match lines of interest
        filename_regex = r'^diff --git a/(.+?) b/\1'
        line_numbers_regex = r'^@@ -(\d+),(\d+) \+(\d+),(\d+) @@'
        
        # Loop over the lines of the diff output
        for line in diff_output.split('\n'):
            # Check if the line contains a filename
            match = re.match(filename_regex, line)
            if match:
                # Extract the filename from the match object
                filename = match.group(1)
            
            # Check if the line contains line numbers
            match = re.match(line_numbers_regex, line)
            if match:
                whole_line = match.group(0)

                # Extract the line numbers from the match object
                start_line = int(match.group(3))
                end_line = start_line + int(match.group(4))
                
                # Construct the hyperlink and print it
                hyperlink = f'<a href="javascript:jumpTo(\'{filename}\', {abs(start_line)})">{whole_line}</a>'
                hyperinks.append(hyperlink)
        return hyperinks

    def inject_hyperlinks(self, diff, hyperlinks):
        for hyperlink in hyperlinks:
            hyperlink_new = hyperlink.replace('>', ' class="hyperlink-colour">')
            diff = diff.replace(hyperlink.split('>')[1].split('<')[0], hyperlink_new)
        return diff
    
    def get_diff(self, previous_commit, current_commit):
        # construct the git command to get the diff between the two commits
        git_command = ['git', 'diff', previous_commit, current_commit]
        
        # call git to get the diff between the two commits
        try:
            git_output = subprocess.check_output(git_command)
        except subprocess.CalledProcessError as e:
            if show_git_fails_in_msgbox:
                wx.MessageBox(str(e), f'Error calling git', wx.OK | wx.ICON_INFORMATION)
            return ''        
        
        # decode the output from bytes to a string
        git_output = git_output.decode('utf-8')

        # add span tags for highlighting "-" and "+" lines
        highlighted_lines = []
        template_coloured = environment.from_string('<span style="color:{{text_colour}}">{{line | escape}}</span>')
        template_untouched = environment.from_string('{{line | escape}}')
        for line in git_output.split("\n"):
            if len(line) >= 1 and line[0] in ['+', '-']:
                if len(line) > 1 and line[1] in ['+', '-']:
                    highlighted_lines.append(template_untouched.render(line=line))
                else:
                    text_colour = LIGHT_GREEN if line[0] == "+" else "red"
                    highlighted_lines.append(template_coloured.render(line=line, text_colour=text_colour))
            else:
                highlighted_lines.append(template_untouched.render(line=line))

        # join the lines back into a string with newline separators
        git_output = "\n".join(highlighted_lines)

        # return the diff with highlighted lines
        return " ".join(git_command) + '\n\n' + git_output

class MyFrame(wx.Frame):
    def __init__(self, parent):
        super().__init__(parent, title=self.title)
        
        # env_vars = os.environ
        # with open('env_vars.txt', 'w') as file:
        #     for var in sorted(env_vars):
        #         file.write(var + ' : ' + env_vars[var] + '\n')

        # Set the size of the frame
        self.SetSize(wx.Size(1200, 700))
        self.Centre(wx.BOTH)

        # Create a menu bar
        self.menu_bar = menu_bar = wx.MenuBar()

        # Create a file menu
        file_menu = wx.Menu()
        file_menu.Append(wx.ID_EXIT, 'Quit\tCtrl+Q', 'Quit the application')
        self.Bind(wx.EVT_MENU, self.on_quit, id=wx.ID_EXIT)
        self.Bind(wx.EVT_MENU, self.on_quit, id=wx.ID_CLOSE)
        menu_bar.Append(file_menu, 'File')
        file_menu.Append(wx.ID_OPEN, 'Open Git Repo\tCtrl+O', 'Open a git repo')
        self.Bind(wx.EVT_MENU, self.on_open, id=wx.ID_OPEN)

        # add menu items to the view menu called refresh commits and refresh branches
        view_menu = wx.Menu()
        view_menu.Append(wx.ID_REFRESH, 'Refresh Commits\tCtrl+R', 'Refresh the commits')
        self.Bind(wx.EVT_MENU, self.on_refresh_commits, id=wx.ID_REFRESH)
        view_menu.Append(wx.ID_REFRESH, 'Refresh Branches\tCtrl+B', 'Refresh the branches')
        self.Bind(wx.EVT_MENU, self.on_refresh_branches, id=wx.ID_REFRESH)
        menu_bar.Append(view_menu, 'View')

        # add a help menu with a menu item called about
        help_menu = wx.Menu()
        help_menu.Append(wx.ID_ABOUT, 'About Git Time Machine\tCtrl+A', 'About the application')
        self.Bind(wx.EVT_MENU, self.on_about, id=wx.ID_ABOUT)
        # add menu item to visit the website https://github.com/abulka/git-time-machine 
        help_menu.Append(wx.ID_HELP, 'Visit Website\tCtrl+V', 'Visit the website')
        self.Bind(wx.EVT_MENU, self.on_visit_website, id=wx.ID_HELP)
        menu_bar.Append(help_menu, 'Help')

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
        left_area.AppendWindow(bp:=BranchesPanel(left_area))
        left_area.AppendWindow(cp:=CommitsPanel(left_area))
        left_area.AppendWindow(ftp:=FileTreePanel(left_area))
        left_area.AppendWindow(DiffPanel(left_area))

        # Once all the panels are created, kick-start the population of panels
        if event_debug:
            print('\n⚡️repo-changed (MyFrame, layout_ui)')
        pub.sendMessage('repo-changed')

        right_area = FileContentsPanel(outer_area)

        outer_area.SplitVertically(left_area, right_area)
        outer_area.SetSashGravity(0.6)

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
            if event_debug:
                print('\n⚡️repo-changed (MyFrame, on_open)')
            pub.sendMessage('repo-changed')

    def on_refresh_commits(self, event):
        if event_debug:
            print('\n⚡️repo-changed (MyFrame, on_refresh_commits)')
        pub.sendMessage('repo-changed')

    def on_refresh_branches(self, event):
        if event_debug:
            print('\n⚡️repo-changed (MyFrame, on_refresh_branches)')
        pub.sendMessage('repo-changed')

    def on_about(self, event):
        wx.MessageBox(f'Git Repo Time Machine version {app_version}', 'About Git Repo Time Machine', wx.OK | wx.ICON_INFORMATION)

    def on_visit_website(self, event):
        wx.LaunchDefaultBrowser('https://github.com/abulka/git-time-machine')
                                

    @property
    def title(self):
        return f"Git Repo Time Machine - {current_repo_path}"

def run():
    app = wx.App()
    frame = MyFrame(None)
    app.MainLoop()
    
if __name__ == '__main__':
    run()

