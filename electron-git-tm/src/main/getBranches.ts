import { exec } from 'child_process'
import util from 'util'
import { repoDir } from './globalsMain'

export async function getBranches(): Promise<string[]> {
  // get the list of branches using the git command

  const options = { cwd: repoDir }
  const execPromisified = util.promisify(exec)
  const git_command = ['git', 'branch']

  try {
    const branches = (await execPromisified(git_command.join(' '), options)).stdout
      .split('\n')
      .map((branch) => branch.trim())
      .filter((branch) => branch !== '')
    return branches
  } catch (e) {
    console.log(`Error fetching branches: ${(e as Error).message}`)
    return []
  }
}
