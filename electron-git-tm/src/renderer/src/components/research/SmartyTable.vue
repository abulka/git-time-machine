<script setup lang="ts">
// import Versions from './components/Versions.vue'
import { ref } from 'vue'

// const name = ref('World')
const users = ref([
  {
    id: 1,
    name: 'John Doe',
    age: 35,
    email: 'johndoe@example.com',
    address: {
      street: '123 Main St',
      city: 'Anytown',
      state: 'CA'
    }
  },
  {
    id: 2,
    name: 'Jane Smith',
    age: 28,
    email: 'janesmith@example.com',
    address: {
      street: '456 Elm St',
      city: 'Othertown',
      state: 'NY'
    }
  },
  {
    id: 3,
    name: 'Bob Johnson',
    age: 42,
    email: 'bobjohnson@example.com',
    address: {
      street: '789 Oak St',
      city: 'Somewhere',
      state: 'TX'
    }
  }
])

// function showDialog(): void {
//   show.value = true
// }
</script>

<template>
  <VTable :data="users">
    <template #head>
      <tr>
        <th>Name</th>
        <th>Age</th>
        <th>Email</th>
        <th>Address</th>
      </tr>
    </template>
    <template #body="{ rows }">
      <tr v-for="row in rows" :key="row.id">
        <td>{{ row.name }}</td>
        <td>{{ row.age }}</td>
        <td>{{ row.email }}</td>
        <td>
          {{ row.address.street }},
          {{ row.address.city }}
          {{ row.address.state }}
        </td>
      </tr>
    </template>
  </VTable>
</template>
