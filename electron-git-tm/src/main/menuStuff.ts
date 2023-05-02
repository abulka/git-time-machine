import { Menu, MenuItemConstructorOptions } from 'electron'
import { changeCwd } from './changeDir'
import { repoDir, preferences, setPreferences } from './globalsMain'
import fs from 'fs'
import path from 'path'
import { app } from 'electron'

export function startupBusinessLogic(mainWindow): void {
  const { webContents } = mainWindow

  // read preferences from file
  const preferencesPath = getPrefsPath()
  const prefsPath = path.join(preferencesPath, 'preferences.json')
  let _preferences = {}
  try {
    _preferences = JSON.parse(fs.readFileSync(prefsPath, 'utf8'));
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

function getPrefsPath(): string {
  const preferencesPath = path.join(app.getPath('userData'), 'prefs')
  console.log(`preferencesPath is ${preferencesPath}`)

  // Create the preferences directory if it doesn't exist
  if (!fs.existsSync(preferencesPath)) {
    fs.mkdirSync(preferencesPath)
    console.log(`${preferencesPath} created`)
  }
  return preferencesPath
}

export function setupMenu(mainWindow): void {
  const menuTemplate: MenuItemConstructorOptions[] = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Change Directory',
          accelerator: 'CmdOrCtrl+O',
          click: async (): Promise<void> => {
            const result = await changeCwd()
            // TODO move this code to changeDir.ts
            if (result.success) {
              const { webContents } = mainWindow
              webContents.send('shouldGetBranches', repoDir) // invoke-async-function - or not async?
              // save preferences
              preferences.repoDir = repoDir
              const preferencesPath = getPrefsPath()
              const prefsPath = path.join(preferencesPath, 'preferences.json')
              fs.writeFileSync(prefsPath, JSON.stringify(preferences))
              console.log(`${prefsPath} written`)
            } else {
              console.error('Cwd change failed')
            }
          }
        },
        { type: 'separator' },
        { role: 'quit' }
      ]
    }
  ]

  const menu = Menu.buildFromTemplate(menuTemplate)
  Menu.setApplicationMenu(menu)
}
