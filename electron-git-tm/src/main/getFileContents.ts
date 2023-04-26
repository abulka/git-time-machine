import { execSync } from 'child_process'

export function getFileContents(commit, filePath): string {
  // TODO sha is not long enough

  const command = ['git', 'show', `${commit}:'${filePath}'`]
  try {
    const result = execSync(command.join(' ')).toString()
    return result
  } catch (e) {
    console.log(`Error getting file contents: ${e}`)
    return 'File does not exist at this commit.'
  }
}
