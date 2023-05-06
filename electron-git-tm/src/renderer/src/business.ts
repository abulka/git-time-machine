import { globals } from '@renderer/globals'
import { BranchOption } from './types/BranchOption'

export async function getBranches(): Promise<void> {
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

// Listen for the 'repoChanged' message from the main process
// when when cwd changes, and call the 'getBranches' function when received
window.electronAPI.repoChanged((_event, repoDir: string) => {
  globals.repoRefreshNeeded = true
  globals.repoDir = repoDir
  globals.selectedCommitRows = []
  document.title = `Git Time Machine - ${globals.repoDirName}`
  globals.loadingMsg = `LOADING ${globals.repoDir}...`
  getBranches()
})
