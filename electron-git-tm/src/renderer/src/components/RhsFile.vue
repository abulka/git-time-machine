<!-- eslint-disable prettier/prettier -->
<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { globals } from '@renderer/globals'

// import { Point } from '../../../../src/main/generateHtml'
// DUPLICATE DECLARATION
interface Point {
  x: number
  y: number
}

watch(
  // Watch for changes to both commit and selectedTreePath
  [(): string => globals.selectedCommit, (): string => globals.selectedTreePath],
  () => {
    generateHtml()
  }
)

function generateHtml(): void {
  if (!globals.selectedTreeNode) {
    noFile()
    return
  }
  const scrollTo: Point = { x: globals.scrollPosX, y: globals.scrollPos }

  window.electron.ipcRenderer
    .invoke('generate-html', globals.selectedCommit, globals.selectedTreePath, scrollTo, globals.lineTo)
    .then((htmlStr) => {
      // Do something with the generated HTML string
      if (myiframe.value.srcdoc === htmlStr) return
      myiframe.value.srcdoc = htmlStr
    })
    .catch((err) => {
      console.error(err)
    })
}

// const url = ref('https://www.example.com')
const myiframe = ref()

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
  // if (event.data === 'hello from iframe') {
  //   console.log('Received message from iframe:', event.data)
  // }
  // else
  //   console.log('Received message from iframe:', event.data)

  if (event.data.scrollPos) globals.scrollPos = event.data.scrollPos
  if (event.data.scrollPosX) globals.scrollPosX = event.data.scrollPosX
})
</script>

<template>
  <div class="q-pa-md">
    {{ globals.selectedCommit }}
    {{ globals.selectedTreePath }}
    {{ globals.scrollPos }}
    {{ globals.scrollPosX }}
    <!-- <q-btn label="Generate HTML" @click="generateHtml" /> -->
    <iframe ref="myiframe" style="height: 100vh" class="w-full"></iframe>
  </div>
</template>

<style lang="less">
// @import './assets/css/styles.less';
</style>
