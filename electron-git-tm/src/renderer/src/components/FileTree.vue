<script setup lang="ts">
import { watch } from 'vue'
import { globals, debug } from '@renderer/globals'
import { Commit } from '../../../shared/Commit'
import { TreeData, TreeDataItem } from '../types/TreeData'

watch([(): string => globals.selectedCommit], async () => {
  const commit: Commit = globals.selectedCommitRows[0]
  if (!commit) {
    return
  }
  const sha = commit.sha
  getFiles(sha)
})

async function getFiles(sha): Promise<void> {
  if (debug.event_flow) console.log('getting file tree...')
  const files: string[] = await window.electron.ipcRenderer.invoke('get-files', sha)
  globals.treeData = convertToTree(files)
}

function convertToTree(arr: string[]): TreeData {
  const root: TreeDataItem = {
    label: '',
    children: [] as TreeData,
    fullPath: ''
  }
  for (let i = 0; i < arr.length; i++) {
    const path = arr[i].split('/')
    let currentNode = root
    let fullPath = ''
    for (let j = 0; j < path.length; j++) {
      const label = path[j]
      // tries to find a child node that has the same label as the one passed in
      // as an argument. If a child node with the same label exists, that node
      // is returned and assigned to the existingNode variable.
      const existingNode = currentNode.children
        ? currentNode.children.find((child) => child.label === label)
        : undefined
      fullPath += `/${label}`
      if (existingNode) {
        currentNode = existingNode
      } else {
        const newNode: TreeDataItem = {
          label: label,
          children: [] as TreeData,
          fullPath: fullPath
        }
        currentNode.children = currentNode.children || []
        currentNode.children.push(newNode)
        currentNode = newNode
      }
    }
  }
  return root.children
}

function selectionChanged(state): void {
  const path = state.substring(1) // remove leading '/'
  if (globals.scroll_is_for_path !== path) {
    // If file path has changed, reset scroll_pos to 0
    globals.scrollPos = 0
    globals.scrollPosX = 0
  }
  globals.scroll_is_for_path = path
}
</script>

<template>
  <div class="q-pa-md">
    <q-tree
      v-model:selected="globals.selectedTreeNode"
      v-model:expanded="globals.expanded"
      :nodes="globals.treeData"
      node-key="fullPath"
      selected-color="primary"
      default-expand-all
      dark
      @update:selected="selectionChanged"
    />
  </div>
</template>
