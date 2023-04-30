<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals } from '@renderer/globals'
import { Commit } from '../../../shared/Commit'

const myiframe = ref()

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
  const diffHtml: string = await window.electron.ipcRenderer.invoke('generate-diff', sha)
  myiframe.value.srcdoc = diffHtml
}
</script>

<template>
  <iframe ref="myiframe" width="100%" height="100%" frameborder="0"></iframe>
</template>

<style lang="less">
// @import './assets/css/styles.less';
</style>
