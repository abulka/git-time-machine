import fs from 'fs';
import path from 'path';
import { app } from 'electron';

export function getPrefsPath(): string {
  const preferencesPath = path.join(app.getPath('userData'), 'prefs');
  // console.log(`preferencesPath is ${preferencesPath}`)
  // Create the preferences directory if it doesn't exist
  if (!fs.existsSync(preferencesPath)) {
    fs.mkdirSync(preferencesPath);
    console.log(`${preferencesPath} created`);
  }
  return preferencesPath;
}
