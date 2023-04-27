<script setup lang="ts">
import { ref } from 'vue'
import Commits from './Commits.vue'
import TimeFileTree from './FileTree.vue'
import Branch from './Branch.vue'
import Diff from './CommitDiff.vue'

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
          <Diff />
        </template>
      </q-splitter>
    </template>
  </q-splitter>
</template>
