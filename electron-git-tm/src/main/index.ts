import { app, shell, BrowserWindow } from 'electron'
import * as path from 'path'
import { electronApp, optimizer, is } from '@electron-toolkit/utils'
const { ipcMain } = require('electron')
import { generateHtml } from './generateHtml'
import { getBranches } from './getBranches'
import { getCommitsForBranch } from './getCommits'
import { getRepoFileTree } from './getFileTree'
import { getPreviousCommit } from './getDiff'

// ipc

import { contextBridge } from 'electron'
import { electronAPI } from '@electron-toolkit/preload'

function createWindow(): void {
  // Create the browser window.
  const mainWindow = new BrowserWindow({
    width: 900,
    height: 670,
    show: false,
    autoHideMenuBar: true,
    ...(process.platform === 'linux'
      ? {
          icon: path.join(__dirname, '../../build/icon.png')
        }
      : {}),
    webPreferences: {
      preload: path.join(__dirname, '../preload/index.js'),
      sandbox: false
    }
  })

  mainWindow.on('ready-to-show', () => {
    mainWindow.show()
  })

  mainWindow.webContents.setWindowOpenHandler((details) => {
    shell.openExternal(details.url)
    return { action: 'deny' }
  })

  // HMR for renderer base on electron-vite cli.
  // Load the remote URL for development or the local html file for production.
  if (is.dev && process.env['ELECTRON_RENDERER_URL']) {
    mainWindow.loadURL(process.env['ELECTRON_RENDERER_URL'])
  } else {
    mainWindow.loadFile(path.join(__dirname, '../renderer/index.html'))
  }

  if (process.contextIsolated) {
    console.log('context is isolated, exposing electronAPI to contextBridge')
    try {
      contextBridge.exposeInMainWorld('electron', electronAPI)
    } catch (error) {
      console.error(error)
    }
  } else {
    // ---> This is what typically runs... <---
    // console.log('context is not isolated, setting window.electron = electronAPI')
    mainWindow.electron = electronAPI
  }

}

// This method will be called when Electron has finished
// initialization and is ready to create browser windows.
// Some APIs can only be used after this event occurs.
app.whenReady().then(() => {
  // Set app user model id for windows
  electronApp.setAppUserModelId('com.electron')

  // Default open or close DevTools by F12 in development
  // and ignore CommandOrControl + R in production.
  // see https://github.com/alex8088/electron-toolkit/tree/master/packages/utils
  app.on('browser-window-created', (_, window) => {
    optimizer.watchWindowShortcuts(window)
  })

  createWindow()

  app.on('activate', function () {
    // On macOS it's common to re-create a window in the app when the
    // dock icon is clicked and there are no other windows open.
    if (BrowserWindow.getAllWindows().length === 0) createWindow()
  })
})

// Quit when all windows are closed, except on macOS. There, it's common
// for applications and their menu bar to stay active until the user quits
// explicitly with Cmd + Q.
app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit()
  }
})

// In this file you can include the rest of your app"s specific main process
// code. You can also put them in separate files and require them here.

// FUNCTIONALITY BEGINS


ipcMain.handle('ping', (event, name) => {
  return `Main process handle(): Hello, ${name}! - pong from main`;
});

ipcMain.on('say', (event, what) => {
  console.log('Main process on()', what)
})

console.log('hello from main')
getPreviousCommit('HEAD').then((commit) => {
  console.log('previous commit:', commit)
})

ipcMain.handle('get-branches', async (event) => {
  const branches: string[] = await getBranches()
  return branches
})

ipcMain.handle('get-commits', async (event, branch) => {
  const commits = await getCommitsForBranch(branch)
  return commits
})  

ipcMain.handle('get-files', async (event, commit) => {
  const files = await getRepoFileTree(commit)
  return files
})

// ipcMain.handle('generate-html', (event, path, sourceFileContents, scrollTo, lineTo) => {
//   const htmlStr = generateHtml(path, sourceFileContents, scrollTo, lineTo)
//   return htmlStr
// })
ipcMain.handle('generate-html', (event, commit, fileName) => {
  const htmlStr = generateHtml(commit, fileName)
  return htmlStr
})
