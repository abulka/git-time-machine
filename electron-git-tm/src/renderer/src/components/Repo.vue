<script setup lang="ts">
import { globals } from '@renderer/globals'
import { refreshRepo } from '@renderer/business'

function changeRepo(_event): void {
  window.electron.ipcRenderer.invoke('change-repo')
}
function _refreshRepo(_event): void {
  refreshRepo()
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
      @click="_refreshRepo"
    />
    <div class="ml-auto" style="text-align: center">
      {{ globals.repoDirName }}
    </div>
    <div class="d-flex ml-auto" style="width: 20px; height: 20px;">
      <q-spinner v-if="globals.isLoading" color="primary" size="20px" />
    </div>
    <div class="ml-auto text-red" style="text-align: right">{{ globals.warningMsg }}</div>
  </div>
</template>
