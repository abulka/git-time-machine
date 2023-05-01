import { exec } from 'child_process'
import util from 'util'

export async function getBranches(): Promise<string[]> {
  // get the list of branches using the git command

  // process.chdir('/Users/andy/Devel/git-time-machine/');
  // process.chdir('/Users/andy/Devel/pynsource/');

  try {
    const execPromisified = util.promisify(exec)
    const git_command = ['git', 'branch']
    const branches = (await execPromisified(git_command.join(' '))).stdout
      .split('\n')
      .map((branch) => branch.trim())
      .filter((branch) => branch !== '')
    return branches
  } catch (e) {
    console.log(`Error fetching branches: ${(e as Error).message}`)
    return []
  }
}
