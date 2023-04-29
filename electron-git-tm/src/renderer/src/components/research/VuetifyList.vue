<template>
  <v-app>
    <v-main>
      <v-text-field v-model="msg" />

      <v-icon>mdi-clock</v-icon>
      <v-icon icon="fa:fas fa-plus" />
      <v-icon icon="fa:fas fa-hashtag" />
      <v-icon icon="fa:fas fa-eye" />
      <v-icon icon="mdi:mdi-minus" />
      <v-icon icon="fa:fas fa-house" />
      <v-icon icon="fa:fas fa-minus" />
      <v-icon icon="mdi-vuetify"></v-icon>
      <v-icon icon="mdi-account"></v-icon>
      <v-icon icon="mdi-home-clock-outline"></v-icon>
      <v-icon icon="mdi-ab-testing"></v-icon>
      <v-icon size="large" color="purple-darken-2" icon="mdi-dialpad"></v-icon>
      <div class="d-flex justify-space-around">
        <v-icon icon="fa:fas fa-lock"></v-icon>
        <v-icon icon="fa:fas fa-search"></v-icon>
        <v-icon icon="fa:fas fa-list"></v-icon>
        <v-icon icon="fa:fas fa-edit"></v-icon>
        <v-icon icon="fa:fas fa-tachometer-alt"></v-icon>
        <v-icon icon="fa:fas fa-circle-notch fa-spin"></v-icon>
      </div>

      <!-- add a spacer -->
      <div class="pb-5"></div>

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

      <div class="text-center">
        <v-btn prepend-icon="mdi-check-circle" append-icon="mdi-account-circle">
          <template v-slot:prepend>
            <v-icon color="success"></v-icon>
          </template>

          Button

          <template v-slot:append>
            <v-icon color="warning"></v-icon>
          </template>
        </v-btn>
      </div>
    </v-main>
  </v-app>
</template>

<script setup lang="ts">
import { ref } from 'vue'

const msg = ref('Hello World!')

const items = ref([
  { text: 'Real-Time', icon: 'mdi-clock' },
  { text: 'Audience', icon: 'mdi-account' },
  { text: 'Conversions', icon: 'mdi-flag' }
  // { text: 'Andy', icon: 'flag' }
])
</script>
