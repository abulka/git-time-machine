<script setup lang="ts">
import { onMounted } from 'vue'
import { globals } from '@renderer/globals'

function branchChanged(value): void {
  console.log('branchChanged', value)
}

async function getBranches(): Promise<void> {
  const _branches = await window.electron.ipcRenderer.invoke('get-branches')

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

onMounted(() => {
  getBranches()
})
</script>

<template>
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
