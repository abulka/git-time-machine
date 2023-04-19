<script setup lang="ts">
import { ref, onMounted } from 'vue'

function generateHtml(): void {
  console.log('generateHtml')

  // window.electron.ipcRenderer.send('say', 'hello there')

  // window.electron.ipcRenderer
  //   .invoke('ping', 'dat')
  //   .then((result) => {
  //     console.log('renderer process got', result) // logs 'pong'
  //   })
  //   .catch((err) => {
  //     console.error(err)
  //   })

  window.electron.ipcRenderer
    .invoke('generate-html')
    .then((htmlStr) => {
      // Do something with the generated HTML string
      console.log(htmlStr)
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
    <div class="text-h4 q-mb-md">RHS</div>
    <q-btn label="Generate HTML" @click="generateHtml" />
    <iframe ref="myiframe" width="100%" height="600"></iframe>
    <div v-for="n in 20" :key="n" class="q-my-md">
      {{ n }}. Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
      magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima assumenda
      consectetur culpa fuga nulla ullam. In, libero.
    </div>
  </div>
</template>

<style lang="less">
// @import './assets/css/styles.less';
</style>
