<script setup lang="ts">
import { onMounted } from 'vue'
import { globals } from '@renderer/globals'

function branchChanged(value): void {
  console.log('branchChanged', value)
}

async function getBranches(): Promise<void> {
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

// Listen for the 'shouldGetBranches' message from the main process
// when when cwd changes, and call the 'getBranches' function when received
window.electronAPI.shouldGetBranches((_event, repoDir: string) => {
  globals.repoRefreshNeeded = true
  globals.repoDir = repoDir
  globals.selectedCommitRows = []
  document.title = `Git Time Machine - ${globals.repoDirName}`
  globals.loadingMsg = `LOADING ${globals.repoDir}...`
  getBranches()
})

onMounted(() => {
  // I used to call getBranches() here, but it's better to wait for the main process to
  // send the 'shouldGetBranches' message.
  // getBranches()
})

function changeRepo(_event): void {
  window.electron.ipcRenderer.invoke('change-repo')
}
function refreshRepo(_event): void {
  globals.repoRefreshNeeded = true
  globals.loadingMsg = `LOADING ${globals.repoDir}...`
  getBranches()
}
</script>

<template>
  <div class="flex items-center">
    <div class="inline mr-6">Select a repo:</div>
    <q-btn
      flat
      dense
      round
      icon="folder"
      class="q-ml-md"
      title="Select a different repo"
      @click="changeRepo"
    />
    <q-btn
      flat
      dense
      round
      icon="refresh"
      class="q-ml-md"
      title="Refresh repo"
      @click="refreshRepo"
    />
    <div class="ml-auto" style="text-align: right">{{ globals.repoDirName }}</div>
    <div class="ml-auto" style="text-align: right">{{ globals.loadingMsg }}</div>
  </div>
  <div class="flex items-center">
    <div class="inline mr-6">Select a branch:</div>
    <q-select
      id="my-select"
      v-model="globals.selectedBranchOption"
      :options="globals.branches"
      dark
      @update:model-value="branchChanged"
    />
  </div>
</template>
