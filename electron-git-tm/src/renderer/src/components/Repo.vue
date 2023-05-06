<script setup lang="ts">
import { globals } from '@renderer/globals'
import { getBranches } from '@renderer/business'

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
</template>
