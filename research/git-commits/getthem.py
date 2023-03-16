import subprocess
import re

branch = 'main'

# Fetch the commit hashes for the specified branch
command = ['git', 'log', f'{branch}', '--format=%H///%cd///%an///%s']
commit_info = subprocess.check_output(command).splitlines()

commits = []
for info in commit_info:
    # split on '///' and get the sha, date, author, and comment
    sha, date, author, comment = info.decode('utf-8').split('///')
    # append dictionary to list
    commits.append({'sha': sha, 'date': date, 'author': author, 'comment': comment})

print(commits)