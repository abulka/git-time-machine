import { globals } from '@renderer/globals'

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
      globals.selectedBranchOption = { id: index, label: branchLabel, value: branch }
    }
    return {
      id: index,
      label: branchLabel,
      value: branch
    }
  })
}
