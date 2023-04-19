<script setup lang="ts">
// import Versions from './components/Versions.vue'
// import { ref } from 'vue'

// const show = ref(false)

// function showDialog(): void {
//   show.value = true
// }

import { ipcRenderer } from 'electron'

// ipcRenderer.invoke('generate-html', path, sourceFileContents, scrollTo, lineTo)
//   .then(htmlStr => {
//     // Do something with the generated HTML string
//   })
//   .catch(err => {
//     console.error(err)
//   })

function generateHtml(): void {
  // ipcRenderer
  //   .invoke('generate-html')
  //   .then((htmlStr) => {
  //     // Do something with the generated HTML string
  //     console.log(htmlStr)
  //   })
  //   .catch((err) => {
  //     console.error(err)
  //   })
  // console.log('generateHtml', ipcRenderer)
}
</script>

<template>
  <div class="q-pa-md">
    <div class="text-h4 q-mb-md">RHS</div>
    <q-btn label="Generate HTML" @click="generateHtml" />
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
