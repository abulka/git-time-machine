<script setup lang="ts">
import { ref } from 'vue'
import TimeLhs from './TimeLhs.vue'
import TimeRhsFileContents from './TimeRhsFileContents.vue'
const splitterModelVert = ref(60)
</script>

<template>
  <div>
    <q-splitter v-model="splitterModelVert" dark>
      <template #before>
        <div class="p-2">
          <TimeLhs />
        </div>
      </template>
      <template #after>
        <TimeRhsFileContents />
      </template>
    </q-splitter>
  </div>
</template>
