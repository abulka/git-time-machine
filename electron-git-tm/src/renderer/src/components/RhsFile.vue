<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { globals } from '@renderer/globals'

watch(
  // Watch for changes to both commit and selectedTreePath
  [(): string => globals.commit, (): string => globals.selectedTreePath],
  () => {
    generateHtml()
  }
)

function generateHtml(): void {
  if (!globals.selectedTreeNode) {
    noFile()
    return
  }
  window.electron.ipcRenderer
    .invoke('generate-html', globals.commit, globals.selectedTreePath)
    .then((htmlStr) => {
      // Do something with the generated HTML string
      myiframe.value.srcdoc = htmlStr
    })
    .catch((err) => {
      console.error(err)
    })
}

// const url = ref('https://www.example.com')
const myiframe = ref('myiframe')

onMounted(() => {
  // default html content
  noFile()
})

function noFile(): void {
  myiframe.value.srcdoc = `
    <html>
      <head>
        <title>My HTML</title>
      </head>
      <body style="background-color: grey;">
        <p>Click on a file in the tree to view its contents.</p>
      </body>
    </html>
  `
}

// In the outer HTML of your app's render process
window.addEventListener('message', (event) => {
  if (event.data === 'hello from iframe') {
    console.log('Received message from iframe:', event.data)
  }
})
</script>

<template>
  <div class="q-pa-md">
    {{ globals.commit }}
    {{ globals.selectedTreePath }}
    <!-- <q-btn label="Generate HTML" @click="generateHtml" /> -->
    <iframe ref="myiframe" style="height: 100vh" class="w-full"></iframe>
  </div>
</template>

<style lang="less">
// @import './assets/css/styles.less';
</style>
