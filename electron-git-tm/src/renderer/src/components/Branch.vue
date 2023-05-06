<script setup lang="ts">
import { globals } from '@renderer/globals'

function branchChanged(value): void {
  console.log('branchChanged', value) // just a notification, does nothing
}
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
