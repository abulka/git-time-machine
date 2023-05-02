import { exec } from 'child_process'
import util from 'util'
import { repoDir } from './globalsMain'

export async function getRepoFileTree(commit): Promise<string[]> {
  const execPromisified = util.promisify(exec)
  const command = ['git', 'ls-tree', '-r', '--full-tree', '--name-only', commit]
  const options = { cwd: repoDir }
  try {
    const { stdout } = await execPromisified(command.join(' '), options)
    const output = stdout.trim()
    return output.split('\n')
  } catch (e) {
    console.log(`Error fetching files: ${(e as Error).message}`)
    return []
  }
}
