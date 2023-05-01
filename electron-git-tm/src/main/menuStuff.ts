import { Menu, MenuItemConstructorOptions } from 'electron'
import { changeCwd } from './changeDir'

export function setupMenu(mainWindow): void {
  const menuTemplate: MenuItemConstructorOptions[] = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Change Directory',
          click: async (): Promise<void> => {
            const result = await changeCwd()
            if (result.success) {
              const { webContents } = mainWindow
              webContents.send('shouldGetBranches') // invoke-async-function - or not async?
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
