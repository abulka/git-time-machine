<script setup lang="ts">
import { ref } from 'vue'
import Commits from './Commits.vue'
import TimeFileTree from './TimeFileTree.vue'
import Branch from './Branch.vue'

const splitterModel = ref(30)
const splitterModelDiffs = ref(55)
</script>

<template>
  <Branch />
  <q-splitter v-model="splitterModel" horizontal style="height: 100vh">
    <template #before>
      <Commits />
    </template>

    <template #after>
      <q-splitter v-model="splitterModelDiffs" horizontal>
        <template #before>
          <TimeFileTree />
        </template>
        <template #after>
          <div class="q-pa-md">
            <div class="text-h4 q-mb-md">After</div>
            <div v-for="n in 20" :key="n" class="q-my-md">
              {{ n }}. Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium
              praesentium cumque magnam odio iure quidem, quod illum numquam possimus obcaecati
              commodi minima assumenda consectetur culpa fuga nulla ullam. In, libero.
            </div>
          </div>
        </template>
      </q-splitter>
    </template>
  </q-splitter>
</template>
