import { Menu, MenuItem, MenuItemConstructorOptions } from 'electron'
import { changeCwd } from './changeRepo'

export function setupMenu(mainWindow): void {
  // Get the existing application menu
  const existingMenu = Menu.getApplicationMenu()
  if (!existingMenu) {
    console.error('No existing menu')
    return
  }

  // Loop through existing menu and print out all the ids
  // existingMenu.items.forEach((item) => {
  //   console.log(item.id, item.label, item.role)
  // })

  // Find the "File" menu
  // const fileMenu = existingMenu.getMenuItemById('file')
  const fileMenu = findMenuItemByLabel('File')
  if (!fileMenu) {
    console.error('No "File" menu')
    return
  }
  if (!fileMenu.submenu) {
    console.error('No "File" submenu')
    return
  }

  // Add the "Change Repository Directory" menu item to the "File" menu
  const changeRepoItem: MenuItemConstructorOptions = {
    label: 'Change Repository Directory',
    accelerator: 'CmdOrCtrl+O',
    click: async (): Promise<void> => {
      const result = await changeCwd(mainWindow)
      if (!result.success) {
        console.error('Cwd change failed')
      }
    }
  }
  // fileMenu.submenu.append(new MenuItem(changeRepoItem))
  fileMenu.submenu.insert(0, new MenuItem(changeRepoItem))

  // Set the updated application menu
  Menu.setApplicationMenu(existingMenu)
}

function findMenuItemByLabel(label: string): Electron.MenuItem | null {
  const menu = Menu.getApplicationMenu()
  if (!menu) {
    return null
  }

  function searchMenuItems(items: Electron.MenuItem[]): Electron.MenuItem | null {
    for (const item of items) {
      if (item.label === label) {
        return item
      }

      if (item.submenu) {
        const found = searchMenuItems(item.submenu.items)
        if (found) {
          return found
        }
      }
    }

    return null
  }

  return searchMenuItems(menu.items)
}

// import { Menu, MenuItemConstructorOptions } from 'electron'
// import { changeCwd } from './changeRepo'

// export function setupMenu(mainWindow): void {
//   const menuTemplate: MenuItemConstructorOptions[] = [
//     {
//       label: 'File',
//       submenu: [
//         {
//           label: 'Change Repository Directory',
//           accelerator: 'CmdOrCtrl+O',
//           click: async (): Promise<void> => {
//             const result = await changeCwd(mainWindow)
//             if (!result.success) {
//               console.error('Cwd change failed')
//             }
//           }
//         },
//         { type: 'separator' },
//         { role: 'quit' }
//       ]
//     }
//   ]

//   const menu = Menu.buildFromTemplate(menuTemplate)
//   Menu.setApplicationMenu(menu)
// }
