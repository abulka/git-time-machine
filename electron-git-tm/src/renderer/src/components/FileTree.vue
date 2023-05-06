<script setup lang="ts">
import { watch } from 'vue'
import { globals } from '@renderer/globals'
import { Commit } from '../../../shared/Commit'
import { TreeData, TreeDataItem } from '../types/TreeData'
import { debounce } from 'lodash'

watch(
  [
    (): Commit[] => globals.selectedCommitRows,
    (): string => globals.selectedBranch,
    (): string => globals.repoDir,
    (): boolean => globals.repoRefreshNeeded
  ],

  // async () => {
  //   console.log('getting file tree...')
  //   const commit: Commit = globals.selectedCommitRows[0]
  //   if (!commit) {
  //     return
  //   }
  //   const sha = commit.sha
  //   await getFiles(sha)
  // }

  // If you have a watch function with an array of dependencies, it will trigger
  // whenever any of the dependencies change. In your case, if all four of the
  // dependencies change at the same time, the watch function will trigger four
  // times. To reduce the number of triggers, you can debounce the watch
  // function using the lodash.debounce function. This will delay the execution
  // of the function until the dependencies have stabilized, meaning that there
  // have been no changes for a certain amount of time. This can reduce the
  // number of triggers and improve the performance of your application.

  debounce(async () => {
    console.log('getting file tree...')
    const commit: Commit = globals.selectedCommitRows[0]
    if (!commit) {
      return
    }
    const sha = commit.sha
    await getFiles(sha)
  }, 500) // Adjust the delay time as needed
)

async function getFiles(sha): Promise<void> {
  const files: string[] = await window.electron.ipcRenderer.invoke('get-files', sha)
  // console.log('files', files)
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
  // If file path has changed, scroll_pos will be wrong and needs to be reset to 0
  console.log('selectionChanged', state)
  const path = state.substring(1) // remove leading /
  if (globals.scroll_is_for_path !== path) {
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
