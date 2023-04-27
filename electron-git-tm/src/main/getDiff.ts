import { exec } from 'child_process'
import util from 'util'
import { Commit } from './Commit'

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

export async function getDiff(previousCommit: string, currentCommit: string): Promise<string> {
  // call git to get the diff between the two commits
  const execPromisified = util.promisify(exec)
  const gitCommand = ['git', 'diff', previousCommit, currentCommit]
  try {
    const { stdout } = await execPromisified(gitCommand.join(' '))
    return stdout

    // let gitOutput = stdout

    // // decode the output from bytes to a string
    // gitOutput = gitOutput.toString()

    // // add span tags for highlighting "-" and "+" lines
    // const highlightedLines = []
    // const templateColoured = '<span style="color:{{textColour}}">{{line | escape}}</span>'
    // const templateUntouched = '{{line | escape}}'

    // gitOutput.split('\n').forEach((line) => {
    //   if (line.length >= 1 && ['+', '-'].includes(line[0])) {
    //     if (line.length > 1 && ['+', '-'].includes(line[1])) {
    //       highlightedLines.push(env.filters.escape(line))
    //     } else {
    //       const textColour = line[0] === '+' ? 'lightgreen' : 'red'
    //       const renderedLine = env.renderString(templateColoured, {
    //         line,
    //         textColour
    //       })
    //       highlightedLines.push(renderedLine)
    //     }
    //   } else {
    //     highlightedLines.push(env.renderString(templateUntouched, { line }))
    //   }
    // })

    // join the lines back into a string with newline separators
    // gitOutput = highlightedLines.join('\n')

    // // return the diff with highlighted lines
    // return `${gitCommand.join(' ')}\n\n${gitOutput}`
  } catch (e) {
    console.log(`Error getting diff: ${(e as Error).message}`)
    return ''
  }
}
