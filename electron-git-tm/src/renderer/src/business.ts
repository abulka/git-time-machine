import { globals } from '@renderer/globals'
import { BranchOption } from './types/BranchOption'
import { Commit } from '../../shared/Commit'
import { watch } from 'vue'

// Repo

window.electronAPI.repoChanged((_event, repoDir: string) => {
  // Listen for the 'repoChanged' message from the main process
  // when when cwd changes, and call the 'getBranches' function when received
  globals.repoRefreshNeeded = true
  globals.repoDir = repoDir
  globals.selectedCommitRows = []
  globals.selectedBranchOption = { id: 9999, label: '', value: '' }
  document.title = `Git Time Machine - ${globals.repoDirName}`
  globals.loadingMsg = `LOADING ${globals.repoDir}...`
  getBranches()
})

// Branches

export async function getBranches(): Promise<void> {
  globals.repoRefreshNeeded = true
  globals.loadingMsg = `LOADING ${globals.repoDir}...`

  const _branches = await window.electron.ipcRenderer.invoke('get-branches')

  if (_branches.length === 0) {
    globals.loadingMsg = 'Not a Repo dir'
    return
  }
  globals.branches = _branches.map((branch, index) => {
    const branchLabel = branch
    if (branch.startsWith('* ')) {
      branch = branch.substring(2)
      const branchOption: BranchOption = { id: index, label: branchLabel, value: branch }
      globals.selectedBranchOption = branchOption
    }
    return {
      id: index,
      label: branchLabel,
      value: branch
    }
  })
}

// Commits

function shortenDateString(dateString): string {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

function shortenSha(sha): string {
  return sha.substring(0, 7)
}

export async function getCommits(): Promise<void> {
  const branch = globals.selectedBranch
  const commits = await window.electron.ipcRenderer.invoke('get-commits', branch)
  const commitsFormatted: Commit[] = commits.map((commit, index) => {
    const _commit: Commit = {
      id: index,
      sha: shortenSha(commit.sha),
      comment: commit.comment,
      date: shortenDateString(commit.date),
      author: commit.author
    }
    return _commit
  })
  globals.commitsData = commitsFormatted
}

// Diff

watch([(): string => globals.selectedCommit], async () => {
  if (globals.selectedCommit == undefined) return
  getDiff()
})

// Need to get diffs when globals.selectedCommitRows changes

export async function getDiff(): Promise<void> {
  console.log('getting diff...', globals.selectedCommit)
  const commit: Commit = globals.selectedCommitRows[0]
  if (!commit) {
    return
  }
  const sha = commit.sha
  globals.diffHtml = await window.electron.ipcRenderer.invoke('generate-diff', sha)
  globals.loadingMsg = ''
  globals.repoRefreshNeeded = false
}
