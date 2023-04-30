<!-- eslint-disable @typescript-eslint/explicit-function-return-type -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Commit } from '../../../shared/Commit'
import { globals } from '@renderer/globals'

// The watch function in Vue takes two main parameters: a function that returns
// the value to watch, and a callback function that is called when the value
// changes.
watch(
  () => globals.selectedBranch,
  async () => {
    await getCommits()
  }
)

async function getCommits(): Promise<void> {
  const branch = globals.selectedBranch
  const commits = await window.electron.ipcRenderer.invoke('get-commits', branch)
  const commitsFormatted: Commit[] = commits.map((commit, index) => {
    const _commit: Commit = {
      id: index,
      sha: shortenSha(commit.sha),
      comment: commit.comment,
      date: shortenDateString(commit.date),
      author: commit.author
    }
    return _commit
  })
  globals.commitsData = commitsFormatted

  // select the latest commit row
  const toSelect = [globals.commitsData[0]]

  commitsTable.value.selectRows(toSelect)
}

const commitsTable = ref()

function shortenDateString(dateString) {
  const date = new Date(dateString)
  return date.toLocaleDateString()
}

function shortenSha(sha) {
  return sha.substring(0, 7)
}

onMounted(() => {
  document.addEventListener('keydown', handleKeyboardInput)
})
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboardInput)
})

// function selectAll() {
//   console.log('selectAll', globals.commitsData)
//   commitsTable.value.selectAll()
// }
// function deselectAll() {
//   commitsTable.value.deselectAll()
// }
// function selectSome() {
//   const toSelect = [globals.commitsData[0], globals.commitsData[2], globals.commitsData[5]]
//   commitsTable.value.selectRows(toSelect)
// }
// function selectOne() {
//   const toSelect = [globals.commitsData[4]]
//   commitsTable.value.selectRows(toSelect)
// }
// function selectOneOther() {
//   const toSelect = [globals.commitsData[7]]
//   commitsTable.value.selectRows(toSelect)
// }

function handleKeyboardInput(event) {
  // console.log('shortcut', event.key)

  // const currentRow = globals.selectedCommitRows.value[0]
  // console.log('currentRow', currentRow)
  // return
  if (event.key === 'ArrowDown') {
    if (globals.selectedCommitRows.length === 0) {
      const toSelect: Commit[] = [globals.commitsData[0]]
      commitsTable.value.selectRows(toSelect)
      return
    }
    const currId = globals.selectedCommitRows[0].id
    if (currId === globals.commitsData.length - 1) {
      return
    }
    const toSelect = [globals.commitsData[currId + 1]]
    commitsTable.value.selectRows(toSelect)
    // prevent the default action (scrolling down) - but would be nice if it did scroll when the selection was not visible anymore
    // event.preventDefault()
  } else if (event.key === 'ArrowUp') {
    if (globals.selectedCommitRows.length === 0) {
      const toSelect: Commit[] = [globals.commitsData[0]]
      commitsTable.value.selectRows(toSelect)
      return
    }
    const currId = globals.selectedCommitRows[0].id
    if (currId === 0) {
      return
    }
    const toSelect = [globals.commitsData[currId - 1]]
    commitsTable.value.selectRows(toSelect)
  }
}

function stateChanged(state) {
  // console.log(
  //   'stateChanged',
  //   state.selectedRows,
  //   'selectedRows.length',
  //   state.selectedRows.length,
  //   'globals.selectedCommitRows',
  //   globals.selectedCommitRows,
  //   globals.selectedCommitRows.length,
  //   'lencommit',
  //   globals.lencommit,
  //   'commit',
  //   globals.commit
  // )
  globals.selectedCommitRows = state.selectedRows
  // if (state.selectedRows.length != 0)
  //   console.log('state.selectedRows.length != 0')

  // if (state.selectedRows.length === 0)
  // // reselect the first row
  // {
  //   const toSelect = [globals.commitsData[0]]
  //   console.log('toSelect', toRaw(commitsTable), toSelect)
  //   // commitsTable.value.selectRows(toSelect)
  // }

  // "globals.selectedCommitRows = $event.selectedRows"
}
</script>

<template>
  <!-- eslint-disable vue/attribute-hyphenation -->
  <!-- eslint-disable vue/v-on-event-hyphenation -->

  <!-- https://vue-smart-table.netlify.app/selection.html#head-scoped-slot for doco on this table component -->
  <div>
    <!-- <div class="flex justify-between mb-5">
      <button @click="selectAll">Select All</button>
      <button @click="deselectAll">Deselect All</button>
      <button @click="selectSome">Select Some</button>
      <button @click="selectOne">Select One</button>
      <button @click="selectOneOther">Select One Other</button>
      <button @click="getCommits">Get Commits</button>
    </div> -->

    <VTable
      ref="commitsTable"
      :data="globals.commitsData"
      selectionMode="single"
      selectedClass="selected-row"
      @stateChanged="stateChanged"
    >
      <!-- <template #head="{ allRowsSelected, selectAll, deselectAll, toggleAllRows, selectedRows }"> -->
      <template #head="{}">
        <!-- {{ allRowsSelected }}
        {{ selectedRows }} -->
        <th>Sha</th>
        <th>Comment</th>
        <th>Date</th>
        <th>Author</th>
      </template>
      <template #body="{ rows }">
        <!-- <VTr v-for="row in rows" :key="row.guid" v-slot="{ isSelected, toggle }" :row="row"> -->
        <VTr v-for="row in rows" :key="row.guid" v-slot="{}" :row="row">
          <td>{{ row.sha }}</td>
          <td>{{ row.comment }}</td>
          <td>{{ row.date }}</td>
          <td>{{ row.author }}</td>
          <!-- <td>{{ isSelected == undefined }}</td> -->
        </VTr>
      </template>
    </VTable>

    <strong>Selected:</strong>
    <div v-if="globals.selectedCommitRows.length === 0">No rows selected</div>
    <ul>
      <li v-for="selected in globals.selectedCommitRows" :key="selected.sha">
        {{ selected.sha }}
        {{ selected.id }}
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
