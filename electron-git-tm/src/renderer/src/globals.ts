import { reactive } from 'vue'

interface BranchOption {
  label: string
  value: string
}

// Identifiers imported from other modules cannot be reassigned.
// so we wrap in a object and export that object instead - CAN change the innards of the object!
// We also make this reactive so that it plays nice with vue.
// TIP: reactive variables are never 'undefined', as vue will set them to a special proxy object
export const globals = reactive({
  silly: 'global sillyness',
  selectedBranchOption: { label: 'main', value: 'main' }, // BranchOption
  get selectedBranch() {
    return this.selectedBranchOption.value
  },
  commitsData: [] // this is the array of commits
})
