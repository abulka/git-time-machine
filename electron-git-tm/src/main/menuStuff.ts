import { Menu, MenuItemConstructorOptions } from 'electron'
import { changeCwd } from './changeDir'
import { repoDir } from './globalsMain'

export function startupBusinessLogic(mainWindow): void {
  const { webContents } = mainWindow
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
