export let repoDir = '/Users/andy/Devel/pynsource/'

export function setRepoDir(dir): void {
  repoDir = dir
}

export let preferences = {
  theme: 'dark',
  fontSize: 14,
  repoDir: repoDir,
}

export function setPreferences(prefs): void {
  preferences = prefs
  if (preferences.repoDir != '') setRepoDir(preferences.repoDir)
}
