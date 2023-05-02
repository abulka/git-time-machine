import { execSync } from 'child_process'
import { repoDir } from './globalsMain'

export function getFileContents(commit, filePath): string {
  // TODO sha is not long enough

  const options = { cwd: repoDir }
  const command = ['git', 'show', `${commit}:'${filePath}'`]
  try {
    const result = execSync(command.join(' '), options).toString()
    return result
  } catch (e) {
    console.log(`Error getting file contents: ${e}`)
    return 'File does not exist at this commit.'
  }
}
