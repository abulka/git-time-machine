# Git Time Machine

An app to easily view the state of your git source code directory at any commit incl. contents of any file.

Sure, Git by definition is a 'time machine', and you can get to this information with git log and git show, or even by checking out a commit and looking at your file system etc. but using `Git Time Machine` is a lot easier:

- No need to checkout a commit
- No need to learn arcane git commands e.g. `git show {commit}:{file_path}`

Just select a commit and see the directory tree as it was at that time! Then select a file and you can see the contents of that file (at the time of that commit).  Simply watch a file change as you navigate through the commit history.

![screenshot1](doco/images/screenshot1.png)

## Usage Tip
Click on a commit and then click on a file to see the contents of that file at that commit.

Then up/down arrow keys to navigate through the commits, and watch the file contents change. 🎉

Easily get to old versions of your code which you can paste back into your project - without needing to checkout an old commit or trawl through diffs.

Why vscode git plugins like GitLens don't do this is beyond me.  One cool (paid) app that *does* do this is [Fork](https://fork.dev/).

## Fun Fact 
I started this app using ChatGPT using the following prompt:

> write a python program that runs git commands. it will first get the list of commits hashes and store them in a list. Then it will prompt for a filename. It will then display the contents of the file at the commit with hash, the most recent commit hash. Then it will ask you if you want to see the same file at the next commit hash, etc. till you answer no.

