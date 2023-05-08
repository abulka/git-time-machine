import { globals, debug } from '@renderer/globals'
import { BranchOption } from './types/BranchOption'
import { Commit } from '../../shared/Commit'

// Repo

window.electronAPI.repoChanged(async (_event, repoDir: string) => {
  if (debug.event_flow) console.log(`${repoDir} repoChanged}!!!`)
  globals.repoDir = repoDir
  await refreshRepo()
})

export async function refreshRepo(): Promise<void> {
  globals.selectedCommitRows = []
  globals.selectedBranchOption = undefined // type BranchOption
  document.title = `Git Time Machine - ${globals.repoDirName}`
  globals.isLoading = true
  await getBranches()
  if (debug.event_flow) console.log('getBranches() completed')
  await getCommits()
  if (debug.event_flow) console.log('getCommits() completed')
  // Both treeview and diffview are watching various globals and asyncronously update themselves
  setTimeout(() => {
    globals.isLoading = false
  }, 1000)
}

// Branches

export async function getBranches(): Promise<void> {
  if (debug.event_flow) console.log('getBranches()...')
  const _branches = await window.electron.ipcRenderer.invoke('get-branches')

  if (_branches.length === 0) {
    globals.warningMsg = 'Not a Repo dir'
    globals.treeData = []
    globals.expanded = []
    return
  } else globals.warningMsg = ''
  globals.branches = _branches.map((branch, index) => {
    const branchLabel = branch
    if (branch.startsWith('* ')) {
      branch = branch.substring(2)
      const branchOption: BranchOption = { id: index, label: branchLabel, value: branch }
      globals.selectedBranchOption = branchOption
    }
    // else globals.selectedBranchOption remains undefined
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
  if (debug.event_flow) console.log(`getting commits...`)
  const branch = globals.selectedBranch
  const _commits = await window.electron.ipcRenderer.invoke('get-commits', branch)
  const commitsFormatted: Commit[] = _commits.map((commit, index) => {
    const _commit: Commit = {
      id: index,
      sha: shortenSha(commit.sha),
      comment: commit.comment,
      date: shortenDateString(commit.date),
      author: commit.author
    }
    return _commit
  })
  globals.commits = commitsFormatted
}
