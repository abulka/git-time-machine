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

// TODO: cache a list of commits so we don't have to call git every time
// actually we already have this in getCommitsForBranch() !!

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

export async function generate_html_diff(currentCommit: string): Promise<string> {
  const commit = await getPreviousCommit(currentCommit)
  if (commit) {
    const diff = await getDiff(commit, currentCommit)
    return diff
  }
  return ''
}

// def generate_html_diff(self):
//   if event_debug:
//       print('   commit_changed ->', 'on_show_diff')
//   # call git to find the sha of the previous commit to current_commit sha
//   previous_commit = self.get_previous_commit(current_commit)

//   # call git to get the diff between the two commits
//   diff_body = self.get_diff(previous_commit, current_commit)

//   hyperlinks = self.extract_hyperlinks(diff_body)
//   diff_body = self.inject_hyperlinks(diff_body, hyperlinks)

//   toc_template = environment.get_template("links-diff.html")
//   toc_links = toc_template.render(hyperlinks=hyperlinks, add_filename_to_link=add_filename_to_link)

//   js_file_contents = environment.get_template("template-diff.js").render()

//   html_template = environment.get_template("template-diff.html")
//   html_str = html_template.render(toc_links=toc_links, diff_body=diff_body, js=js_file_contents)

//   if html_debug:
//       with open('junk-diff.html', 'w') as f:
//           f.write(html_str)

//   # Set the HTML content
//   self.html.SetPage(html_str, "")
