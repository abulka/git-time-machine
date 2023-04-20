<script setup lang="ts">
import { ref } from 'vue'

const selected = ref('Room view')
const expanded = ref(['Relax Hotel', 'Room amenities'])

const simple = ref([
  {
    label: 'Relax Hotel',
    children: [
      {
        label: 'Room view',
        icon: 'photo'
      },
      {
        label: 'Room service',
        icon: 'local_dining'
      },
      {
        label: 'Room amenities',
        children: [
          {
            label: 'Air conditioning',
            icon: 'ac_unit'
          },
          {
            label: 'TV',
            icon: 'tv'
          },
          {
            label: 'Wi-Fi',
            icon: 'wifi'
          },
          {
            label: 'Minibar',
            icon: 'local_bar'
          },
          {
            label: 'Safe',
            icon: 'lock'
          },
          {
            label: 'Bathroom',
            icon: 'bathtub'
          }
        ]
      },
      {
        label: 'Room rates',
        icon: 'attach_money'
      },
      {
        label: 'Room availability',
        icon: 'event_available'
      },
      {
        label: 'Room booking',
        icon: 'event_busy'
      }
    ]
  }
])
</script>

<template>
  <div class="q-pa-md">
    {{ selected }}
    {{ expanded }}
    <br />
    <q-btn label="Collapse" @click="expanded = []" />
    <q-btn label="Expand" @click="expanded = ['Relax Hotel']" />
    <q-btn label="Expand2" @click="expanded = ['Relax Hotel', 'Room amenities']" />
    <q-btn label="select Room view" @click="selected = 'Room view'" />
    <q-btn label="select TV" @click="selected = 'TV'" />
    <q-tree
      v-model:selected="selected"
      v-model:expanded="expanded"
      :nodes="simple"
      node-key="label"
      selected-color="primary"
      default-expand-all
      dark
    />
  </div>
</template>
