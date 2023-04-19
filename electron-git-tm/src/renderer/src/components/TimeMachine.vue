<script setup lang="ts">
import { ref } from 'vue'
import SmartyTable from './SmartyTableSel.vue'
import TimeFileTree from './TimeFileTree.vue'
const splitterModel = ref(30)
const splitterModelVert = ref(60)
const splitterModelDiffs = ref(55)

const selectedColor = ref('main')
const colorOptions = [
  { label: 'main', value: 'main' },
  { label: 'master', value: 'master' },
  { label: 'branch1', value: 'branch1' }
]

// import Versions from './components/Versions.vue'

// const show = ref(false)

// function showDialog(): void {
//   show.value = true
// }
</script>

<template>
  <div>
    <q-splitter v-model="splitterModelVert">
      <template #before>
        <div class="flex items-center">
          <div class="inline mr-6">Select a branch:</div>
          <q-select id="my-select" v-model="selectedColor" :options="colorOptions" />
        </div>
        <q-splitter v-model="splitterModel" horizontal class="h-screen">
          <template #before>
            <SmartyTable />
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
                    {{ n }}. Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis
                    praesentium praesentium cumque magnam odio iure quidem, quod illum numquam
                    possimus obcaecati commodi minima assumenda consectetur culpa fuga nulla ullam.
                    In, libero.
                  </div>
                </div>
              </template>
            </q-splitter>
          </template>
        </q-splitter>
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
