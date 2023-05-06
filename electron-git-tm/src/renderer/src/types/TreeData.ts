export interface TreeDataItem {
  label: string
  icon?: string
  children: TreeDataItem[]
  fullPath: string
}

export type TreeData = TreeDataItem[]
