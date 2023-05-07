<script setup lang="ts">
import { ref, watch } from 'vue'
import { globals, debug } from '@renderer/globals'
import { Commit } from '../../../shared/Commit'

const myiframe = ref()

watch([(): string => globals.selectedCommit], async () => {
  if (globals.selectedCommit == undefined) return
  getDiff()
})

async function getDiff(): Promise<void> {
  if (debug.event_flow) console.log('getting diff...', globals.selectedCommit)
  const commit: Commit = globals.selectedCommitRows[0]
  if (!commit) {
    return
  }
  const sha = commit.sha
  const diffHtml: string = await window.electron.ipcRenderer.invoke('generate-diff', sha)
  myiframe.value.srcdoc = diffHtml
}

// In the outer HTML of your app's render process
window.addEventListener('message', (event) => {
  console.log('Received message from iframe:', event.data)

  // TODO: IMPLEMENT THIS

  // # print("Script message received (Diff Panel)", event.GetString())
  // if event.GetString()[0] == '{':
  //     command_obj = json.loads(event.GetString())
  //     if command_obj['command'] == 'jump_to_file':
  //         filePath = command_obj['filePath']
  //         lineNum = command_obj['lineNum']
  //         # print("Jump to file command received", filePath, lineNum)

  //         # Load the file contents into the content view and jump to the specified line
  //         contents = get_file_contents(current_commit, filePath)

  //         if event_debug:
  //             print('\n⚡️file_selected (DiffPanel, jump_to_file)')
  //         pub.sendMessage('file_selected', path=filePath, contents=contents, line_to=lineNum)

  //         # Tell the treeview to select the item
  //         if event_debug:
  //             print('\n⚡️select_treeview_item (DiffPanel, jump_to_file)')
  //         pub.sendMessage('select_treeview_item', path=filePath)

})
</script>

<template>
  <iframe ref="myiframe" width="100%" height="100%" frameborder="0"></iframe>
</template>
