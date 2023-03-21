import re
import subprocess

"""
The function uses a regular expression to extract the filename, starting line
number, and line range from the input link text, and then constructs a new link
text that includes the filename and the original line range. If the input link
text does not match the expected format, the function simply returns the
original link text unchanged.

Here's an example usage of the function:

    link_text = '<a href="javascript:jumpTo(\'main.py\', 434)">@@ -434,6 +434,7 @@</a>'
    new_link_text = add_filename_to_link(link_text)
    print(new_link_text)

This would output:

    <a href="javascript:jumpTo('main.py', 434)">main.py @@ -434,6 +434,7 @@</a>

"""

def add_filename_to_link(link_text):
    match = re.match(r'<a href="javascript:jumpTo\(\'(.+?)\'\s*,\s*(\d+)\)">@@\s*-(\d+),(\d+)\s*\+\d+,\d+\s*@@</a>', link_text)
    if match:
        filename = match.group(1)
        start_line = match.group(3)
        line_range = match.group(4)
        new_link_text = f'<a href="javascript:jumpTo(\'{filename}\', {start_line})">{filename} @@ -{start_line},{line_range} @@</a>'
        return new_link_text
    else:
        return link_text

    
def get_file_contents(commit, file_path):
    # get the git command to get the contents of the file at the given commit
    command = ['git', 'show', f'{commit}:{file_path}']
    # run the command and return the output
    return subprocess.check_output(command).decode()


"""
You can use this function by passing the contents of a source file as a string to the wrap_lines_with_spans() function, like this:

with open("source_file.txt", "r") as source_file:
    source_file_contents = source_file.read()

wrapped_file_contents = wrap_lines_with_spans(source_file_contents)
"""
# def wrap_lines_with_spans(source_file_contents):
#     # Split the source file contents into lines
#     lines = source_file_contents.splitlines()

#     # Create an empty list to hold the wrapped lines
#     wrapped_lines = []

#     # Loop over each line and wrap it with a span tag with a unique ID
#     for i, line in enumerate(lines):
#         wrapped_line = f'<span id="line{i+1}">{line}</span>'
#         wrapped_lines.append(wrapped_line)

#     # Join the wrapped lines back into a single string and return it
#     wrapped_file_contents = '\n'.join(wrapped_lines)
#     return wrapped_file_contents

