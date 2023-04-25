<!-- eslint-disable @typescript-eslint/explicit-function-return-type -->
<script setup>
import { ref, onMounted, onUnmounted } from 'vue'
// import { Commit } from '../../main/Commit'
import { globals } from '@renderer/globals'

async function getCommits() {
  const branch = globals.selectedBranch // or whatever branch you want to get commits for
  const commits = await window.electron.ipcRenderer.invoke('get-commits', branch)
  const commitsFormatted = commits.map((commit, index) => {
    return {
      id: index,
      sha: shortenSha(commit.sha),
      comment: commit.comment,
      date: shortenDateString(commit.date),
      author: commit.author
    }
  })
  commitsData.value = commitsFormatted
}

const commitsTable = ref('commitsTable')
const commitsData = ref([])
const selectedRows = ref([])

function shortenDateString(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

function shortenSha(sha) {
  return sha.substring(0, 7)
}

onMounted(() => {
  // call the function getCommits()
  getCommits()
  document.addEventListener('keydown', handleKeyboardInput)
})
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboardInput)
})

function selectAll() {
  console.log('selectAll', commitsData)
  commitsTable.value.selectAll()
}

function deselectAll() {
  commitsTable.value.deselectAll()
}
function selectSome() {
  const toSelect = [commitsData.value[0], commitsData.value[2], commitsData.value[5]]
  commitsTable.value.selectRows(toSelect)
  // console.log('selectedRows', selectedRows)
}
function selectOne() {
  const toSelect = [commitsData.value[4]]
  commitsTable.value.selectRows(toSelect)
}
function selectOneOther() {
  const toSelect = [commitsData.value[7]]
  commitsTable.value.selectRows(toSelect)
}
function handleKeyboardInput(event) {
  console.log('shortcut', event.key)
  // const currentRow = selectedRows.value[0]
  // console.log('currentRow', currentRow)
  // return
  if (event.key === 'ArrowDown') {
    if (selectedRows.value.length === 0) {
      const toSelect = [commitsData.value[0]]
      commitsTable.value.selectRows(toSelect)
      return
    }
    const currId = selectedRows.value[0].id
    if (currId === commitsData.value.length - 1) {
      return
    }
    const toSelect = [commitsData.value[currId + 1]]
    commitsTable.value.selectRows(toSelect)
    // prevent the default action (scrolling down) - but would be nice if it did scroll when the selection was not visible anymore
    // event.preventDefault()
  } else if (event.key === 'ArrowUp') {
    if (selectedRows.value.length === 0) {
      const toSelect = [commitsData.value[0]]
      commitsTable.value.selectRows(toSelect)
      return
    }
    const currId = selectedRows.value[0].id
    if (currId === 0) {
      return
    }
    const toSelect = [commitsData.value[currId - 1]]
    commitsTable.value.selectRows(toSelect)
  }
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
      ref="commitsTable"
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
