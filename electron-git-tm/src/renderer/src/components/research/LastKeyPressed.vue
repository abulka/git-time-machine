<script setup lang="ts">
// import Versions from './components/Versions.vue'
import { ref } from 'vue'

// const show = ref(false)

// function showDialog(): void {
//   show.value = true
// }
const lastKeyPressed = ref('')
function handleKeyDown(event): void {
  console.log('key', event.key)
  lastKeyPressed.value = event.key
}
</script>

<template>
  <input type="text" autofocus @keydown="handleKeyDown">
  {{ lastKeyPressed }}
</template>

<style lang="less">
input {
  width: 100%;
  height: 100%;
  font-size: 20px;
  padding: 10px;
  border: none;
  outline: none;
  background: transparent;
  color: white;
}
</style>