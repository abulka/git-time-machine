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
    ensurePathIsExpanded('/' + event.data.filePath)
    // Scroll selectedTreeNode into view
    const el = document.querySelector('.q-tree__node--selected')
    if (el) {
      // timer is needed to wait for the DOM to update first, before scrolling
      setTimeout(() => {
        el.scrollIntoView()
      }, 500)
    }

  }
})
function ensurePathIsExpanded(filePath): void {
  const pathComponents = filePath.split('/')
  const parentNodes: string[] = []

  for (let i = 1; i < pathComponents.length - 1; i++) {
    const parentPath = '/' + pathComponents.slice(1, i+1).join('/')
    if (!globals.expanded.includes(parentPath)) {
      parentNodes.push(parentPath)
    }
  }
  // console.log(`${filePath} parentNodes: ${parentNodes}`)
  globals.expanded = globals.expanded.concat(parentNodes)
}

</script>

<template>
  <iframe
    v-if="globals.commits.length > 0"
    ref="myiframe"
    width="100%"
    height="100%"
    frameborder="0"
  ></iframe>
</template>
