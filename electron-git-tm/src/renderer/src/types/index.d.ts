import { electronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electronAPI: typeof electronAPI & {
      shouldGetBranches: (callback: (event: unknown) => void) => void
    }
  }
}
