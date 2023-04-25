<script setup lang="ts">
import { ref, onMounted, watch } from 'vue'
import { globals } from '@renderer/globals'

watch(
  // TODO watch for changes to globals.commit as well
  () => globals.selectedTreeNode,
  () => {
    console.log('selectedTreeNode', globals.selectedTreeNode)
    generateHtml()
  }
)

function generateHtml(): void {
  console.log('generateHtml', globals.commit, globals.selectedTreeNode)
  window.electron.ipcRenderer
    .invoke('generate-html', globals.commit, globals.selectedTreeNode)
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
})
</script>

<template>
  <div class="q-pa-md">
    {{ globals.commit }}
    {{ globals.selectedTreeNode }}
    <q-btn label="Generate HTML" @click="generateHtml" />
    <iframe ref="myiframe" style="height: 100vh" class="w-full"></iframe>
  </div>
</template>

<style lang="less">
// @import './assets/css/styles.less';
</style>
