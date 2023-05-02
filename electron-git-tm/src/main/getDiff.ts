/// <reference types="electron-vite/node" />
import { exec } from 'child_process'
import util from 'util'
import { commits } from './getCommits' // TODO: import from globalsMain
import Handlebars from 'handlebars'
import fs from 'fs';
import t3 from '../../resources/templates/template-diff.hbs?asset'
import { repoDir } from './globalsMain'

function findPreviousCommit(currentCommit: string): string | null {
  for (let i = 0; i < commits.length; i++) {
    if (commits[i].sha.startsWith(currentCommit)) {
    // if (commits[i].sha === currentCommit) { // TODO: use full length sha strings
      if (i < commits.length - 1) {
        return commits[i + 1].sha
      } else {
        return null
      }
    }
  }
  return null
}

export async function getDiff(previousCommit: string, currentCommit: string): Promise<string> {
  const templateSource = fs.readFileSync(t3, 'utf8')
  const template = Handlebars.compile(templateSource) // Compile the template

  // call git to get the diff between the two commits
  const execPromisified = util.promisify(exec)
  const options = { 
    cwd: repoDir,
    maxBuffer: 10 * 1024 * 1024 // 10MB instead of 200 KB
  }
  const gitCommand = ['git', 'diff', previousCommit, currentCommit]
  // console.log('gitCommand', gitCommand)
  try {
    const { stdout } = await execPromisified(gitCommand.join(' '), options)
    // console.log(`stdout ${stdout}`)

    const data = {
      diff_body: stdout,
      toc_links: '',
      git_cmd: gitCommand.join(' '),
      js: '' // 'console.log("Hello World from template")'
    }

    if (data.diff_body.match(/[\x00-\x08\x0E-\x1F]/)) { // eslint-disable-line no-control-regex
      data.diff_body = 'diff contains binary characters!'
    }
    if (data.diff_body.length > 100000) {
      data.diff_body = 'diff too long'
    }

    const renderedTemplate = template(data)
    return renderedTemplate

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
  const commit = findPreviousCommit(currentCommit)
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
