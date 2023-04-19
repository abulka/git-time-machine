<script setup lang="ts">
import { ref } from 'vue'

const selected = ref('Room view')

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
    <q-tree
      v-model:selected="selected"
      :nodes="simple"
      node-key="label"
      selected-color="primary"
      default-expand-all
    />
  </div>
</template>
