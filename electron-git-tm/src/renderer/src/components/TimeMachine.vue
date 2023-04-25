<script setup lang="ts">
import { ref } from 'vue'
import Lhs from './Lhs.vue'
import RhsFile from './RhsFile.vue'
const splitterModelVert = ref(60)
</script>

<template>
  <div>
    <q-splitter v-model="splitterModelVert" dark>
      <template #before>
        <div class="p-2">
          <Lhs />
        </div>
      </template>
      <template #after>
        <RhsFile />
      </template>
    </q-splitter>
  </div>
</template>
