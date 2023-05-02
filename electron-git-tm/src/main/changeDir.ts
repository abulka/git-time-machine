import { setRepoDir } from './globalsMain'
const dialog = require('electron').dialog

export async function changeCwd(): Promise<{ success: boolean }> {
  try {
    // Show the directory selection dialog
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory']
    })

    if (!result.canceled) {
      const selectedDirectory = result.filePaths[0]

      // Change the current working directory to the selected directory
      // process.chdir(selectedDirectory)
      setRepoDir(selectedDirectory)

      return { success: true }
    } else {
      return { success: false }
    }
  } catch (error) {
    console.error(error)
    return { success: false }
  }
}
