import { exec } from 'child_process'
import util from 'util'

export async function getFilesInRepo(commit): Promise<string[]> {
  const execPromisified = util.promisify(exec)
  const command = ['git', 'ls-tree', '-r', '--full-tree', '--name-only', commit]
  console.log(`getFilesInRepo called: ${command.join(' ')}`)
  try {
    const { stdout } = await execPromisified(command.join(' '))
    const output = stdout.trim()
    console.log(`Files at commit ${commit}: ${output}`)
    return output.split('\n')
  } catch (e) {
    console.log(`Error fetching files: ${(e as Error).message}`)
    return []
  }
}
