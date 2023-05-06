import { globals } from '@renderer/globals'
import { BranchOption } from './types/BranchOption'
import { Commit } from '../../shared/Commit'
import { watch } from 'vue'

// Repo

window.electronAPI.repoChanged(async (_event, repoDir: string) => {
  console.log(`${repoDir} repoChanged}!!!`)
  globals.repoRefreshNeeded = true
  globals.repoDir = repoDir
  globals.selectedCommitRows = []
  globals.selectedBranchOption = undefined // type BranchOption
  document.title = `Git Time Machine - ${globals.repoDirName}`
  globals.loadingMsg = `LOADING ${globals.repoDir}...`
  await getBranches()
  console.log('getBranches() completed')
  await getCommits()
  console.log('getCommits() completed')

})

// Branches

export async function getBranches(): Promise<void> {
  console.log('getBranches()...')
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
