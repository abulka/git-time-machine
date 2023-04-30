<script setup lang="ts">
import { ref, Ref, watch } from 'vue'
import { globals } from '@renderer/globals'
import { Commit } from '../../../shared/Commit'

interface TreeDataItem {
  label: string
  icon?: string
  children?: TreeDataItem[]
  fullPath: string
}

type TreeData = TreeDataItem[]

// const treeData: TreeData = ref([])
const treeData: Ref<TreeData> = ref<TreeData>([])
const expanded = ref(['src', 'main'])

watch(
  () => globals.selectedCommitRows,
  async () => {
    const commit: Commit = globals.selectedCommitRows[0]
    if (!commit) {
      return
    }
    const sha = commit.sha
    await getFiles(sha)
  }
)

async function getFiles(sha): Promise<void> {
  const files: string[] = await window.electron.ipcRenderer.invoke('get-files', sha)
  // console.log('files', files)
  treeData.value = convertToTree(files)
}

function convertToTree(arr: string[]): TreeData {
  const root = {
    label: '',
    children: [] as TreeDataItem[],
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
        const newNode = {
          label: label,
          children: [],
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

function convertToTreeNEW(arr: string[]): TreeData {
  const root: TreeDataItem = {
    label: '',
    children: [] as TreeDataItem[],
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
          children: [] as TreeDataItem[],
          fullPath: fullPath
        }
        currentNode.children = currentNode.children || []
        currentNode.children.push(newNode)
        currentNode = newNode
      }
    }
  }
  const newRoot = {
    label: 'root',
    children: [root],
    fullPath: '/'
  }
  return newRoot.children
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
    <!-- {{ globals.selectedTreeNode }}
    {{ expanded }}
    <br />
    <q-btn label="Collapse" @click="expanded = []" />
    <q-btn label="Expand" @click="expanded = ['Relax Hotel']" />
    <q-btn label="Expand2" @click="expanded = ['Relax Hotel', 'Room amenities']" />
    <q-btn label="select Room view" @click="selected = 'Room view'" />
    <q-btn label="select TV" @click="selected = 'TV'" />
    <q-btn label="Change a node" @click="treeData[0].children[1].label = 'FRED'" /> -->
    <q-tree
      v-model:selected="globals.selectedTreeNode"
      v-model:expanded="expanded"
      :nodes="treeData"
      node-key="fullPath"
      selected-color="primary"
      default-expand-all
      dark
      @update:selected="selectionChanged"
    />
  </div>
</template>
