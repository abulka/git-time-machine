import Handlebars from 'handlebars'
const fs = require('fs')
import { getFileContents as getFileContent } from './getFileContent'
import { isBinary } from 'istextorbinary'
import { fileExtToPrismAlias } from './fileExtToPrismAlias'

interface Point {
  x: number
  y: number
}

// const templateSource = fs.readFileSync('src/main/templates/template-file-contents.hbs', 'utf8')
const templateSource = fs.readFileSync(
  'src/main/templates/template-file-contents-autoload.hbs',
  'utf8'
)
const template = Handlebars.compile(templateSource) // Compile the template

const templateSourceJs = fs.readFileSync('src/main/templates/template-file-js.hbs', 'utf8')
const templateJs = Handlebars.compile(templateSourceJs) // Compile the js template

export function generateHtml(
  commit,
  path,
  scrollTo: Point | null = null,
  lineTo: number | null
): string {
  const scrollPosX = scrollTo?.x || 0
  const scrollPosY = scrollTo?.y || 0

  const source_file_contents: string = getFileContent(commit, path)
  console.log('fileName', path)
  const isBinaryFile = isBinary(null, source_file_contents)
  if (isBinaryFile) {
    return 'Binary file'
  }

  const lang = fileExtToPrismAlias(path)

  // highlight.js auto-detection is not working for some files so help it by using the file extension to set the language-* if possible
  const lang_override = lang != '' ? `lang-${lang}` : ''

  const jsFileTemplate = constructJsFileContents(templateJs, scrollPosX, scrollPosY, lineTo)
  // console.log(`${path} jsFileTemplate: ${jsFileTemplate}`)

  // Define the data to be used in the template
  const data = {
    title: 'My Title',
    body: 'This is the body of my template.',
    lang: lang,
    lang_override: lang_override,
    vers: '1.29.0', // https://cdnjs.com/libraries/prism/1.29.0
    source_file_contents: source_file_contents,
    js_file_contents: jsFileTemplate // '' // 'console.log("Hello World from template")'
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

function constructJsFileContents(
  templateJs: Handlebars.TemplateDelegate<any>,
  scrollPosX: number,
  scrollPosY: number,
  lineTo: number | null
): string {
  const data = {
    scroll_to: scrollPosY,
    scroll_to_x: scrollPosX,
    line_to: lineTo
  }
  console.log(`constructJsFileContents: ${scrollPosX} ${scrollPosY} ${lineTo}`)
  const jsFileContents = templateJs(data)
  return jsFileContents
}