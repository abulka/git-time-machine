import { reactive } from 'vue'
import { Commit } from '../../shared/Commit'
import { BranchOption } from './types/BranchOption'
import { TreeData } from './types/TreeData'

// Identifiers imported from other modules cannot be reassigned.
// so we wrap in a object and export that object instead - CAN change the innards of the object!
// We also make this reactive so that it plays nice with vue.
// TIP: reactive variables are never 'undefined', as vue will set them to a special proxy object
export const globals = reactive({
  silly: 'global sillyness',
  // REPO
  repoDir: '' as string,
  get repoDirName(): string {
    return this.repoDir.split('/').pop() || ''
  },
  repoRefreshNeeded: false as boolean,
  loadingMsg: '' as string,
  // BRANCHES
  selectedBranchOption: { id: 9999, label: '', value: '' } as BranchOption,
  get selectedBranch(): string {
    return this.selectedBranchOption.value
  },
  branches: [] as string[],
  // COMMITS
  commitsData: [] as Commit[], // this is the array of commits
  selectedCommitRows: [] as Commit[],
  lastCommit: '' as string, // cache this so when user deselects commit table we still have it
  get commit(): string {
    let result = this.lastCommit
    if (this.selectedCommitRows.length == 0 && this.lastCommit) return result
    this.lastCommit = result = this.selectedCommitRows[0]?.sha // returns undefined if nothing selected
    return result
  },
  get lencommit(): number {
    return this.selectedCommitRows.length
  },
  // TREEVIEW
  selectedTreeNode: '',
  get selectedTreePath(): string {
    if (!this.selectedTreeNode) {
      return ''
    }
    return this.selectedTreeNode.replace(/^\//, '')
  },
  treeData: [] as TreeData, // Ref<TreeData> = ref<TreeData>([]),
  expanded: [] as string[], // = ref<string[]>([]), // e.g. ['src', 'main']
  // FILEVIEW
  scroll_is_for_path: '',
  scrollPos: 0 as number,
  scrollPosX: 0 as number,
  lineTo: 0 as number
})
