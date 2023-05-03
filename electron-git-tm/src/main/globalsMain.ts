export let repoDir = '/Users/andy/Devel/pynsource/'
export let preferences = {
  theme: 'dark',
  fontSize: 14,
  repoDir: repoDir,
}

// Setters

export function setRepoDir(dir): void {
  repoDir = dir
  preferences.repoDir = repoDir
}

export function initPreferences(prefs): void {
  preferences = prefs
  if (preferences.repoDir != '') setRepoDir(preferences.repoDir)
}
