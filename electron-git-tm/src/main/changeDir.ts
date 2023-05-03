import fs from 'fs'
import path from 'path'
import { setRepoDir, repoDir, preferences, setPreferences } from './globalsMain'
import { getPrefsPath } from './getPrefsPath'
const dialog = require('electron').dialog

export async function changeCwd(mainWindow): Promise<{ success: boolean }> {
  try {
    // Show the directory selection dialog
    const result = await dialog.showOpenDialog({
      properties: ['openDirectory']
    })

    if (!result.canceled) {
      const selectedDirectory = result.filePaths[0]

      setRepoDir(selectedDirectory)

      const { webContents } = mainWindow
      webContents.send('shouldGetBranches', repoDir) // invoke-async-function - or not async?

      // save preferences
      preferences.repoDir = repoDir
      const preferencesPath = getPrefsPath()
      const prefsPath = path.join(preferencesPath, 'preferences.json')
      fs.writeFileSync(prefsPath, JSON.stringify(preferences))
      // console.log(`${prefsPath} written`)

      return { success: true }
    } else {
      return { success: false }
    }
  } catch (error) {
    console.error(error)
    return { success: false }
  }
}

export function startupBusinessLogic(mainWindow): void {
  const { webContents } = mainWindow

  // read preferences from file
  const preferencesPath = getPrefsPath()
  const prefsPath = path.join(preferencesPath, 'preferences.json')
  let _preferences = {}
  try {
    _preferences = JSON.parse(fs.readFileSync(prefsPath, 'utf8'))
    console.log('preferences', _preferences)
    setPreferences(_preferences)
  } catch (err) {
    console.error('Error parsing preferences.json', prefsPath)
  }

  if (repoDir === '') {
    console.log(`${repoDir} is empty, not bothering to get branches`)
  }
  webContents.send('shouldGetBranches', repoDir) // invoke-async-function - or not async?
}
