<!-- eslint-disable @typescript-eslint/explicit-function-return-type -->
<script setup lang="ts">
import { ref, onMounted } from 'vue'

interface User {
  _id: string
  name: string
}
// interface SelectedItem {
//   id: number;
//   name: string;
//   // add other properties as needed
// }
// interface UsersTable {
//   selectAll: () => void;
//   deselectAll: () => void;
//   selectRows: (ids: number[]) => void;
//   // Add any other properties or methods that the usersTable object has
// }

const usersTable = ref()
// const usersTable = ref<HTMLInputElement | null>(null) // Template Refs

// const name = ref('World')
const users = ref([
  {
    _id: '57ef9cd8e22df324d77c4f07',
    index: 0,
    guid: '9bc8e89d-658c-47cf-acc3-b0e225ddb549',
    isActive: false,
    balance: '$1,029.59',
    picture: 'http://placehold.it/32x32',
    age: 25,
    eyeColor: 'green',
    name: 'Deana Lindsay',
    gender: 'female',
    company: 'TERRAGO',
    email: 'deanalindsay@terrago.com',
    phone: '+1 (858) 506-2166',
    address: {
      street: '268 Garnet Street',
      city: 'Chicopee',
      state: 'Pennsylvania'
    },
    registered: '2015-10-30',
    tags: ['reprehenderit', 'duis', 'mollit', 'eiusmod', 'incididunt', 'nisi', 'sunt']
  },
  {
    _id: '57ef9cd8392af802937a0974',
    index: 1,
    guid: '1436aae5-4540-474a-8bad-4ca6b9c903ac',
    isActive: true,
    balance: '$1,302.22',
    picture: 'http://placehold.it/32x32',
    age: 39,
    eyeColor: 'blue',
    name: 'Wyatt Kline',
    gender: 'male',
    company: 'MEDMEX',
    email: 'wyattkline@medmex.com',
    phone: '+1 (827) 579-2502',
    address: {
      street: '234 Irwin Street',
      city: 'Irwin',
      state: 'Maine'
    },
    registered: '2014-06-17',
    tags: ['aute', 'laboris', 'sit', 'voluptate', 'magna', 'voluptate', 'occaecat']
  },
  {
    _id: '57ef9cd865c7f5203dc5e126',
    index: 2,
    guid: '2bc5aad6-2172-4041-a949-b31729290f25',
    isActive: true,
    balance: '$3,066.01',
    picture: 'http://placehold.it/32x32',
    age: 29,
    eyeColor: 'green',
    name: 'Harmon Huber',
    gender: 'male',
    company: 'SNIPS',
    email: 'harmonhuber@snips.com',
    phone: '+1 (931) 482-3018',
    address: {
      street: '913 Gerritsen Avenue',
      city: 'Nash',
      state: 'American Samoa'
    },
    registered: '2016-01-25',
    tags: ['do', 'voluptate', 'id', 'do', 'occaecat', 'minim', 'tempor']
  },
  {
    _id: '57ef9cd8594cc4bc18a121f7',
    index: 3,
    guid: '5d48aae2-9e3c-434e-a835-3abdab56e240',
    isActive: false,
    balance: '$3,574.33',
    picture: 'http://placehold.it/32x32',
    age: 29,
    eyeColor: 'green',
    name: 'Penny Maddox',
    gender: 'female',
    company: 'BALUBA',
    email: 'pennymaddox@baluba.com',
    phone: '+1 (873) 552-2338',
    address: {
      street: '218 Agate Court',
      city: 'Sandston',
      state: 'Oregon'
    },
    registered: '2016-01-08',
    tags: ['anim', 'aliqua', 'consequat', 'tempor', 'excepteur', 'est', 'enim']
  },
  {
    _id: '57ef9cd846b7cd74053c10c9',
    index: 4,
    guid: '3c4a0399-68c9-4741-8c77-0e7e0dd9ed00',
    isActive: true,
    balance: '$1,363.39',
    picture: 'http://placehold.it/32x32',
    age: 39,
    eyeColor: 'brown',
    name: 'Morgan Gomez',
    gender: 'male',
    company: 'AFFLUEX',
    email: 'morgangomez@affluex.com',
    phone: '+1 (976) 466-3779',
    address: {
      street: '632 Highland Avenue',
      city: 'Tuttle',
      state: 'Connecticut'
    },
    registered: '2014-04-10',
    tags: ['duis', 'deserunt', 'id', 'nostrud', 'mollit', 'consequat', 'ea']
  },
  {
    _id: '57ef9cd8d429bf34a0c2dc36',
    index: 5,
    guid: 'd321b26f-f8ce-461e-9673-5b9497aacea7',
    isActive: false,
    balance: '$1,469.54',
    picture: 'http://placehold.it/32x32',
    age: 35,
    eyeColor: 'green',
    name: 'Beck Mckay',
    gender: 'male',
    company: 'GEOLOGIX',
    email: 'beckmckay@geologix.com',
    phone: '+1 (879) 477-3341',
    address: {
      street: '936 Woodpoint Road',
      city: 'Wakulla',
      state: 'Mississippi'
    },
    registered: '2016-05-06',
    tags: ['non', 'cillum', 'culpa', 'irure', 'nulla', 'non', 'occaecat']
  },
  {
    _id: '57ef9cd86866468dc1c20447',
    index: 6,
    guid: 'c097a185-98ee-4bdd-a6ec-a3e5e40801be',
    isActive: true,
    balance: '$3,125.22',
    picture: 'http://placehold.it/32x32',
    age: 39,
    eyeColor: 'blue',
    name: 'Massey Carlson',
    gender: 'male',
    company: 'EARTHWAX',
    email: 'masseycarlson@earthwax.com',
    phone: '+1 (871) 471-2647',
    address: {
      street: '278 Chapel Street',
      city: 'Taycheedah',
      state: 'Hawaii'
    },
    registered: '2014-10-22',
    tags: ['ullamco', 'fugiat', 'consequat', 'nostrud', 'aliqua', 'consequat', 'fugiat']
  },
  {
    _id: '57ef9cd83f55c1d078fc6cfd',
    index: 7,
    guid: '29e53cbb-6353-44a3-a2c8-e7b3176d00af',
    isActive: false,
    balance: '$3,663.46',
    picture: 'http://placehold.it/32x32',
    age: 33,
    eyeColor: 'blue',
    name: 'Hill Hale',
    gender: 'male',
    company: 'CALCU',
    email: 'hillhale@calcu.com',
    phone: '+1 (877) 598-2610',
    address: {
      street: '618 Newport Street',
      city: 'Deercroft',
      state: 'Colorado'
    },
    registered: '2016-04-18',
    tags: ['nostrud', 'duis', 'Lorem', 'ex', 'elit', 'labore', 'in']
  },
  {
    _id: '57ef9cd8f8863a277e1c2055',
    index: 8,
    guid: '955a6cd5-b73c-4a6c-9280-76cbc4e232b2',
    isActive: false,
    balance: '$2,451.20',
    picture: 'http://placehold.it/32x32',
    age: 26,
    eyeColor: 'blue',
    name: 'Stokes Hurst',
    gender: 'male',
    company: 'DATAGEN',
    email: 'stokeshurst@datagen.com',
    phone: '+1 (897) 537-2718',
    address: {
      street: '146 Conover Street',
      city: 'Dahlen',
      state: 'North Dakota'
    },
    registered: '2016-01-30',
    tags: ['est', 'eu', 'anim', 'eiusmod', 'exercitation', 'commodo', 'nulla']
  },
  {
    _id: '57ef9cd86b62971bb96f7603',
    index: 9,
    guid: '239a3301-1dae-4ef8-ae30-7e92a84c78a2',
    isActive: false,
    balance: '$1,753.67',
    picture: 'http://placehold.it/32x32',
    age: 20,
    eyeColor: 'green',
    name: 'Cain Knapp',
    gender: 'male',
    company: 'NAMEBOX',
    email: 'cainknapp@namebox.com',
    phone: '+1 (873) 435-3377',
    address: {
      street: '460 Bridgewater Street',
      city: 'Manchester',
      state: 'Michigan'
    },
    registered: '2016-01-04',
    tags: ['fugiat', 'non', 'adipisicing', 'id', 'incididunt', 'do', 'enim']
  },
  {
    _id: '57ef9cd8431bccda13eea218',
    index: 10,
    guid: 'b5671cc8-2776-4180-9cab-2f26fd38c720',
    isActive: false,
    balance: '$1,619.16',
    picture: 'http://placehold.it/32x32',
    age: 22,
    eyeColor: 'brown',
    name: 'Ramirez Valdez',
    gender: 'male',
    company: 'SOLAREN',
    email: 'ramirezvaldez@solaren.com',
    phone: '+1 (820) 465-2360',
    address: {
      street: '932 Battery Avenue',
      city: 'Iola',
      state: 'Virginia'
    },
    registered: '2014-01-27',
    tags: ['minim', 'aliqua', 'culpa', 'dolore', 'excepteur', 'minim', 'sit']
  }
])

