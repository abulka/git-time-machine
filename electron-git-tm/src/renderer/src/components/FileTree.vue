<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals } from '@renderer/globals'
import { Commit } from '../../../main/Commit'

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
  simple.value = convertToTree(files)
}

// const selected = ref('README.md')
const expanded = ref(['src', 'main'])

// Incoming array is a list of file paths, e.g.:
// .github/workflows/build-snap.yml
// .github/workflows/offline/build-all-os-except-mac.yml
// .github/workflows/offline/build-all-os.yml
// .github/workflows/offline/build-mac.yml
// .gitignore
// README.md
// bin/build-package
// bin/build-snap
// bin/build-snap-clean
// bin/build-snap-clean-python-stuff
// bin/build-snap-debug
// bin/install-snap
// bin/lxd-containers-ls
// bin/lxd-shell
// bin/publish-snap
// bin/run
// bin/run-snap-with-shell
// doco/images/screenshot1.png
// doco/uml/events.drawio
// doco/uml/events.png
// doco/uml/events.svg
// doco/uml/uml.pyns
// electron-git-tm/.editorconfig

interface TreeDataItem {
  label: string;
  icon?: string;
  children?: TreeDataItem[];
  fullPath: string;
}

type TreeData = TreeDataItem[];

function convertToTree(arr): TreeData {
  const root = {
    label: '',
    children: [] as TreeDataItem[],
  }
  for (let i = 0; i < arr.length; i++) {
    const path = arr[i].split('/')
    let currentNode = root
    let fullPath = ''
    for (let j = 0; j < path.length; j++) {
      const label = path[j]
      const existingNode = currentNode.children ? currentNode.children.find((child) => child.label === label) : undefined
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

const simple: TreeData = ref([
  // {
  //   label: 'Relax Hotel',
  //   children: [
  //     {
  //       label: 'Room view',
  //       icon: 'photo'
  //     },
  //     {
  //       label: 'Room service',
  //       icon: 'local_dining'
  //     },
  //     {
  //       label: 'Room amenities',
  //       children: [
  //         {
  //           label: 'Air conditioning',
  //           icon: 'ac_unit'
  //         },
  //         {
  //           label: 'TV',
  //           icon: 'tv'
  //         },
  //         {
  //           label: 'Wi-Fi',
  //           icon: 'wifi'
  //         },
  //         {
  //           label: 'Minibar',
  //           icon: 'local_bar'
  //         },
  //         {
  //           label: 'Safe',
  //           icon: 'lock'
  //         },
  //         {
  //           label: 'Bathroom',
  //           icon: 'bathtub'
  //         }
  //       ]
  //     },
  //     {
  //       label: 'Room rates',
  //       icon: 'attach_money'
  //     },
  //     {
  //       label: 'Room availability',
  //       icon: 'event_available'
  //     },
  //     {
  //       label: 'Room booking',
  //       icon: 'event_busy'
  //     }
  //   ]
  // }
])

// simple.value = convertToTree(files)
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
    <q-btn label="Change a node" @click="simple[0].children[1].label = 'FRED'" /> -->
    <q-tree
      v-model:selected="globals.selectedTreeNode"
      v-model:expanded="expanded"
      :nodes="simple"
      node-key="fullPath"
      selected-color="primary"
      default-expand-all
      dark
    />
  </div>
</template>
