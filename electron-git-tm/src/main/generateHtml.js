import Handlebars from 'handlebars'
const fs = require('fs')
import path from 'path';
import { getFileContents as getFileContent } from './getFileContent'
import { isText, isBinary, getEncoding } from 'istextorbinary'

// const templateSource = fs.readFileSync('src/main/templates/template-file-contents.hbs', 'utf8')
const templateSource = fs.readFileSync(
  'src/main/templates/template-file-contents-autoload.hbs',
  'utf8'
)
const template = Handlebars.compile(templateSource) // Compile the template

export function generateHtml(commit, fileName) {
  const source_file_contents = getFileContent(commit, fileName)
  const fileExtension = path.extname(fileName)

  const isBinaryFile = isBinary(null, source_file_contents)
  if (isBinaryFile) {
    return 'Binary file'
  }

  const lang_map = {
    '.html': 'html',
    '.css': 'css',
    '.js': 'javascript',
    '.ts': 'typescript',
    '.py': 'python',
    '.java': 'java',
    '.md': 'markdown',
    '.drawio': 'markup',
    '.vue': 'html' // TODO: use vue syntax highlighting via https://vue-prism.netlify.app/ 
    // Add more mappings for other file types as needed e.g. vue
  }
  const lang = lang_map[fileExtension] || 'auto'

  let lang_override = ''
  if (fileExtension == '.md') lang_override = 'markdown' // just for highlight.js auto-detection which doesn't work for markdown

  // Define the data to be used in the template
  const data = {
    title: 'My Title',
    body: 'This is the body of my template.',
    lang: lang,
    lang_override: lang_override,
    vers: '1.29.0', // https://cdnjs.com/libraries/prism/1.29.0
    source_file_contents: source_file_contents,
    js_file_contents: '' // 'console.log("Hello World from template")'
  }

  // Render the template with the data
  const renderedTemplate = template(data)
  return renderedTemplate
}

// const generateHtml = (path, sourceFileContents, scrollTo = null, lineTo = null) => {
//   const pathExtension = path.substring(path.lastIndexOf('.'))
//   const langMap = {
//     '.html': 'html',
//     '.css': 'css',
//     '.js': 'javascript',
//     '.py': 'python',
//     '.java': 'java',
//     '.md': 'markdown'
//     // Add more mappings for other file types as needed
//   }
//   const lang = langMap[pathExtension] || 'auto'

//   const scrollPosX = scrollTo?.x || 0
//   const scrollPosY = scrollTo?.y || 0

//   const jsFileTemplate = environment.getTemplate('template.jinja-js')
//   const jsFileContents = jsFileTemplate.render({
//     scroll_to: scrollTo,
//     scroll_to_x: scrollPosX,
//     line_to: lineTo
//   })

//   const template = environment.getTemplate('template.html')
//   const htmlStr = template.render({
//     lang,
//     source_file_contents: sourceFileContents,
//     js_file_contents: jsFileContents
//   })

//   if (htmlDebug) {
//     const fs = require('fs')
//     fs.writeFileSync('junk-content.html', htmlStr)
//   }

// //   return htmlStr
// }

export function generateHtml_OFFLINE() {
  // return a dummy html file for testing
  return `
  <html>
    <body style="background-color: grey;">
      <h1>Test</h1>
    </body>
  </html>
`
}
