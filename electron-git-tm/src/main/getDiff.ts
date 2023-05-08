/// <reference types="electron-vite/node" />
import { exec } from 'child_process'
import util from 'util'
import { commits } from './getCommits' // TODO: import from globalsMain
import Handlebars from 'handlebars'
import fs from 'fs'
import t3 from '../../resources/templates/template-diff.hbs?asset'
import t4 from '../../resources/templates/template-diff-js.hbs?asset'
import { repoDir } from './globalsMain'
import { html } from 'Diff2Html'

const templateSource = fs.readFileSync(t3, 'utf8')
const template = Handlebars.compile(templateSource) // Compile the template

const templateSourceJs = fs.readFileSync(t4, 'utf8')
const templateJs = Handlebars.compile(templateSourceJs) // Compile the js template

function _findPreviousCommit(currentCommit: string): string | null {
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

async function _getDiff(previousCommit: string, currentCommit: string): Promise<string> {
  // call git to get the diff between the two commits
  const execPromisified = util.promisify(exec)
  const options = {
    cwd: repoDir,
    maxBuffer: 10 * 1024 * 1024 // 10MB instead of 200 KB
  }
  const gitCommand = ['git', 'diff', previousCommit, currentCommit]
  let stdout = ''
  try {
    ;({ stdout } = await execPromisified(gitCommand.join(' '), options))
  } catch (e) {
    console.log(`Error getting diff: ${(e as Error).message}`)
  }
  return stdout
}

function _renderHtml(stdout, gitCommand): string {
  let msg = ''

  if (stdout.match(/[\x00-\x08\x0E-\x1F]/)) { // eslint-disable-line no-control-regex
    msg = 'binary characters detected - cannot display diff.'
    stdout = ''
  }

  // Uses Diff2Html https://github.com/rtfpessoa/diff2html to convert git diff to html.
  // Can convert into an object first, then use html() to convert to html, or just use html() directly.
  // import { parse, html } from 'Diff2Html'
  // const diffAsObj = parse(stdout, { drawFileList: true })
  // const prettyHtml = html(diffAsObj, { outputFormat: 'side-by-side' })
  const prettyHtml = html(stdout, { outputFormat: 'side-by-side', drawFileList: true })

  const jsFileContents = templateJs({})

  const data = {
    msg: msg,
    diff_body: prettyHtml, //stdout,
    git_cmd: gitCommand.join(' '),
    js: jsFileContents
  }
  const renderedTemplate = template(data)
  return renderedTemplate
}

export async function generate_html_diff(currentCommit: string): Promise<string> {
  const commit = _findPreviousCommit(currentCommit)
  if (commit) {
    const diff = await _getDiff(commit, currentCommit)
    const gitCommand = ['git', 'diff', commit, currentCommit]
    const renderedTemplate = _renderHtml(diff, gitCommand)
    return renderedTemplate
  }
  return ''
}
