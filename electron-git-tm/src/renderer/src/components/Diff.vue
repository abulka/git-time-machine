<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals } from '@renderer/globals'

const myiframe = ref()

watch([(): string => globals.diffHtml], async () => {
  myiframe.value.srcdoc = globals.diffHtml
})
</script>

<template>
  <iframe ref="myiframe" width="100%" height="100%" frameborder="0"></iframe>
</template>
