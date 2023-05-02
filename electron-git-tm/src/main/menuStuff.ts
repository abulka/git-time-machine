import { Menu, MenuItemConstructorOptions } from 'electron'
import { changeCwd } from './changeDir'
import { repoDir, preferences, setPreferences } from './globalsMain'
import fs from 'fs'
import path from 'path'

export function startupBusinessLogic(mainWindow): void {
  const { webContents } = mainWindow

  // read preferences from file
  const prefsPath = path.join(__dirname, 'preferences.json');
  let _preferences = {}
  try {
    _preferences = JSON.parse(fs.readFileSync(prefsPath, 'utf8'));
    console.log('preferences', _preferences)
    setPreferences(_preferences)
  } catch (err) {
    console.error('Error parsing preferences.json', err)
  }

  if (repoDir === '') {
    console.log(`${repoDir} is empty, not bothering to get branches`)
  }
  webContents.send('shouldGetBranches', repoDir) // invoke-async-function - or not async?
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
              const prefsPath = path.join(__dirname, 'preferences.json')
              fs.writeFileSync(prefsPath, JSON.stringify(preferences))
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
