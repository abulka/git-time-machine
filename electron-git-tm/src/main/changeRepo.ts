import { setRepoDir, repoDir } from './globalsMain'
import { loadPreferences, savePreferences } from './preferences'
const dialog = require('electron').dialog

export async function changeCwd(mainWindow): Promise<{ success: boolean }> {
  try {
    // Show the directory selection dialog
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory']
    })
    if (result.canceled) return { success: false }

    // Set the repo directory for the main process, used by all git calls
    const selectedDirectory = result.filePaths[0]
    setRepoDir(selectedDirectory)
    savePreferences()

    // Notify the renderer process that the directory has changed
    const { webContents } = mainWindow
    webContents.send('repoChanged', repoDir)

    return { success: true }
  } catch (error) {
    console.error(error)
    return { success: false }
  }
}

export async function toggleRepo(mainWindow): Promise<{ success: boolean }> {
  // Quick way of toggling through various repos for testing
  switch (repoDir) {
    case '/Users/andy/Devel/pynsource':
      setRepoDir('/Users/andy/Devel/alsm')
      break
    case '/Users/andy/Devel/alsm':
      setRepoDir('/Users/andy/Devel/dalai-llama')
      break
    case '/Users/andy/Devel/dalai-llama':
      setRepoDir('/Users/andy/Devel/pynsource')
      break
    default:
      setRepoDir('/Users/andy/Devel/pynsource')
      break
  }
  // Notify the renderer process that the directory has changed
  const { webContents } = mainWindow
  webContents.send('repoChanged', repoDir)
  return { success: true }
}

export function startupBusinessLogic(mainWindow): void {
  loadPreferences()

  if (repoDir === '') {
    console.log(`${repoDir} is empty, not bothering to get branches`)
    return
  }

  // Notify the renderer process of initial repo directory
  const { webContents } = mainWindow
  webContents.send('repoChanged', repoDir)
}
