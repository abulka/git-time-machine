import { execSync } from 'child_process'

export function getFileContents(commit, filePath): string {
  
  // TODO there's something about the path that's not working
  // git show 7e40d78:'package.json'
  // fatal: path 'electron-git-tm/package.json' exists, but not 'package.json'
  // ALSO the sha is not long enough
  
  const command = ['git', 'show', `${commit}:'${filePath}'`]
  console.log(`getFileContents called: ${command.join(' ')}`)
  try {
    const result = execSync(command.join(' ')).toString()
    console.log(`File contents: ${result}`)
    return result
  } catch (e) {
    console.log(`Error getting file contents: ${e}`)
    return 'File does not exist at this commit.'
  }
}
