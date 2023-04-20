<script setup lang="ts">
import { reactive } from 'vue'

const versions = reactive({ ...window.electron.process.versions })
</script>

<template>
  <hr />
  <div class="flex justify-evenly">
    <span>Electron v{{ versions.electron }}</span>
    <span>Chromium v{{ versions.chrome }}</span>
    <span>Node v{{ versions.node }}</span>
    <span>V8 v{{ versions.v8 }}</span>
  </div>
</template>
