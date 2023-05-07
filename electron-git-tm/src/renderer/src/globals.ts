import { reactive } from 'vue'
import { Commit } from '../../shared/Commit'
import { BranchOption } from './types/BranchOption'
import { TreeData } from './types/TreeData'

export const globals = reactive({
  // REPO
  repoDir: '' as string,
  get repoDirName(): string {
    return this.repoDir.split('/').pop() || ''
  },
  loadingMsg: '' as string,
  // BRANCHES
  branches: [] as string[],
  selectedBranchOption: { id: 9999, label: '', value: '' } as BranchOption | undefined,
  get selectedBranch(): string {
    if (!this.selectedBranchOption) {
      return ''
    }
    return this.selectedBranchOption.value
  },
  // COMMITS
  commits: [] as Commit[], // this is the array of commits
  selectedCommitRows: [] as Commit[],
  lastCommit: '' as string, // cache this so when user deselects commit table we still have it
  get selectedCommit(): string {
    let result = this.lastCommit
    if (this.selectedCommitRows.length == 0 && this.lastCommit) return result
    this.lastCommit = result = this.selectedCommitRows[0]?.sha // returns undefined if nothing selected
    return result
  },
  get lencommit(): number {
    return this.selectedCommitRows.length
  },
  // TREEVIEW
  treeData: [] as TreeData, // Ref<TreeData> = ref<TreeData>([]),
  expanded: [] as string[], // = ref<string[]>([]), // e.g. ['src', 'main']
  selectedTreeNode: '',
  get selectedTreePath(): string {
    if (!this.selectedTreeNode) {
      return ''
    }
    return this.selectedTreeNode.replace(/^\//, '')
  },
  // DIFFVIEW
  diffHtml: '' as string,
  // FILEVIEW
  scroll_is_for_path: '',
  scrollPos: 0 as number,
  scrollPosX: 0 as number,
  lineTo: 0 as number
})
