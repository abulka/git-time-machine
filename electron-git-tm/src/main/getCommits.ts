import { exec } from 'child_process'
import util from 'util'
import { Commit } from './Commit'

// return array of Commits

export let commits: Commit[] = []

export async function getCommitsForBranch(branch): Promise<Commit[]> {
  try {
    // Fetch the commit hashes for the specified branch
    const execPromisified = util.promisify(exec)

    if (branch.includes('(HEAD detached at')) {
      // we are in detached head mode, so get the commit hash from the branch name
      branch = branch.split(' ')[3].replace(')', '')
    }

    const command = `git log ${branch} --format=%H///%cd///%an///%s`
    const commitInfo = (await execPromisified(command)).stdout.split('\n')

    const _commits: Commit[] = []
    let id = 0
    for (const info of commitInfo) {
      // split on '///' and get the sha, date, author, and comment
      const [sha, date, author, comment] = info.split('///')
      _commits.push(new Commit(id, sha, date, author, comment))
      id++
    }
    commits = _commits // cache the commits
    return _commits
  } catch (e) {
    // Handle Git errors by returning an empty list
    console.log(`Error fetching commits for branch '${branch}': ${(e as Error).message}`)
    commits = []
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
