import subprocess

# Get the list of commit hashes
commit_hashes = subprocess.check_output(['git', 'log', '--format=%H']).splitlines()

# Prompt for a filename
filename = input('Enter filename: ')

# Initialize index to 0
index = 0

# Loop until user quits
while True:
    # Get the current commit hash
    current_hash = commit_hashes[index].decode()

    # Display the contents of the file at the current commit hash
    subprocess.run(['git', 'show', f'{current_hash}:{filename}'])

    # Ask if user wants to see the same file at the next commit hash
    answer = input('Do you want to see the same file at the next commit hash? (y/n) ')
    if answer.lower() == 'y':
        # Increment index if user wants to see next commit hash
        index += 1
        if index == len(commit_hashes):
            # If at the end of the list, loop back to beginning
            index = 0
    else:
        # Break the loop if user doesn't want to see next commit hash
        break
