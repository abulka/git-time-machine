import Handlebars from 'handlebars'
const fs = require('fs')
import { getFileContents } from './getFileContents'

const templateSource = fs.readFileSync('src/main/templates/template-file-contents.hbs', 'utf8')
const template = Handlebars.compile(templateSource) // Compile the template

export function generateHtml(commit, fileName) {
  const source_file_contents = getFileContents(commit, fileName)

  const lang_map = {
    '.html': 'html',
    '.css': 'css',
    '.js': 'javascript',
    '.py': 'python',
    '.java': 'java',
    '.md': 'markdown',
    // Add more mappings for other file types as needed e.g. vue
}
    // TODO convert lookup into js
    // lang = lang_map.get(file_ext, 'auto') // Use "auto" if extension is not recognized
    // const fileExtension = ??
    // const lang = lang_map[fileExtension] ???
    const lang = 'javasscript'

  // Define the data to be used in the template
  const data = {
    title: 'My Title',
    body: 'This is the body of my template.',
    lang: lang,
    source_file_contents: source_file_contents,
    // js_file_contents: 'console.log("Hello World from template")'
    js_file_contents: ''
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
