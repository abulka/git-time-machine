import { electronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electronAPI: typeof electronAPI & {
      shouldGetBranches: (callback: (event: unknown, repoDir: string) => void) => void
    }
  }
}
