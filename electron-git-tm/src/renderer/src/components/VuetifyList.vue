<template>
  <v-app>
    <v-main>
      <v-text-field v-model="msg" />
      <v-text-field v-model="msg" />

      <v-card class="mx-auto" max-width="300">
        <p>hi there this is a test of vuetify v-list</p>

        <v-list density="compact">
          <v-list-subheader>REPORTS</v-list-subheader>

          <v-list-item v-for="(item, i) in items" :key="i" :value="item" active-color="primary">
            <template v-slot:prepend>
              <v-icon :icon="item.icon"></v-icon>
            </template>

            <v-list-item-title v-text="item.text"></v-list-item-title>
          </v-list-item>
        </v-list>
      </v-card>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref } from 'vue'

const msg = ref('Hello World!')

const items = ref([
  { text: 'Real-Time', icon: 'mdi-clock' },
  { text: 'Audience', icon: 'mdi-account' },
  { text: 'Conversions', icon: 'mdi-flag' }
])
</script>
