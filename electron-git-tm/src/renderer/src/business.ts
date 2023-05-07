import { globals } from '@renderer/globals'
import { BranchOption } from './types/BranchOption'
import { Commit } from '../../shared/Commit'

// Repo

window.electronAPI.repoChanged(async (_event, repoDir: string) => {
  console.log(`${repoDir} repoChanged}!!!`)
  globals.repoDir = repoDir
  await refreshRepo()
})

export async function refreshRepo(): Promise<void> {
  globals.selectedCommitRows = []
  globals.selectedBranchOption = undefined // type BranchOption
  document.title = `Git Time Machine - ${globals.repoDirName}`
  globals.loadingMsg = `LOADING ${globals.repoDir}...`
  await getBranches()
  console.log('getBranches() completed')
  await getCommits()
  console.log('getCommits() completed')
  // don't await getDiff() here, as it will be called by the watcher below
  globals.loadingMsg = ''
}

// Branches

export async function getBranches(): Promise<void> {
  console.log('getBranches()...')
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
  console.log(`getting commits...`)
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
