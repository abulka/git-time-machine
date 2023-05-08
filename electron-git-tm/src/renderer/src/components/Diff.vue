<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals, debug } from '@renderer/globals'
import { Commit } from '../../../shared/Commit'

const myiframe = ref()

watch([(): string => globals.selectedCommit], async () => {
  if (globals.selectedCommit == undefined) return
  getDiff()
})

async function getDiff(): Promise<void> {
  if (debug.event_flow) console.log('getting diff...', globals.selectedCommit)
  const commit: Commit = globals.selectedCommitRows[0]
  if (!commit) {
    return
  }
  const sha = commit.sha
  const diffHtml: string = await window.electron.ipcRenderer.invoke('generate-diff', sha)
  myiframe.value.srcdoc = diffHtml
}

// In the outer HTML of your app's render process
window.addEventListener('message', (event) => {
  if (event.data == undefined) {
    console.log('Unknown message received from diff iframe:', event.data)
    return
  }
  if (event.data.command == 'jump_to_file') {
    // console.log(`jump_to_file ${event.data.filePath}:${event.data.lineNum}`)
    globals.selectedTreeNode = '/' + event.data.filePath
  }
})
</script>

<template>
  <iframe ref="myiframe" width="100%" height="100%" frameborder="0"></iframe>
</template>
