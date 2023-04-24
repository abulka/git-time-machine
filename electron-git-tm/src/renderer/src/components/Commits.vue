<!-- eslint-disable @typescript-eslint/explicit-function-return-type -->
<script setup>
import { ref, onMounted } from 'vue'
// import { Commit } from '../../main/Commit'

async function getCommits() {
  const branch = 'main' // or whatever branch you want to get commits for
  const commits = await window.electron.ipcRenderer.invoke('get-commits', branch)

  // direct!
  commitsData.value = commits

  // commitsData.value = []
  // for (const commit of commits) {
  //   // users.value.push(commit)
  //   const dummy = {}
  //   dummy.guid = commit.sha
  //   dummy.name = commit.sha
  //   dummy.age = commit.comment
  //   dummy.gender = commit.date
  //   dummy.registered = commit.author
  //   commitsData.value.push(dummy)
  // }
}

const usersTable = ref('usersTable')
const commitsData = ref([])
const selectedRows = ref([])

onMounted(() => {
  // call the function getCommits()
  getCommits()

})

function selectAll() {
  console.log('selectAll', commitsData)
  usersTable.value.selectAll()
}

function deselectAll() {
  usersTable.value.deselectAll()
}
function selectSome() {
  const toSelect = [commitsData.value[0], commitsData.value[2], commitsData.value[5]]
  usersTable.value.selectRows(toSelect)
}
function selectOne() {
  const toSelect = [commitsData.value[4]]
  usersTable.value.selectRows(toSelect)
}
function selectOneOther() {
  const toSelect = [commitsData.value[7]]
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
      <button @click="getCommits">Get Commits</button>
    </div>

    <VTable
      ref="usersTable"
      :data="commitsData"
      selectionMode="single"
      selectedClass="selected-row"
      @stateChanged="selectedRows = $event.selectedRows"
    >
      <template #head>
        <th>Sha</th>
        <th>Comment</th>
        <th>Date</th>
        <th>Author</th>
      </template>
      <template #body="{ rows }">
        <VTr v-for="row in rows" :key="row.guid" :row="row">
          <td>{{ row.sha }}</td>
          <td>{{ row.comment }}</td>
          <td>{{ row.date }}</td>
          <td>{{ row.author }}</td>
        </VTr>
      </template>
    </VTable>

    <strong>Selected:</strong>
    <div v-if="selectedRows.length === 0">No rows selected</div>
    <ul>
      <li v-for="selected in selectedRows" :key="selected.id">
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
