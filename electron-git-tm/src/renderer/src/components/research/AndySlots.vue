<template>
  <div class="my">
    <p><b>This is the AndySlots component offering several slots:</b></p>

    <slot>default slot placeholder</slot>
    <div><slot name="second">second placeholder</slot></div>
    <p><slot name="third">third placeholder</slot></p>
    <slot name="fourth">fourth placeholder</slot>
  </div>
</template>

<script setup>
import { ref, computed, watch, onMounted } from 'vue'

onMounted(() => {
  console.log('mounted AndySlots ok')
})
</script>

<style>
div.my {
  border: 1px solid cyan;
}
</style>
