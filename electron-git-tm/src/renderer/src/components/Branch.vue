<script setup lang="ts">
import { globals } from '@renderer/globals'

const branches = [
  { label: 'main', value: 'main' },
  { label: 'master', value: 'master' },
  { label: 'branch1', value: 'branch1' },
  { label: 'branch2', value: 'branch2' },
]
function branchChanged(value): void {
  console.log('branchChanged', value)
}
</script>

<template>
  <div class="flex items-center">
    <div class="inline mr-6">Select a branch:</div>
    <q-select
      id="my-select"
      v-model="globals.selectedBranch"
      :options="branches"
      dark
      @update:model-value="branchChanged"
    />
  </div>
</template>
