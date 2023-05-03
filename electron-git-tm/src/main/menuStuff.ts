import { Menu, MenuItemConstructorOptions } from 'electron'
import { changeCwd } from './changeRepo'

export function setupMenu(mainWindow): void {
  const menuTemplate: MenuItemConstructorOptions[] = [
    {
      label: 'File',
      submenu: [
        {
          label: 'Change Repository Directory',
          accelerator: 'CmdOrCtrl+O',
          click: async (): Promise<void> => {
            const result = await changeCwd(mainWindow)
            if (!result.success) {
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
