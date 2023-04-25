<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals } from '@renderer/globals'
import { Commit } from '../../../main/Commit'

watch(
  () => globals.selectedCommitRows,
  async () => {
    console.log('selectedCommitRows changed', globals.selectedCommitRows)
    const commit: Commit = globals.selectedCommitRows[0]
    const sha = commit.sha
    await getFiles(sha)
  }
)

async function getFiles(sha): Promise<void> {
  const files: string[] = await window.electron.ipcRenderer.invoke('get-files', sha)
  // console.log('files', files)
  simple.value = convertToTree(files)
}

function convertToTree(arr) {
  const root = {
    label: '',
    children: []
  }
  for (let i = 0; i < arr.length; i++) {
    const path = arr[i].split('/')
    let currentNode = root
    for (let j = 0; j < path.length; j++) {
      const label = path[j]
      const existingNode = currentNode.children.find(child => child.label === label)
      if (existingNode) {
        currentNode = existingNode
      } else {
        const newNode = {
          label: label,
          children: []
        }
        currentNode.children.push(newNode)
        currentNode = newNode
      }
    }
  }
  return root.children
}

// const files = [  ".editorconfig",  ".eslintignore",  ".eslintrc.cjs",  ".gitignore",  ".prettierignore",  ".prettierrc.yaml",  ".vscode/extensions.json",  ".vscode/launch.json",  ".vscode/settings.json",  "README.md",  "electron-builder.yml",  "electron.vite.config.1681794709451.mjs",  "electron.vite.config.1681822042798.mjs",  "electron.vite.config.ts",  "package-lock.json",  "package.json",  "postcss.config.js",  "src/main/Commit.ts",  "src/main/generateHtml.js",  "src/main/getBranches.ts",  "src/main/getCommits.ts",  "src/main/index.ts",  "src/main/templates/template-file-contents.hbs",  "src/preload/index.d.ts",  "src/preload/index.ts",  "src/renderer/index.html",  "src/renderer/src/App.vue",  "src/renderer/src/AppResearch.vue",  "src/renderer/src/assets/css/styles.less",  "src/renderer/src/assets/icons.svg",  "src/renderer/src/assets/users.json",  "src/renderer/src/components/Branch.vue",  "src/renderer/src/components/Commits.vue",  "src/renderer/src/components/TimeFileTree.vue",  "src/renderer/src/components/TimeLhs.vue",  "src/renderer/src/components/TimeMachine.vue",  "src/renderer/src/components/TimeRhsFileContents.vue",  "src/renderer/src/components/Versions.vue",  "src/renderer/src/components/research/AndyQDialog.vue",  "src/renderer/src/components/research/AndySlots.vue",  "src/renderer/src/components/research/AndySplitter.vue",  "src/renderer/src/components/research/LastKeyPressed.vue",  "src/renderer/src/components/research/SmartyTable.vue",  "src/renderer/src/components/research/SmartyTableSel.vue",  "src/renderer/src/components/research/TreeAndSplitter.vue",  "src/renderer/src/components/research/VuetifyList.vue",  "src/renderer/src/components/research/sub/HorizontalSplitter.vue",  "src/renderer/src/env.d.ts",  "src/renderer/src/globals.ts",  "src/renderer/src/index.css",  "src/renderer/src/main.ts",  "tailwind.config.js",  "tsconfig.json",  "tsconfig.node.json",  "tsconfig.web.json"]

const selected = ref('Room view')
const expanded = ref(['Relax Hotel', 'Room amenities'])

const simple = ref([
  {
    label: 'Relax Hotel',
    children: [
      {
        label: 'Room view',
        icon: 'photo'
      },
      {
        label: 'Room service',
        icon: 'local_dining'
      },
      {
        label: 'Room amenities',
        children: [
          {
            label: 'Air conditioning',
            icon: 'ac_unit'
          },
          {
            label: 'TV',
            icon: 'tv'
          },
          {
            label: 'Wi-Fi',
            icon: 'wifi'
          },
          {
            label: 'Minibar',
            icon: 'local_bar'
          },
          {
            label: 'Safe',
            icon: 'lock'
          },
          {
            label: 'Bathroom',
            icon: 'bathtub'
          }
        ]
      },
      {
        label: 'Room rates',
        icon: 'attach_money'
      },
      {
        label: 'Room availability',
        icon: 'event_available'
      },
      {
        label: 'Room booking',
        icon: 'event_busy'
      }
    ]
  }
])

// simple.value = convertToTree(files)

</script>

<template>
  <div class="q-pa-md">
    <!-- {{ selected }}
    {{ expanded }}
    <br />
    <q-btn label="Collapse" @click="expanded = []" />
    <q-btn label="Expand" @click="expanded = ['Relax Hotel']" />
    <q-btn label="Expand2" @click="expanded = ['Relax Hotel', 'Room amenities']" />
    <q-btn label="select Room view" @click="selected = 'Room view'" />
    <q-btn label="select TV" @click="selected = 'TV'" />
    <q-btn label="Change a node" @click="simple[0].children[1].label = 'FRED'" /> -->
    <q-tree
      v-model:selected="selected"
      v-model:expanded="expanded"
      :nodes="simple"
      node-key="label"
      selected-color="primary"
      default-expand-all
      dark
    />
  </div>
</template>
