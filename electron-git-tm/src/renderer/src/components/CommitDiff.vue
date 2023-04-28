<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals } from '@renderer/globals'
import { Commit } from '../../../main/Commit'

const myiframe = ref('myiframe')

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
  myiframe.value.srcdoc = `<html>
  <head>
    <title>My HTML</title>
  </head>
  <body style="background-color: grey;">
    <pre>${diffStr}</pre>
  </body>
  </html>
  `
}
</script>

<template>
  <iframe ref="myiframe" width="100%" height="100%" frameborder="0"></iframe>
</template>

<style lang="less">
// @import './assets/css/styles.less';
</style>
