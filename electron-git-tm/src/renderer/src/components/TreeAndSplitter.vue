<template>
  <div>
    <q-splitter v-model="splitterModel" style="height: 400px">
      <template v-slot:before>
        <div class="q-pa-md">
          <q-tree
            :nodes="simple"
            node-key="label"
            selected-color="primary"
            v-model:selected="selected"
            default-expand-all
          />
        </div>
      </template>
      <template v-slot:after>
        <q-tab-panels
          v-model="selected"
          animated
          transition-prev="jump-up"
          transition-next="jump-up"
        >
          <q-tab-panel name="Relax Hotel">
            <div class="text-h4 q-mb-md">Welcome</div>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
          </q-tab-panel>

          <q-tab-panel name="Food">
            <div class="text-h4 q-mb-md">Food</div>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
          </q-tab-panel>

          <q-tab-panel name="Room service">
            <div class="text-h4 q-mb-md">Room service</div>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
          </q-tab-panel>

          <q-tab-panel name="Room view">
            <div class="text-h4 q-mb-md">Room view</div>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
            <p>
              Lorem ipsum dolor sit, amet consectetur adipisicing elit. Quis praesentium cumque
              magnam odio iure quidem, quod illum numquam possimus obcaecati commodi minima
              assumenda consectetur culpa fuga nulla ullam. In, libero.
            </p>
          </q-tab-panel>
        </q-tab-panels>
      </template>
    </q-splitter>

    <q-btn label="XXXXX" />
    <q-btn @click="addNode" label="Add Node" />
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue';

const simple = ref([
  {
    label: 'Relax Hotel',
    children: [
      {
        label: 'Room view',
        icon: 'photo'
      }
    ]
  }
])

const addNode = (): void => {
  simple.value[0].children.push({
    label: 'New Node',
    icon: 'add'
  })
};

const splitterModel = ref(50)
const selected = ref('Food')

</script>
