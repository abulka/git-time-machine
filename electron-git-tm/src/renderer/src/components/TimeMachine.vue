<script setup lang="ts">
import { ref } from 'vue'
import TimeLhs from './TimeLhs.vue'
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
        <div class="q-pa-md">
          <div class="text-h4 q-mb-md">RHS</div>
          <div v-for="n in 20" :key="n" class="q-my-md">
            {{ n }}. Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium
            cumque magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
            assumenda consectetur culpa fuga nulla ullam. In, libero.
          </div>
        </div>
      </template>
    </q-splitter>
  </div>
</template>
