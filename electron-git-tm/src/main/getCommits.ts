import { exec } from 'child_process'
import util from 'util'
import { Commit } from './Commit'

// return array of Commits

export async function getCommitsForBranch(branch): Promise<Commit[]> {
  try {
    // Fetch the commit hashes for the specified branch
    const execPromisified = util.promisify(exec)

    const command = `git log ${branch} --format=%H///%cd///%an///%s`
    const commitInfo = (await execPromisified(command)).stdout.split('\n')

    const commits: Commit[] = []
    for (const info of commitInfo) {
      // split on '///' and get the sha, date, author, and comment
      const [sha, date, author, comment] = info.split('///')
      commits.push(new Commit(sha, date, author, comment))
    }

    return commits
  } catch (e) {
    // Handle Git errors by returning an empty list
    console.log(`Error fetching commits for branch '${branch}': ${(e as Error).message}`)
    return []
  }
}

// testing only
// getCommitsForBranch('main')
//   .then((commits) => {
//     console.log('Commits retrieved:', commits)
//   })
//   .catch((error) => {
//     console.error('Error retrieving commits:', error)
//   })
