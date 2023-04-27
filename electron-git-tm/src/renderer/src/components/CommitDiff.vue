<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals } from '@renderer/globals'
import { Commit } from '../../../main/Commit'

const diff = ref('')

watch(
  () => globals.selectedCommitRows,
  async () => {
    const commit: Commit = globals.selectedCommitRows[0]
    if (!commit) {
      return
    }
    const sha = commit.sha
    await getDiff(sha)
  }
)

async function getDiff(sha): Promise<void> {
  const diffStr: string = await window.electron.ipcRenderer.invoke('generate-diff', sha)
  console.log('diff is', diffStr)
  diff.value = diffStr
}
</script>

<template>
  <pre>
{{ diff }}
  </pre>
</template>

<style lang="less">
// @import './assets/css/styles.less';
</style>
