<template>
  <div>
    <q-btn label="Show Dialog" @click="showDialog" />
    <q-dialog v-model="show" title="My Dialog" @hide="hideDialog">
      <q-card>
        <q-card-section>
          <p>This is the content of my dialog.</p>
          <p>This is the content of my dialog.</p>
          <p>This is the content of my dialog.</p>
          <p>This is the content of my dialog.</p>
        </q-card-section>
        <q-card-actions align="right">
          <q-btn label="Cancel" @click="hideDialog" />
          <q-btn label="OK" color="primary" @click="hideDialog" />
          <slot name="actions" />
        </q-card-actions>
      </q-card>
    </q-dialog>
  </div>
  {{ show }}
</template>

<script setup lang="ts">
import { ref } from 'vue'

const show = ref(false)

function showDialog(): void {
  show.value = true
}
function hideDialog(): void {
  show.value = false
}
</script>
