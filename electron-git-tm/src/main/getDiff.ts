import { exec } from 'child_process'
import util from 'util'

export async function getPreviousCommit(currentCommit): Promise<string | null> {
  const execPromisified = util.promisify(exec)
  const gitCommand = ['git', 'rev-list', currentCommit]
  try {
    const { stdout } = await execPromisified(gitCommand.join(' '))
    const commits: string[] = stdout.toString().split('\n')

    // return the previous commit in the list (i.e., the commit before current_commit)
    if (commits.length > 1) {
      return commits[1]
    } else if (commits.length === 1) {
      return null
    } else {
      throw new Error('No commits found in repository')
    }
  } catch (e) {
    console.log(`Error fetching previous commit: ${(e as Error).message}`)
    return null
  }
}
