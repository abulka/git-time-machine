<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { globals } from '@renderer/globals'

function branchChanged(value): void {
  console.log('branchChanged', value)
}

async function getBranches(): Promise<void> {
  const _branches = await window.electron.ipcRenderer.invoke('get-branches')

  globals.branches = _branches.map((branch, index) => {
    if (branch.startsWith('* ')) {
      branch = branch.substring(2)
      // TODO set selectedBranchOption to this branch
    }
    return {
      id: index,
      label: branch,
      value: branch
    }
  })
  console.log(`${globals.branches.length} branches: ${globals.branches}`)
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
