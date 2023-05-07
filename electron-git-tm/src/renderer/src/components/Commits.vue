<!-- eslint-disable @typescript-eslint/explicit-function-return-type -->
<script setup lang="ts">
import { ref, onMounted, onUnmounted, watch } from 'vue'
import { Commit } from '../../../shared/Commit'
import { globals } from '@renderer/globals'

watch([(): Commit[] => globals.commits], () => {
  // select the 'top-most' commit in the table
  const toSelect = [globals.commits[0]]
  commitsTable.value.selectRows(toSelect)
})

const commitsTable = ref()

onMounted(() => {
  document.addEventListener('keydown', handleKeyboardInput)
})
onUnmounted(() => {
  document.removeEventListener('keydown', handleKeyboardInput)
})

function handleKeyboardInput(event) {
  const commits = globals.commits
  const selectedCommitRows = globals.selectedCommitRows

  if (event.key === 'ArrowDown') {
    const currId = selectedCommitRows.length ? selectedCommitRows[0].id : -1
    const nextId = currId + 1
    if (nextId < commits.length) {
      const toSelect: Commit[] = [commits[nextId]]
      commitsTable.value.selectRows(toSelect)
    }
  } else if (event.key === 'ArrowUp') {
    const currId = selectedCommitRows.length ? selectedCommitRows[0].id : 1
    const prevId = currId - 1
    if (prevId >= 0) {
      const toSelect: Commit[] = [commits[prevId]]
      commitsTable.value.selectRows(toSelect)
    }
  }
}

function stateChanged(state) {
  // Avoid bug where undefined is selected
  if (state.selectedRows.length === 1 && state.selectedRows[0] == undefined) return

  globals.selectedCommitRows = state.selectedRows as Commit[]
}
</script>

<template>
  <!-- eslint-disable vue/attribute-hyphenation -->
  <!-- eslint-disable vue/v-on-event-hyphenation -->
  <div>
    <VTable
      ref="commitsTable"
      :data="globals.commits"
      selectionMode="single"
      selectedClass="selected-row"
      @stateChanged="stateChanged"
    >
      <template #head="{}">
        <th>Sha</th>
        <th>Comment</th>
        <th>Date</th>
        <th>Author</th>
      </template>
      <template #body="{ rows }">
        <VTr v-for="row in rows" :key="row.guid" v-slot="{}" :row="row">
          <td>{{ row.sha }}</td>
          <td>{{ row.comment }}</td>
          <td>{{ row.date }}</td>
          <td>{{ row.author }}</td>
        </VTr>
      </template>
    </VTable>
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
