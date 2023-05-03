import fs from 'fs'
import path from 'path'
import { app } from 'electron'
import { initPreferences, preferences } from './globalsMain'

// Store preferences in the user data directory 'prefs'
// e.g. /Users/andy/Library/Application Support/git-time-machine/prefs

const PREFS_DIR = 'prefs'
const PREFS_JSON = 'preferences.json'

function getPrefsDir(): string {
  const dir = path.join(app.getPath('userData'), PREFS_DIR)

  // Create the preferences directory if it doesn't exist
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir)
    console.log(`${dir} created`)
  }
  return dir
}

function getPreferencesPath(): string {
  const prefsDir = getPrefsDir()
  const prefsPath = path.join(prefsDir, PREFS_JSON)
  return prefsPath
}

export function savePreferences(): void {
  const preferencesPath = getPreferencesPath()
  fs.writeFileSync(preferencesPath, JSON.stringify(preferences))
  // console.log(`${prefsPath} written`)
}

export function loadPreferences(): void {
  const preferencesPath = getPreferencesPath()
  let _preferences = {}
  try {
    _preferences = JSON.parse(fs.readFileSync(preferencesPath, 'utf8'))
    initPreferences(_preferences)
  } catch (err) {
    console.error('Error parsing preferences.json', preferencesPath)
  }
}
