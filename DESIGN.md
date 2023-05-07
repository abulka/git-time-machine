# Git Time Machine - Design Notes

# Testing

Scenarios

- Initial boot of app
    - main process sends `repoChanged` to renderer process 
    - BUSINESS-LOGIC: repoChanged 
        - clears selected branch and selected commit
        - sets `globals.repoDir`
        - calls `await getBranches()`
            - populates `globals.branches`
            - sets `selectedBranchOption` and thus `selectedBranch` to branch with '*' in it
        - calls `getCommits()`
            - populates `globals.commits`
    - Commits.vue 
        - table models `globals.commits`
        - 👁️ watches `globals.commits` and selects the 'top-most' commit in the table
        - does not model selected commit, this is done by the user clicking on a commit in the table and the event setting `globals.selectedCommitRows` manually
    - FileTree.vue
        - tree models `globals.selectedTreeNode`
        - 👁️ watches `globals.selectedCommit` and calls `getFiles`
            - which populates `globals.treeData`
    - BUSINESS-LOGIC: 👁️ watches `globals.selectedCommit` and calls `getDiff` which
        - populates `globals.diffHtml` which in turn causes `Diff.vue` to render
        - TODO: could move diff logic back into `Diff.vue` and have it watch `globals.selectedCommit` directly

Questions: 

- How is selectedBranch set?  Via selectedBranchOption
which is set by the user selecting a branch from the dropdown.
When switching repos, selectedBranchOption is set to the current
branch (marked with * in git). When nothing is selected, the value of the Quasar q-select selected model is `undefined`.

- How is selectedCommit set?  Via selectedCommitRows which is set by the user clicking on a commit in the table.  When nothing is selected, the value of the Quasar q-table selected model is `[]`.
