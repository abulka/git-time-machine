<script setup lang="ts">
// import Versions from './components/Versions.vue'
// import { ref } from 'vue'

// const show = ref(false)

// function showDialog(): void {
//   show.value = true
// }
</script>

<template>
  <div class="q-pa-md">
    <div class="text-h4 q-mb-md">RHS</div>
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
