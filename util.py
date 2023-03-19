import re

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
    match = re.match(r'<a href="javascript:jumpTo\(\'(\w+\.\w+)\'\s*,\s*(\d+)\)">@@\s*-(\d+),(\d+)\s*\+\d+,\d+\s*@@</a>', link_text)
    if match:
        filename = match.group(1)
        start_line = match.group(3)
        line_range = match.group(4)
        new_link_text = f'<a href="javascript:jumpTo(\'{filename}\', {start_line})">{filename} @@ -{start_line},{line_range} @@</a>'
        return new_link_text
    else:
        return link_text
    