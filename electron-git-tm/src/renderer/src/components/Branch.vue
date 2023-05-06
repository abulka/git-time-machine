<script setup lang="ts">
import { onMounted } from 'vue'
import { globals } from '@renderer/globals'

function branchChanged(value): void {
  console.log('branchChanged', value) // just a notification, does nothing
}

onMounted(() => {
  // I used to call getBranches() here, but it's better to wait for the main process to
  // send the 'shouldGetBranches' message.
  // getBranches()
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
