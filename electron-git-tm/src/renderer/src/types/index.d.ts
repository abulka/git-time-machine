import { electronAPI } from '@electron-toolkit/preload'

declare global {
  interface Window {
    electronAPI: typeof electronAPI & {
      repoChanged: (callback: (event: unknown, repoDir: string) => void) => void
    }
  }
}