// const selectedRows = ref([])
// const selectedRows: User[] = ref([]) // wrong
// const selectedRows<User[]> = ref([]) // wrong
const selectedRows = ref<User[]>([])

onMounted(() => {
  // console.log('users', users)
})

function selectAll() {
  console.log('selectAll', users)
  usersTable.value.selectAll()
}

function deselectAll() {
  usersTable.value.deselectAll()
}
function selectSome() {
  const toSelect = [users.value[0], users.value[2], users.value[5]]
  usersTable.value.selectRows(toSelect)
}
function selectOne() {
  const toSelect = [users.value[4]]
  usersTable.value.selectRows(toSelect)
}
function selectOneOther() {
  const toSelect = [users.value[7]]
  usersTable.value.selectRows(toSelect)
}
</script>

<template>
  <!-- eslint-disable vue/attribute-hyphenation -->
  <!-- eslint-disable vue/v-on-event-hyphenation -->

  <div>
    <div class="flex justify-between mb-5">
      <button @click="selectAll">Select All</button>
      <button @click="deselectAll">Deselect All</button>
      <button @click="selectSome">Select Some</button>
      <button @click="selectOne">Select One</button>
      <button @click="selectOneOther">Select One Other</button>
    </div>

    <VTable
      ref="usersTable"
      :data="users"
      selectionMode="single"
      selectedClass="selected-row"
      @stateChanged="selectedRows = $event.selectedRows"
    >
      <template #head>
        <th>Name</th>
        <th>Age</th>
        <th>State</th>
        <th>Registered at</th>
      </template>
      <template #body="{ rows }">
        <VTr v-for="row in rows" :key="row.guid" :row="row">
          <td>{{ row.name }}</td>
          <td>{{ row.age }}</td>
          <td>{{ row.address.state }}</td>
          <td>{{ row.registered }}</td>
        </VTr>
      </template>
    </VTable>

    <strong>Selected:</strong>
    <div v-if="selectedRows.length === 0">No rows selected</div>
    <ul>
      <li v-for="selected in selectedRows" :key="selected._id">
        {{ selected.name }}
      </li>
    </ul>
  </div>
</template>

<style>
table {
  border-collapse: collapse;
  width: 100%;
}

th,
td {
  border: 1px solid #ccc;
  padding: 8px;
  text-align: left;
}

th {
  background-color: #ac2c2c;
  color: #fff;
}

.selected-row {
  background-color: rgba(255, 255, 255, 0.1);
}
</style>
